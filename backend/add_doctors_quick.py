"""
Quick script to add doctors to Neon DB using batch insert for better performance
"""

from db import get_db_cursor
import sys

def add_doctors_batch():
    """Add doctors using batch insert for faster performance"""
    
    # Hospital names
    hospitals = [
        'City General Hospital',
        'Saint Mary Medical Center', 
        'Metro Health Institute',
        'University Medical Center'
    ]
    
    # Doctors data: (name, specialization, experience, rating, hospital_idx)
    doctors_data = [
        # Cardiology
        ('Dr. Michael Chen', 'Cardiology', 15, 4.8, 0),
        ('Dr. Sarah Thompson', 'Cardiology', 12, 4.7, 1),
        ('Dr. Robert Kim', 'Cardiology', 20, 4.9, 2),
        ('Dr. Lisa Anderson', 'Cardiology', 8, 4.6, 3),
        ('Dr. Ahmed Hassan', 'Cardiology', 18, 4.8, 0),
        
        # Dermatology
        ('Dr. Emily Watson', 'Dermatology', 10, 4.7, 1),
        ('Dr. Carlos Rivera', 'Dermatology', 14, 4.8, 2),
        ('Dr. Jennifer Park', 'Dermatology', 7, 4.6, 3),
        ('Dr. Marcus Johnson', 'Dermatology', 16, 4.9, 0),
        
        # Neurology
        ('Dr. Rachel Miller', 'Neurology', 13, 4.8, 1),
        ('Dr. David Wilson', 'Neurology', 19, 4.9, 2),
        ('Dr. Priya Patel', 'Neurology', 11, 4.7, 3),
        ('Dr. Thomas Brown', 'Neurology', 22, 4.8, 0),
        
        # Orthopedics
        ('Dr. Kevin Martinez', 'Orthopedics', 17, 4.9, 1),
        ('Dr. Michelle Davis', 'Orthopedics', 9, 4.6, 2),
        ('Dr. Jason Lee', 'Orthopedics', 21, 4.8, 3),
        ('Dr. Amanda Rodriguez', 'Orthopedics', 12, 4.7, 0),
        ('Dr. Steven Clark', 'Orthopedics', 25, 4.9, 1),
        
        # Pediatrics
        ('Dr. Maria Gonzalez', 'Pediatrics', 8, 4.7, 2),
        ('Dr. Christopher White', 'Pediatrics', 14, 4.8, 3),
        ('Dr. Nicole Taylor', 'Pediatrics', 6, 4.6, 0),
        ('Dr. Benjamin Moore', 'Pediatrics', 11, 4.7, 1),
        ('Dr. Samantha Jackson', 'Pediatrics', 16, 4.9, 2),
    ]
    
    print("🏥 Adding doctors to Neon DB (Quick Batch Insert)...")
    print("=" * 60)
    
    try:
        with get_db_cursor() as cursor:
            # Prepare batch insert
            insert_query = """
                INSERT INTO doctors (
                    name, email, phone, specialization, qualification,
                    experience_years, consultation_fee, rating, available,
                    image_url, hospital, bio
                ) VALUES %s
                ON CONFLICT (email) DO NOTHING
            """
            
            # Prepare values
            values_list = []
            for idx, (name, specialization, experience, rating, hospital_idx) in enumerate(doctors_data):
                email = name.lower().replace('dr. ', '').replace(' ', '.') + '@healthcare.com'
                phone = f'+1-555-{1000 + idx:04d}'
                qualification = 'MD, Board Certified'
                consultation_fee = 100 + (experience * 5) + ((rating - 4.0) * 50)
                hospital = hospitals[hospital_idx % len(hospitals)]
                bio = f"Experienced {specialization} specialist with {experience} years of practice."
                image_url = f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&size=200"
                
                values_list.append((
                    name, email, phone, specialization, qualification,
                    experience, consultation_fee, rating, True,
                    image_url, hospital, bio
                ))
            
            # Use execute_values for batch insert
            from psycopg2.extras import execute_values
            execute_values(cursor, insert_query, values_list)
            
        print(f"✅ Successfully added {len(doctors_data)} doctors!")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    success = add_doctors_batch()
    sys.exit(0 if success else 1)
