import psycopg2
import random
from config import Config

def update_consultation_fees():
    # Define base consultation fees by specialization (in USD)
    specialization_fees = {
        'Emergency Medicine': (150, 250),
        'General Surgery': (200, 350),
        'Cardiology': (180, 300),
        'Neurology': (170, 280),
        'Oncology': (200, 320),
        'Orthopedics': (160, 270),
        'Dermatology': (120, 200),
        'Pediatrics': (100, 180),
        'Psychiatry': (140, 220),
        'Ophthalmology': (130, 210),
        'Otolaryngology': (140, 230),
        'Urology': (150, 240),
        'Gastroenterology': (160, 260),
        'Pulmonology': (150, 240),
        'Endocrinology': (140, 230),
        'Rheumatology': (150, 250),
        'Nephrology': (160, 270),
        'Hematology': (170, 280),
        'Infectious Disease': (150, 240),
        'Allergist/Immunologist': (130, 210),
        'Anesthesiology': (200, 300),
        'Radiology': (180, 280),
        'Pathology': (160, 250),
        'Physical Medicine & Rehabilitation': (140, 220),
        'Plastic Surgery': (250, 400),
        'Family Medicine': (80, 150),
        'Geriatrics': (120, 180),
        'Obstetrics and Gynecology': (150, 250)
    }

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
        
        # Get all doctors
        cur.execute("SELECT id, name, specialization, experience, rating FROM doctors")
        doctors = cur.fetchall()
        
        updated_count = 0
        
        for doctor in doctors:
            doctor_id, name, specialization, experience, rating = doctor
            
            # Get base fee range for specialization
            if specialization in specialization_fees:
                min_fee, max_fee = specialization_fees[specialization]
            else:
                # Default range for unknown specializations
                min_fee, max_fee = (120, 200)
            
            # Calculate base fee within the range
            base_fee = random.randint(min_fee, max_fee)
            
            # Adjust fee based on experience (more experience = higher fee)
            experience_multiplier = 1.0
            if experience >= 20:
                experience_multiplier = 1.3
            elif experience >= 15:
                experience_multiplier = 1.2
            elif experience >= 10:
                experience_multiplier = 1.1
            elif experience >= 5:
                experience_multiplier = 1.0
            else:
                experience_multiplier = 0.9
            
            # Adjust fee based on rating (higher rating = higher fee)
            rating_multiplier = 1.0
            if rating >= 4.8:
                rating_multiplier = 1.2
            elif rating >= 4.7:
                rating_multiplier = 1.1
            elif rating >= 4.6:
                rating_multiplier = 1.0
            else:
                rating_multiplier = 0.95
            
            # Calculate final consultation fee
            final_fee = base_fee * experience_multiplier * rating_multiplier
            
            # Round to nearest 5 (make it look more realistic)
            final_fee = round(final_fee / 5) * 5
            
            # Ensure minimum fee of $50
            final_fee = max(final_fee, 50)
            
            # Update the doctor's consultation fee
            cur.execute(
                "UPDATE doctors SET consultation_fee = %s WHERE id = %s",
                (final_fee, doctor_id)
            )
            updated_count += 1
        
        conn.commit()
        cur.close()
        print(f"Successfully updated consultation fees for {updated_count} doctors.")
        
        # Show some sample updated records
        cur = conn.cursor()
        cur.execute("""
            SELECT name, specialization, experience, rating, consultation_fee 
            FROM doctors 
            ORDER BY consultation_fee DESC 
            LIMIT 10
        """)
        top_fee_doctors = cur.fetchall()
        
        print("\n=== TOP 10 HIGHEST CONSULTATION FEES ===")
        for doctor in top_fee_doctors:
            print(f"{doctor[0]} ({doctor[1]}) - {doctor[2]} yrs exp, {doctor[3]} rating: ${doctor[4]}")
        
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        if conn:
            conn.rollback()
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    update_consultation_fees()