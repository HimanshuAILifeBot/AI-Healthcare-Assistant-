#!/usr/bin/env python3
"""
Test script for dynamic specialist-to-specialization mapping
"""

from langgraph_llm_agents import build_graph, find_matching_specialization
from db import get_db_connection

def test_dynamic_mapping():
    """Test the dynamic mapping functionality"""
    print("Testing Dynamic Specialist-to-Specialization Mapping")
    print("=" * 60)
    
    # Get all specializations from database
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT DISTINCT specialization FROM doctors ORDER BY specialization")
        db_specializations = [row[0] for row in cur.fetchall()]
        print(f"Available specializations in database: {db_specializations}")
        print()
    except Exception as e:
        print(f"Error getting specializations: {e}")
        return
    finally:
        cur.close()
        conn.close()
    
    # Test various specialist names
    test_specialists = [
        "Cardiologist",
        "Neurologist", 
        "Dermatologist",
        "Orthopedic Surgeon",
        "Pediatrician",
        "General Medicine",
        "Heart Specialist",  # Alternative name
        "Brain Doctor",      # Alternative name
        "Skin Doctor",       # Alternative name
        "Bone Specialist",   # Alternative name
        "Child Doctor",      # Alternative name
        "Family Doctor"      # Alternative name
    ]
    
    print("Testing specialist name mappings:")
    print("-" * 40)
    
    for specialist in test_specialists:
        matched = find_matching_specialization(specialist, db_specializations)
        if matched:
            print(f"✓ '{specialist}' -> '{matched}'")
        else:
            print(f"✗ '{specialist}' -> No match found")
    
    print("\n" + "=" * 60)
    print("Testing complete workflow with sample symptoms...")
    
    # Test the complete workflow
    graph = build_graph()
    initial_state = {
        "phrases": ["I have chest pain and shortness of breath"],
        "normalized_symptoms": [],
        "specialists": [],
        "recommended_specialists": [],
        "doctors": []
    }
    
    try:
        result = graph.invoke(initial_state)
        print("\nWorkflow Results:")
        print(f"Normalized symptoms: {result.get('normalized_symptoms', [])}")
        print(f"Found specialists: {result.get('specialists', [])}")
        print(f"Recommended specialists: {result.get('recommended_specialists', [])}")
        print(f"Found doctors: {len(result.get('doctors', []))} doctors")
        
        for doctor in result.get('doctors', [])[:3]:  # Show first 3 doctors
            print(f"  - Dr. {doctor['name']} ({doctor['specialization']}) - Rating: {doctor['rating']}")
            
    except Exception as e:
        print(f"Error in workflow: {e}")

if __name__ == "__main__":
    test_dynamic_mapping()