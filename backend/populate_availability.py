"""
Add doctor availability to Neon DB
This populates the doctor_availability table with weekly schedules for all doctors
"""

from db import execute_query, get_db_cursor
import random
from datetime import time

def add_doctor_availability():
    """Add weekly availability schedules for all doctors"""
    
    print("🕐 Adding doctor availability schedules to Neon DB...")
    print("=" * 60)
    
    # Define time slots
    morning_slots = [
        (time(9, 0), time(12, 0)),   # Morning shift
    ]
    
    afternoon_slots = [
        (time(14, 0), time(17, 0)),  # Afternoon shift
    ]
    
    evening_slots = [
        (time(18, 0), time(21, 0)),  # Evening shift
    ]
    
    # Working days configuration by specialization
    specialization_schedules = {
        'Emergency Medicine': {
            'days': [0, 1, 2, 3, 4, 5, 6],  # All 7 days
            'shifts': ['morning', 'afternoon', 'evening']
        },
        'Family Medicine': {
            'days': [0, 1, 2, 3, 4, 5],  # Mon-Sat
            'shifts': ['morning', 'afternoon']
        },
        'Pediatrics': {
            'days': [0, 1, 2, 3, 4, 5],  # Mon-Sat
            'shifts': ['morning', 'afternoon']
        },
        'Cardiology': {
            'days': [0, 1, 2, 3, 4],  # Mon-Fri
            'shifts': ['morning', 'afternoon']
        },
        'General Surgery': {
            'days': [0, 1, 2, 3, 4, 5],  # Mon-Sat
            'shifts': ['morning', 'afternoon']
        },
        'default': {
            'days': [0, 1, 2, 3, 4],  # Mon-Fri
            'shifts': ['morning', 'afternoon']
        }
    }
    
    try:
        # Get all doctors
        doctors = execute_query("SELECT id, name, specialization FROM doctors ORDER BY id")
        print(f"Found {len(doctors)} doctors to schedule")
        
        added_count = 0
        
        with get_db_cursor() as cursor:
            for doctor in doctors:
                doctor_id = doctor['id']
                doctor_name = doctor['name']
                specialization = doctor['specialization']
                
                # Get schedule configuration for this specialization
                schedule_config = specialization_schedules.get(
                    specialization, 
                    specialization_schedules['default']
                )
                
                working_days = schedule_config['days']
                available_shifts = schedule_config['shifts']
                
                # For each working day
                for day_of_week in working_days:
                    # Randomly select which shifts this doctor works on this day
                    num_shifts = random.randint(1, len(available_shifts))
                    selected_shifts = random.sample(available_shifts, num_shifts)
                    
                    for shift in selected_shifts:
                        if shift == 'morning':
                            start_time, end_time = morning_slots[0]
                        elif shift == 'afternoon':
                            start_time, end_time = afternoon_slots[0]
                        else:  # evening
                            start_time, end_time = evening_slots[0]
                        
                        try:
                            cursor.execute("""
                                INSERT INTO doctor_availability (
                                    doctor_id, day_of_week, start_time, end_time, is_available
                                ) VALUES (%s, %s, %s, %s, %s)
                                ON CONFLICT (doctor_id, day_of_week, start_time) 
                                DO UPDATE SET end_time = EXCLUDED.end_time
                            """, (doctor_id, day_of_week, start_time, end_time, True))
                            
                            added_count += 1
                            
                        except Exception as e:
                            print(f"  ✗ Error adding availability for {doctor_name}: {e}")
                
                if added_count % 50 == 0 and added_count > 0:
                    print(f"  ✓ Processed {added_count} availability slots...")
        
        print("=" * 60)
        print(f"✅ Successfully added {added_count} availability slots!")
        
        # Show summary
        print("\n📊 Availability Summary:")
        summary = execute_query("""
            SELECT 
                CASE day_of_week
                    WHEN 0 THEN 'Monday'
                    WHEN 1 THEN 'Tuesday'
                    WHEN 2 THEN 'Wednesday'
                    WHEN 3 THEN 'Thursday'
                    WHEN 4 THEN 'Friday'
                    WHEN 5 THEN 'Saturday'
                    WHEN 6 THEN 'Sunday'
                END as day_name,
                COUNT(*) as slot_count,
                COUNT(DISTINCT doctor_id) as doctor_count
            FROM doctor_availability
            GROUP BY day_of_week
            ORDER BY day_of_week
        """)
        
        for row in summary:
            print(f"   • {row['day_name']}: {row['slot_count']} slots ({row['doctor_count']} doctors)")
        
        # Show sample availability
        print("\n📋 Sample Doctor Schedules:")
        samples = execute_query("""
            SELECT 
                d.name,
                d.specialization,
                CASE da.day_of_week
                    WHEN 0 THEN 'Mon'
                    WHEN 1 THEN 'Tue'
                    WHEN 2 THEN 'Wed'
                    WHEN 3 THEN 'Thu'
                    WHEN 4 THEN 'Fri'
                    WHEN 5 THEN 'Sat'
                    WHEN 6 THEN 'Sun'
                END as day,
                da.start_time,
                da.end_time
            FROM doctors d
            JOIN doctor_availability da ON d.id = da.doctor_id
            ORDER BY d.id, da.day_of_week, da.start_time
            LIMIT 15
        """)
        
        current_doctor = None
        for row in samples:
            if current_doctor != row['name']:
                if current_doctor is not None:
                    print()
                current_doctor = row['name']
                print(f"\n   {row['name']} ({row['specialization']}):")
            print(f"      {row['day']}: {row['start_time']} - {row['end_time']}")
        
        print("\n🎉 Doctor availability setup complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise

if __name__ == '__main__':
    add_doctor_availability()
