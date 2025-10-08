"""
Database queries for the healthcare voice assistant.
"""

# SQL queries for various operations
GET_PATIENT_DETAILS = """
SELECT * FROM patients WHERE patient_id = %s
"""

GET_MEDICAL_HISTORY = """
SELECT * FROM medical_history WHERE patient_id = %s
"""

GET_DOCTORS_BY_SPECIALIST = """
SELECT * FROM doctors WHERE LOWER(specialization) = LOWER(%s)
"""

GET_SPECIALISTS = """
SELECT DISTINCT specialty FROM doctors
"""

LOGIN_USER = """
SELECT patient_id, username FROM patients 
WHERE username = %s AND password = %s
"""

CREATE_APPOINTMENT = """
INSERT INTO appointments (patient_id, doctor_id, appointment_date, appointment_time, status)
VALUES (%s, %s, %s, %s, %s)
RETURNING appointment_id
"""