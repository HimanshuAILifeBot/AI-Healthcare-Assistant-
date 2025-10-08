import os
import psycopg2
from typing import List, TypedDict
from dotenv import load_dotenv

from langchain.schema import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from db import get_db_connection

from langchain_google_genai import ChatGoogleGenerativeAI
# Load environment variables
load_dotenv()

# Shared LangGraph state definition
class AgentState(TypedDict):
    phrases: List[str]
    normalized_symptoms: List[str]
    specialists: List[str]
    recommended_specialists: List[str]
    doctors: List[dict]

# Initialize Gemini-2.0-flash
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.3,
    google_api_key= os.getenv("GEMINI_API_KEY")
)

# Normalize Agent using Gemini-2.0-flash
def normalize_agent(state: AgentState) -> AgentState:
    print("\nGemini-2.0-flash Normalize Agent running...")
    prompt = (
        "You are a medical assistant. Normalize the following patient symptom phrases "
        "into a list of clinical symptom terms. Only output comma-separated clinical terms.\n"
        f"Patient phrases: {state['phrases']}"
    )
    messages = [
        SystemMessage(content="You are a helpful medical assistant."),
        HumanMessage(content=prompt)
    ]
    response = llm.invoke(messages)
    raw_output = response.content
    normalized = [term.strip().lower() for term in raw_output.split(",") if term.strip()]
    return {"normalized_symptoms": normalized}

# Specialist Lookup Agent (via stored procedure)
def specialist_lookup_agent(state: AgentState) -> AgentState:
    print("\nLooking up specialists for:", state.get("normalized_symptoms", []))
    normalized = state.get("normalized_symptoms", [])
    original_phrases = state.get("phrases", [])
    
    if not normalized:
        print("No normalized symptoms found")
        return {"specialists": []}

    conn = get_db_connection()
    cur = conn.cursor()
    specialists = []
    
    try:
        # First try with normalized symptoms
        print(f"Executing sp_get_specialists with normalized symptoms: {normalized}")
        cur.execute("SELECT * FROM sp_get_specialists(%s)", (normalized,))
        specialists_result = cur.fetchall()
        specialists = [row[0] for row in specialists_result]
        print(f"Found specialists with normalized symptoms: {specialists}")
        
        # If no specialists found with normalized symptoms, try original phrases as fallback
        if not specialists and original_phrases:
            print(f"No specialists found with normalized symptoms, trying original phrases: {original_phrases}")
            # Try multiple variations: original, title case, and lowercase
            variations_to_try = [
                original_phrases,  # original case
                [phrase.title() for phrase in original_phrases],  # title case
                [phrase.lower() for phrase in original_phrases],  # lowercase
            ]
            
            for variation in variations_to_try:
                if specialists:  # Stop if we found specialists
                    break
                print(f"Trying variation: {variation}")
                cur.execute("SELECT * FROM sp_get_specialists(%s)", (variation,))
                specialists_result = cur.fetchall()
                specialists = [row[0] for row in specialists_result]
                if specialists:
                    print(f"Found specialists with variation {variation}: {specialists}")
                    break
            
    except Exception as e:
        print("Error in specialist_lookup_agent:", e)
        specialists = []
    finally:
        cur.close()
        conn.close()

    return {"specialists": specialists}

# Helper function to find matching specialization using fuzzy matching
def find_matching_specialization(specialist_name: str, db_specializations: List[str]) -> str:
    """
    Find the best matching specialization from database for a given specialist name.
    Uses various matching strategies including exact match, substring match, and common mappings.
    """
    specialist_lower = specialist_name.lower().strip()
    
    # Direct exact match
    for specialization in db_specializations:
        if specialist_lower == specialization.lower():
            return specialization
    
    # Common specialist-to-specialization mappings (comprehensive)
    common_mappings = {
        "cardiologist": ["cardiology"],
        "heart specialist": ["cardiology"],
        "heart doctor": ["cardiology"],
        "neurologist": ["neurology"],
        "brain doctor": ["neurology"],
        "brain specialist": ["neurology"],
        "neuro specialist": ["neurology"],
        "dermatologist": ["dermatology"],
        "skin doctor": ["dermatology"],
        "skin specialist": ["dermatology"],
        "orthopedic surgeon": ["orthopedics"],
        "orthopedist": ["orthopedics"],
        "bone specialist": ["orthopedics"],
        "bone doctor": ["orthopedics"],
        "joint specialist": ["orthopedics"],
        "pediatrician": ["pediatrics"],
        "child doctor": ["pediatrics"],
        "child specialist": ["pediatrics"],
        "general medicine": ["family medicine"],
        "family doctor": ["family medicine"],
        "family physician": ["family medicine"],
        "psychiatrist": ["psychiatry"],
        "mental health doctor": ["psychiatry"],
        "gynecologist": ["obstetrics and gynecology"],
        "obstetrician": ["obstetrics and gynecology"],
        "oncologist": ["oncology"],
        "cancer specialist": ["oncology"],
        "radiologist": ["radiology"],
        "anesthesiologist": ["anesthesiology"],
        "surgeon": ["general surgery"],
        "general surgeon": ["general surgery"],
        "ophthalmologist": ["ophthalmology"],
        "eye doctor": ["ophthalmology"],
        "eye specialist": ["ophthalmology"],
        "ent specialist": ["otolaryngology"],
        "ent doctor": ["otolaryngology"],
        "throat doctor": ["otolaryngology"],
        "ear doctor": ["otolaryngology"],
        "urologist": ["urology"],
        "nephrologist": ["nephrology"],
        "kidney specialist": ["nephrology"],
        "kidney doctor": ["nephrology"],
        "gastroenterologist": ["gastroenterology"],
        "stomach doctor": ["gastroenterology"],
        "digestive specialist": ["gastroenterology"],
        "pulmonologist": ["pulmonology"],
        "lung doctor": ["pulmonology"],
        "lung specialist": ["pulmonology"],
        "rheumatologist": ["rheumatology"],
        "endocrinologist": ["endocrinology"],
        "allergist": ["allergist/immunologist"],
        "immunologist": ["allergist/immunologist"],
        "pathologist": ["pathology"],
        "geriatrician": ["geriatrics"],
        "hematologist": ["hematology"],
        "infectious disease specialist": ["infectious disease"]
    }
    
    # Try mapping-based matching first (most reliable)
    if specialist_lower in common_mappings:
        target_specializations = common_mappings[specialist_lower]
        for specialization in db_specializations:
            spec_lower = specialization.lower()
            for target in target_specializations:
                # Exact match
                if target == spec_lower:
                    return specialization
                # Target is in specialization (e.g., "neurology" in "Neurology")
                if target in spec_lower:
                    return specialization
    
    # Try removing common suffixes (e.g., "Neurologist" -> "Neuro")
    # This helps when common_mappings don't have an entry
    specialist_root = specialist_lower
    for suffix in ["ist", "er", "ian", "or"]:
        if specialist_lower.endswith(suffix):
            specialist_root = specialist_lower[:-len(suffix)]
            break
    
    # Try matching with the root
    for specialization in db_specializations:
        spec_lower = specialization.lower()
        # Check if root matches beginning of specialization
        if spec_lower.startswith(specialist_root) and len(specialist_root) >= 4:
            return specialization
        # Check if specialization root matches specialist root
        spec_root = spec_lower.rstrip("y").rstrip("ic").rstrip("al")
        if specialist_root == spec_root and len(specialist_root) >= 4:
            return specialization
    
    # Substring matching - check if specialist name contains specialization or vice versa
    for specialization in db_specializations:
        spec_lower = specialization.lower()
        # Only match if substring is significant (>= 5 characters)
        if len(specialist_lower) >= 5 and specialist_lower in spec_lower:
            return specialization
        if len(spec_lower) >= 5 and spec_lower in specialist_lower:
            return specialization
    
    # If no match found, return None
    return None

# LLM-Based Specialist Recommender Agent
def recommend_specialists_agent(state: AgentState) -> AgentState:
    print("\nRecommending best specialists using Gemini...")
    symptoms = state.get("normalized_symptoms", [])
    specialists = state.get("specialists", [])
    if not specialists or not symptoms:
        return {"recommended_specialists": []}

    # If we have 3 or fewer specialists, just use all of them (they're already relevant)
    if len(specialists) <= 3:
        print(f"Using all {len(specialists)} specialists (≤3): {specialists}")
        recommended = specialists
    else:
        # Only use LLM to narrow down if we have more than 3 specialists
        prompt = (
            f"You are a medical assistant. A patient reported the following symptoms: {', '.join(symptoms)}.\n"
            f"The following specialists are available: {', '.join(specialists)}.\n"
            "From this list, select ALL specialists that could help with these symptoms.\n"
            "Return ALL relevant specialist names as a comma-separated list. Do not limit to just 1-2.\n"
            "Only return the specialist names, nothing else."
        )
        messages = [
            SystemMessage(content="You are an intelligent medical assistant that triages patients."),
            HumanMessage(content=prompt)
        ]
        response = llm.invoke(messages)
        raw_output = response.content
        recommended = [name.strip() for name in raw_output.split(",") if name.strip() in specialists]
        print(f"LLM recommended {len(recommended)} out of {len(specialists)} specialists: {recommended}")
    
    # Dynamically get specialist-to-specialization mapping from database
    mapped_specialists = []
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Get all unique specializations from doctors table
        cur.execute("SELECT DISTINCT specialization FROM doctors")
        db_specializations = [row[0] for row in cur.fetchall()]
        print(f"Available specializations in database: {db_specializations}")
        
        for specialist in recommended:
            # Try to find matching specialization using fuzzy matching
            matched_specialization = find_matching_specialization(specialist, db_specializations)
            if matched_specialization:
                print(f"✓ Mapped '{specialist}' -> '{matched_specialization}'")
                # Only add if not already in the list (avoid duplicates)
                if matched_specialization not in mapped_specialists:
                    mapped_specialists.append(matched_specialization)
            else:
                print(f"❌ Failed to map '{specialist}'")
                print(f"   Attempting alternative mapping strategies...")
                
                # Try alternative strategies
                # 1. Check if the specialist name itself exists in db_specializations
                for db_spec in db_specializations:
                    if specialist.lower() in db_spec.lower() or db_spec.lower() in specialist.lower():
                        print(f"✓ Alternative match found: '{specialist}' -> '{db_spec}'")
                        if db_spec not in mapped_specialists:
                            mapped_specialists.append(db_spec)
                        break
                else:
                    # 2. If still no match, log detailed info for debugging
                    print(f"❌ No match found for '{specialist}' in database specializations")
                    print(f"   Specialist (lowercase): '{specialist.lower()}'")
                    print(f"   Trying to match against: {[s.lower() for s in db_specializations][:5]}...")
                
    except Exception as e:
        print(f"Error getting specializations from database: {e}")
        # Fallback to original recommended specialists
        mapped_specialists = recommended
    finally:
        cur.close()
        conn.close()
    
    print(f"Mapped specialists: {mapped_specialists}")
    return {"recommended_specialists": mapped_specialists}

# Utility function to get all available specializations (for external use)
def get_available_specializations():
    """
    Get all available specializations from the database.
    Useful for administrative interfaces or external systems.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT DISTINCT specialization FROM doctors ORDER BY specialization")
        return [row[0] for row in cur.fetchall()]
    except Exception as e:
        print(f"Error getting specializations: {e}")
        return []
    finally:
        cur.close()
        conn.close()

# Utility function to test specialist mapping (for debugging)
def test_specialist_mapping(specialist_name: str):
    """
    Test how a specialist name would be mapped to specializations.
    Useful for debugging and validation.
    """
    db_specializations = get_available_specializations()
    matched = find_matching_specialization(specialist_name, db_specializations)
    return {
        "input": specialist_name,
        "matched_specialization": matched,
        "available_specializations": db_specializations
    }

# Doctor Info Agent (via stored procedure)
def fetch_doctor_details_agent(state: AgentState) -> AgentState:
    print("\nFetching doctor info for:", state.get("recommended_specialists", []))
    recommended = state.get("recommended_specialists", [])
    if not recommended:
        return {"doctors": []}

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        print(f"Executing sp_get_doctors_by_specialists with specialists: {recommended}")
        cur.execute("SELECT * FROM sp_get_doctors_by_specialists(%s)", (recommended,))
        doctor_rows = cur.fetchall()
        doctors = []
        for row in doctor_rows:
            doctors.append({
                "doctor_id": row[0],
                "name": row[1],
                "specialization": row[2],
                "rating": float(row[3]),
                "fees": int(row[4]) if row[4] else 0,
                "hospital": row[5],
                "next_available_date": str(row[6]) if row[6] else "Not available",
                "start_time": str(row[7]) if row[7] else "N/A",
                "end_time": str(row[8]) if row[8] else "N/A",
                "slot_id": row[9]
            })
        print(f"Found {len(doctors)} doctors")
    except Exception as e:
        print("Error in fetch_doctor_details_agent:", e)
        doctors = []
    finally:
        cur.close()
        conn.close()

    return {"doctors": doctors}

# Build LangGraph flow
def build_graph():
    builder = StateGraph(AgentState)
    builder.add_node("normalize_agent", normalize_agent)
    builder.add_node("specialist_lookup_agent", specialist_lookup_agent)
    builder.add_node("recommend_specialists_agent", recommend_specialists_agent)
    builder.add_node("fetch_doctor_details_agent", fetch_doctor_details_agent)

    builder.set_entry_point("normalize_agent")
    builder.add_edge("normalize_agent", "specialist_lookup_agent")
    builder.add_edge("specialist_lookup_agent", "recommend_specialists_agent")
    builder.add_edge("recommend_specialists_agent", "fetch_doctor_details_agent")
    builder.add_edge("fetch_doctor_details_agent", END)
    return builder.compile()
