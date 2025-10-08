from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str
    phone: str
    dateOfBirth: str
    gender: str
    bloodGroup: str
    maritalStatus: str
    medicalHistory: Optional[str] = None
    allergies: Optional[str] = None
    currentMedications: Optional[str] = None

class AppointmentRequest(BaseModel):
    patient_id: int
    doctor_id: int
    slot_id: int
    reason: str

class PatientDetailsResponse(BaseModel):
    name: str
    date_of_birth: str
    gender: str
    contact_number: str
    medical_record_number: str
    blood_group: str
    marital_status: str
    id: int

class MedicalHistoryResponse(BaseModel):
    past_diagnoses: Optional[str]
    surgeries: Optional[str]
    hospital_admissions: Optional[str]
    immunization_records: Optional[str]
    family_medical_history: Optional[str]
    lifestyle_factors: Optional[str]

class AppointmentResponse(BaseModel):
    id: int
    doctor_name: str
    doctor_specialization: str
    hospital_name: str
    appointment_date: str
    appointment_time: str
    reason: Optional[str]
    status: str

class TTSRequest(BaseModel):
    text: str
    language: Optional[str] = "en-US"
    voice_name: Optional[str] = None