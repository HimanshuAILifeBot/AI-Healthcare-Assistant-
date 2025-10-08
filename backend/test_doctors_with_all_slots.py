"""
Test sp_get_doctors_by_specialists with multiple time slots
"""
from db import get_db_connection

def test_doctors_with_slots():
    conn = get_db_connection()
    cur = conn.cursor()
    
    print("Testing sp_get_doctors_by_specialists for Family Medicine")
    print("=" * 80)
    
    cur.execute("SELECT * FROM sp_get_doctors_by_specialists(ARRAY['Family Medicine'])")
    results = cur.fetchall()
    
    print(f"\nTotal slots returned: {len(results)}")
    print("\nGrouped by doctor:")
    print("=" * 80)
    
    current_doctor = None
    slot_count = 0
    
    for row in results:
        if current_doctor != row[1]:  # New doctor
            if current_doctor is not None:
                print(f"   → Total slots: {slot_count}\n")
            current_doctor = row[1]
            slot_count = 0
            print(f"\n👨‍⚕️ {row[1]}")
            print(f"   Specialization: {row[2]}")
            print(f"   Rating: {row[3]} | Fees: ${row[4]} | Hospital: {row[5]}")
            print(f"   Available slots:")
        
        slot_count += 1
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_of_week = row[6].weekday()
        day_name = days[day_of_week]
        print(f"      {slot_count}. {row[6]} ({day_name}) | {row[7]} - {row[8]} | Slot ID: {row[9]}")
    
    if current_doctor is not None:
        print(f"   → Total slots: {slot_count}\n")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    test_doctors_with_slots()
