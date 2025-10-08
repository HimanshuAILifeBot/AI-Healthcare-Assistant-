
import psycopg2
from config import Config

def get_all_doctors():
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            port=Config.DB_PORT
        )
        cur = conn.cursor()
        cur.execute("SELECT id, name, specialization, experience, rating, hospital_id, consultation_fee FROM doctors")
        doctors = cur.fetchall()
        cur.close()
        return doctors
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_doctors_by_specialization(specialization):
    """Get doctors filtered by specialization"""
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            port=Config.DB_PORT
        )
        cur = conn.cursor()
        cur.execute("""
            SELECT d.id, d.name, d.specialization, d.experience, d.rating, 
                   h.name as hospital_name, d.consultation_fee
            FROM doctors d
            LEFT JOIN hospitals h ON d.hospital_id = h.id
            WHERE LOWER(d.specialization) = LOWER(%s)
            ORDER BY d.rating DESC, d.experience DESC
        """, (specialization,))
        doctors = cur.fetchall()
        cur.close()
        return doctors
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return []
    finally:
        if conn is not None:
            conn.close()

def format_doctor_info(doctor_tuple):
    """Format doctor information for display"""
    if len(doctor_tuple) == 7:  # With hospital name
        doctor_id, name, specialization, experience, rating, hospital_name, consultation_fee = doctor_tuple
        return f"{name} ({specialization}) - {experience} yrs experience, {float(rating)}★ rating, ${float(consultation_fee)} consultation fee at {hospital_name}"
    else:  # Without hospital name
        doctor_id, name, specialization, experience, rating, hospital_id, consultation_fee = doctor_tuple
        return f"{name} ({specialization}) - {experience} yrs experience, {float(rating)}★ rating, ${float(consultation_fee)} consultation fee"

if __name__ == '__main__':
    doctors_list = get_all_doctors()
    if doctors_list:
        for doctor in doctors_list:
            print(doctor)
