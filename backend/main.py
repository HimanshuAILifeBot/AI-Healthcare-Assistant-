from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import logging
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from config import Config
from db import get_db_connection
from smart_connection import get_smart_connection
from models import LoginRequest, SignupRequest, AppointmentRequest, AppointmentResponse
from preprocess import preprocess_text
from queries import *
from langgraph_llm_agents import build_graph
from models import PatientDetailsResponse
from models import MedicalHistoryResponse
from models import TTSRequest
from pydantic import BaseModel
from azure_tts import synthesize_speech_azure, shutdown_tts
from invoice_generator import generate_invoice, generate_invoice_filename
from email_service import EmailService, save_invoice_locally
import base64

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize FAISS index and terms list
# Example: Load your terms and build the index here
terms = [
    "fever", "cough", "headache", "diabetes", "hypertension"
    # Add your medical terms here
]
term_embeddings = model.encode(terms)
dimension = term_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(term_embeddings))

app.add_middleware(
    CORSMiddleware,
    allow_origins=[Config.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use smart connection that auto-reconnects on SSL errors
conn = get_smart_connection()


@app.get("/")
async def root():
    return {"message": "Welcome to the Healthcare Agent API!"}

@app.post("/login")
def login(request: LoginRequest):
    logger.info(f"Login attempt: {request.email} / {request.password}")
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM sp_login_user(%s::TEXT, %s::TEXT)", (request.email, request.password))
        user = cur.fetchone()
        cur.close()
    except Exception as e:
        logger.error(f"Database error during login: {e}")
        conn.rollback()
        cur.close()
        raise HTTPException(status_code=500, detail="Login failed")

    if user:
        return JSONResponse(content={"message": "Login successful", "user_id": user[0]})
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/signup")
def signup(request: SignupRequest):
    logger.info(f"Signup attempt: {request.email}")
    cur = conn.cursor()
    try:
        # Insert directly into patients table (no separate users table in new schema)
        cur.execute(
            """INSERT INTO patients (
                name, email, phone, password_hash, date_of_birth, gender, blood_group
            ) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id""",
            (
                request.name, request.email, request.phone, request.password,
                request.dateOfBirth, request.gender, request.bloodGroup
            )
        )
        patient_id = cur.fetchone()[0]
        
        # Insert medical history if provided
        if request.medicalHistory or request.allergies or request.currentMedications:
            history_parts = []
            if request.medicalHistory:
                history_parts.append(f"Medical History: {request.medicalHistory}")
            if request.allergies:
                history_parts.append(f"Allergies: {request.allergies}")
            if request.currentMedications:
                history_parts.append(f"Current Medications: {request.currentMedications}")
            medical_history_text = " | ".join(history_parts)
            
            cur.execute(
                """INSERT INTO medical_records (
                    patient_id, record_type, description
                ) VALUES (%s, %s, %s)""",
                (patient_id, 'Medical History', medical_history_text)
            )
        
        conn.commit()
        cur.close()
        
        return JSONResponse(content={
            "message": "Signup successful", 
            "user_id": patient_id,  # Use patient_id as user_id
            "patient_id": patient_id
        })
        
    except Exception as e:
        logger.error(f"Database error during signup: {e}")
        conn.rollback()
        cur.close()
        raise HTTPException(status_code=500, detail="Signup failed")

@app.get("/patient-details/{user_id}", response_model=PatientDetailsResponse)
def get_patient_details(user_id: int):
    logger.info(f"Fetching patient details for user_id={user_id}")
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM sp_get_patient_details(%s);", (user_id,))
        row = cur.fetchone()
        logger.info(f"Fetched row: {row}")
        cur.close()
    except Exception as e:
        logger.error(f"DB error in patient-details: {e}")
        conn.rollback()
        cur.close()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    if row:
        return jsonable_encoder({
            "name": row[0], "date_of_birth": row[1], "gender": row[2], "contact_number": row[3],
            "medical_record_number": row[4], "blood_group": row[5], "marital_status": row[6], "id": row[7]
        })
    raise HTTPException(status_code=404, detail="Patient not found")


@app.get("/medical-history/{user_id}", response_model=MedicalHistoryResponse)
def get_medical_history(user_id: int):
    logger.info(f"Fetching medical history for user_id={user_id}")
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM sp_get_patient_id(%s);", (user_id,))
        patient_row = cur.fetchone()
        logger.info(f"Patient row: {patient_row}")
        if not patient_row:
            cur.close()
            raise HTTPException(status_code=404, detail="Patient not found")
        patient_id = patient_row[0]

        cur.execute("SELECT * FROM sp_get_medical_history(%s);", (patient_id,))
        row = cur.fetchone()
        logger.info(f"Medical history row: {row}")
        cur.close()
    except Exception as e:
        logger.error(f"DB error in medical-history: {e}")
        conn.rollback()
        cur.close()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    if row:
        return jsonable_encoder({
            "past_diagnoses": row[0], "surgeries": row[1], "hospital_admissions": row[2],
            "immunization_records": row[3], "family_medical_history": row[4], "lifestyle_factors": row[5]
        })
    raise HTTPException(status_code=404, detail="Medical history not found")

@app.get("/appointments/{user_id}")
def get_user_appointments(user_id: int):
    logger.info(f"Fetching appointments for user_id={user_id}")
    cur = conn.cursor()
    try:
        # First get patient_id from user_id
        cur.execute("SELECT id FROM patients WHERE user_id = %s", (user_id,))
        patient_row = cur.fetchone()
        if not patient_row:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        patient_id = patient_row[0]
        
        # Get appointments with doctor and hospital details
        cur.execute("""
            SELECT 
                a.id,
                d.name as doctor_name,
                d.specialization,
                h.name as hospital_name,
                asl.available_date,
                asl.start_time,
                a.reason,
                'Scheduled' as status
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.id
            JOIN availability_slots asl ON a.slot_id = asl.id
            LEFT JOIN hospitals h ON d.hospital_id = h.id
            WHERE a.patient_id = %s
            ORDER BY asl.available_date DESC, asl.start_time DESC
        """, (patient_id,))
        
        appointment_rows = cur.fetchall()
        cur.close()
        
        appointments = []
        for row in appointment_rows:
            appointments.append({
                "id": row[0],
                "doctor_name": row[1],
                "doctor_specialization": row[2],
                "hospital_name": row[3] or "General Hospital",
                "appointment_date": str(row[4]),
                "appointment_time": str(row[5]),
                "reason": row[6],
                "status": row[7]
            })
        
        return {"appointments": appointments}
        
    except Exception as e:
        logger.error(f"DB error in get_user_appointments: {e}")
        conn.rollback()
        cur.close()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@app.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int):
    logger.info(f"Deleting appointment with id={appointment_id}")
    cur = conn.cursor()
    try:
        # Check if appointment exists
        cur.execute("SELECT id FROM appointments WHERE id = %s", (appointment_id,))
        if not cur.fetchone():
            cur.close()
            raise HTTPException(status_code=404, detail="Appointment not found")
        
        # Delete the appointment
        cur.execute("DELETE FROM appointments WHERE id = %s", (appointment_id,))
        conn.commit()
        cur.close()
        
        logger.info(f"Successfully deleted appointment {appointment_id}")
        return {"message": "Appointment deleted successfully", "appointment_id": appointment_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"DB error in delete_appointment: {e}")
        conn.rollback()
        cur.close()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


from typing import List

class NormalizeRequest(BaseModel):
    phrases: List[str]

# Add a request model for run_langgraph
class LangGraphRequest(BaseModel):
    phrases: List[str]
    
@app.post("/normalize")
async def normalize(request: NormalizeRequest):
    phrases = request.phrases
    results = []
    for phrase in phrases:
        cleaned = preprocess_text(phrase)
        if not cleaned:
            continue
        emb = model.encode([cleaned])
        D, I = index.search(np.array(emb), 1)
        distance = D[0][0]
        match = terms[I[0][0]]
        if distance > 1.0:
            continue
        results.append({"original": phrase, "cleaned": cleaned, "match": match, "score": float(distance)})
    return {"results": results}

@app.post("/run_langgraph")
async def run_langgraph(request: LangGraphRequest):
    phrases = request.phrases
    if not phrases:
        raise HTTPException(status_code=400, detail="No phrases provided.")
    graph = build_graph()
    final_state = graph.invoke({"phrases": phrases})
    return {
        "phrases": final_state.get("phrases", []),
        "normalized_symptoms": final_state.get("normalized_symptoms", []),
        "specialists": final_state.get("specialists", []),
        "recommended_specialists": final_state.get("recommended_specialists", []),
        "doctors": final_state.get("doctors", [])
    }


@app.post("/appointments")
async def create_appointment(req: AppointmentRequest):
    cur = conn.cursor()
    try:
        # Create appointment
        cur.execute("SELECT * FROM sp_create_appointment(%s, %s, %s, %s)", 
                   (req.patient_id, req.doctor_id, req.slot_id, req.reason))
        appointment_id = cur.fetchone()[0]
        conn.commit()
        
        # Generate and send invoice asynchronously
        try:
            await generate_and_send_invoice(appointment_id, req.patient_id, req.doctor_id, req.slot_id, req.reason)
        except Exception as invoice_error:
            logger.error(f"Failed to generate/send invoice: {invoice_error}")
            # Don't fail the appointment creation if invoice fails
        
        cur.close()
        return {"message": "Appointment created and invoice sent", "appointment_id": appointment_id}
    except Exception as e:
        conn.rollback()
        cur.close()
        raise HTTPException(status_code=500, detail=str(e))


async def generate_and_send_invoice(appointment_id, patient_id, doctor_id, slot_id, reason):
    """
    Generate invoice PDF and send via email (agentic workflow)
    """
    cur = conn.cursor()
    try:
        # Fetch patient details
        cur.execute("""
            SELECT p.name, p.contact_number, p.medical_record_number, 
                   p.blood_group, u.email
            FROM patients p
            JOIN users u ON p.user_id = u.id
            WHERE p.id = %s
        """, (patient_id,))
        patient_row = cur.fetchone()
        if not patient_row:
            raise Exception("Patient not found")
        
        patient_data = {
            'name': patient_row[0],
            'contact_number': patient_row[1],
            'medical_record_number': patient_row[2],
            'blood_group': patient_row[3],
            'email': patient_row[4]
        }
        
        # Fetch doctor and appointment details
        cur.execute("""
            SELECT d.name, d.specialization, h.name, asl.available_date, 
                   asl.start_time, d.consultation_fees
            FROM doctors d
            LEFT JOIN hospitals h ON d.hospital_id = h.id
            JOIN availability_slots asl ON asl.id = %s
            WHERE d.id = %s
        """, (slot_id, doctor_id))
        doctor_row = cur.fetchone()
        if not doctor_row:
            raise Exception("Doctor not found")
        
        doctor_data = {
            'doctor_name': doctor_row[0],
            'specialization': doctor_row[1],
            'hospital_name': doctor_row[2] or 'General Hospital',
            'fees': doctor_row[5] or 500
        }
        
        appointment_data = {
            'id': appointment_id,
            'appointment_date': str(doctor_row[3]),
            'appointment_time': str(doctor_row[4]),
            'reason': reason,
            'transaction_id': f'RAZORPAY_{appointment_id:05d}'
        }
        
        # Generate invoice PDF
        logger.info(f"Generating invoice for appointment {appointment_id}")
        invoice_pdf = generate_invoice(appointment_data, patient_data, doctor_data)
        
        # Initialize email service
        email_service = EmailService()
        
        # Check if email configuration is available
        if email_service.sender_email and email_service.sender_password:
            # Send invoice via email
            success = email_service.send_invoice_email(
                recipient_email=patient_data['email'],
                patient_name=patient_data['name'],
                invoice_pdf=invoice_pdf,
                appointment_data=appointment_data,
                doctor_data=doctor_data
            )
            
            if success:
                logger.info(f"Invoice emailed successfully to {patient_data['email']}")
            else:
                logger.warning("Email sending failed, saving invoice locally")
                filename = generate_invoice_filename(appointment_id, patient_data['name'])
                save_invoice_locally(invoice_pdf, filename)
        else:
            # Fallback: Save invoice locally if email not configured
            logger.info("Email not configured, saving invoice locally")
            filename = generate_invoice_filename(appointment_id, patient_data['name'])
            save_invoice_locally(invoice_pdf, filename)
        
    except Exception as e:
        logger.error(f"Error in generate_and_send_invoice: {e}")
        raise
    finally:
        cur.close()

@app.get("/appointments/{user_id}")
def get_user_appointments(user_id: int):
    logger.info(f"Fetching appointments for user_id={user_id}")
    cur = conn.cursor()
    try:
        # First get the patient_id from user_id
        cur.execute("SELECT * FROM sp_get_patient_id(%s);", (user_id,))
        patient_row = cur.fetchone()
        if not patient_row:
            raise HTTPException(status_code=404, detail="Patient not found")
        
        patient_id = patient_row[0]
        
        # Get appointments with doctor and hospital details
        cur.execute("""
            SELECT 
                a.id,
                d.name as doctor_name,
                d.specialization,
                h.name as hospital_name,
                s.available_date,
                s.start_time,
                a.reason,
                CASE 
                    WHEN s.available_date < CURRENT_DATE THEN 'Completed'
                    WHEN s.available_date = CURRENT_DATE AND s.start_time < CURRENT_TIME THEN 'Completed'
                    ELSE 'Scheduled'
                END as status
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.id
            JOIN hospitals h ON d.hospital_id = h.id
            JOIN availability_slots s ON a.slot_id = s.id
            WHERE a.patient_id = %s
            ORDER BY s.available_date DESC, s.start_time DESC
        """, (patient_id,))
        
        appointments_data = cur.fetchall()
        cur.close()
        
        appointments = []
        for row in appointments_data:
            appointments.append({
                "id": row[0],
                "doctor_name": row[1],
                "doctor_specialization": row[2],
                "hospital_name": row[3],
                "appointment_date": str(row[4]),
                "appointment_time": str(row[5]),
                "reason": row[6],
                "status": row[7]
            })
        
        return {"appointments": appointments}
        
    except Exception as e:
        logger.error(f"Error fetching appointments: {e}")
        cur.close()
        raise HTTPException(status_code=500, detail=f"Failed to fetch appointments: {e}")

@app.post("/tts")
async def text_to_speech(request: TTSRequest):
    """
    Convert text to speech using Azure TTS.
    
    Args:
        request: TTSRequest containing text, language, and optional voice_name
    
    Returns:
        JSON with base64 encoded audio data
    """
    logger.info(f"TTS request: {request.text[:50]}... (language: {request.language})")
    
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        audio_data = await synthesize_speech_azure(
            text=request.text,
            language=request.language,
            voice_name=request.voice_name
        )
        
        if audio_data:
            return JSONResponse(content={
                "success": True,
                "audio_data": audio_data,
                "text": request.text
            })
        else:
            raise HTTPException(status_code=500, detail="Failed to generate speech")
            
    except Exception as e:
        logger.error(f"Error in TTS endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"TTS error: {str(e)}")
    
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/patient/{user_id}")
def get_patient_name(user_id: int):
    """Get patient name for voice biometrics greeting"""
    logger.info(f"Fetching patient name for user_id={user_id}")
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT name FROM patients WHERE user_id = %s
        """, (user_id,))
        result = cur.fetchone()
        cur.close()
        
        if result:
            return {"name": result[0]}
        else:
            raise HTTPException(status_code=404, detail="Patient not found")
    except Exception as e:
        logger.error(f"Error fetching patient name: {e}")
        cur.close()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/doctors")
def get_doctors(specialty: str):
    logger.info(f"Fetching doctors for specialty: {specialty}")
    cur = conn.cursor()
    try:
        cur.execute(GET_DOCTORS_BY_SPECIALIST, (specialty,))
        rows = cur.fetchall()
        cur.close()
    except Exception as e:
        logger.error(f"DB error in doctors: {e}")
        conn.rollback()
        cur.close()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    if rows:
        doctors = []
        for row in rows:
            doctors.append({
                "doctor_id": row[0],
                "name": row[1],
                "specialization": row[2],
                "experience": row[3],
                "rating": row[4],
                "hospital_id": row[5]
            })
        return {"doctors": doctors}
    raise HTTPException(status_code=404, detail="No doctors found for this specialty")