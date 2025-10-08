import psycopg2
import random
from datetime import datetime, timedelta, time
from config import Config

def add_availability_slots():
    """Add availability slots for all doctors without existing slots"""
    
    # Define working hours and days
    working_days = [0, 1, 2, 3, 4, 5]  # Monday to Saturday (0=Monday, 6=Sunday)
    morning_slots = [
        (time(9, 0), time(9, 30)),
        (time(9, 30), time(10, 0)),
        (time(10, 0), time(10, 30)),
        (time(10, 30), time(11, 0)),
        (time(11, 0), time(11, 30)),
        (time(11, 30), time(12, 0))
    ]
    
    afternoon_slots = [
        (time(14, 0), time(14, 30)),
        (time(14, 30), time(15, 0)),
        (time(15, 0), time(15, 30)),
        (time(15, 30), time(16, 0)),
        (time(16, 0), time(16, 30)),
        (time(16, 30), time(17, 0)),
        (time(17, 0), time(17, 30)),
        (time(17, 30), time(18, 0))
    ]
    
    evening_slots = [
        (time(18, 30), time(19, 0)),
        (time(19, 0), time(19, 30)),
        (time(19, 30), time(20, 0)),
        (time(20, 0), time(20, 30))
    ]
    
    all_time_slots = morning_slots + afternoon_slots + evening_slots
    
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
        
        # Get doctors without availability slots
        cur.execute('''
            SELECT d.id, d.name, d.specialization
            FROM doctors d
            LEFT JOIN availability_slots a ON d.id = a.doctor_id
            WHERE a.id IS NULL
        ''')
        doctors_without_slots = cur.fetchall()
        
        print(f"Found {len(doctors_without_slots)} doctors without availability slots")
        
        # Generate availability for the next 30 days
        start_date = datetime.now().date()
        total_slots_added = 0
        
        for doctor_id, doctor_name, specialization in doctors_without_slots:
            doctor_slots_added = 0
            
            # Generate slots for the next 30 days
            for day_offset in range(30):
                current_date = start_date + timedelta(days=day_offset)
                
                # Skip Sundays for most doctors (except Emergency Medicine)
                if current_date.weekday() == 6 and specialization != 'Emergency Medicine':
                    continue
                
                # Determine number of slots based on specialization
                if specialization in ['Emergency Medicine']:
                    # Emergency doctors work more hours
                    num_slots = random.randint(10, 18)
                    available_slots = all_time_slots
                elif specialization in ['Family Medicine', 'Pediatrics', 'General Surgery']:
                    # High-demand specialties get more slots
                    num_slots = random.randint(8, 12)
                    available_slots = morning_slots + afternoon_slots
                elif specialization in ['Cardiology', 'Neurology', 'Oncology']:
                    # Specialist consultations - moderate slots
                    num_slots = random.randint(6, 10)
                    available_slots = morning_slots + afternoon_slots
                else:
                    # Regular specialties
                    num_slots = random.randint(4, 8)
                    # Some doctors work evenings
                    if random.random() < 0.3:  # 30% chance of evening slots
                        available_slots = morning_slots + afternoon_slots + evening_slots
                    else:
                        available_slots = morning_slots + afternoon_slots
                
                # Randomly select time slots for this day
                selected_slots = random.sample(available_slots, min(num_slots, len(available_slots)))
                
                # Insert availability slots
                for start_time, end_time in selected_slots:
                    try:
                        cur.execute('''
                            INSERT INTO availability_slots (doctor_id, available_date, start_time, end_time)
                            VALUES (%s, %s, %s, %s)
                        ''', (doctor_id, current_date, start_time, end_time))
                        doctor_slots_added += 1
                        total_slots_added += 1
                    except Exception as e:
                        print(f"Error adding slot for {doctor_name}: {e}")
            
            if doctor_slots_added > 0:
                print(f"Added {doctor_slots_added} slots for {doctor_name} ({specialization})")
        
        conn.commit()
        cur.close()
        print(f"\nSuccessfully added {total_slots_added} availability slots for {len(doctors_without_slots)} doctors!")
        
        # Verify the results
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM availability_slots')
        total_slots_now = cur.fetchone()[0]
        print(f"Total availability slots in database: {total_slots_now}")
        
        # Show sample availability
        print("\n=== SAMPLE AVAILABILITY ADDED ===")
        cur.execute('''
            SELECT d.name, d.specialization, a.available_date, a.start_time, a.end_time
            FROM doctors d
            JOIN availability_slots a ON d.id = a.doctor_id
            WHERE a.available_date >= CURRENT_DATE
            ORDER BY d.name, a.available_date, a.start_time
            LIMIT 10
        ''')
        sample_slots = cur.fetchall()
        
        for slot in sample_slots:
            name, spec, date, start, end = slot
            print(f"{name} ({spec}) - {date} from {start} to {end}")
        
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        if conn:
            conn.rollback()
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    add_availability_slots()