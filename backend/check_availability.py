"""
Check doctor availability data
"""
from db import get_db_connection

def check_availability():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Check how many availability records we have
    cur.execute("SELECT COUNT(*) as count FROM doctor_availability")
    count = cur.fetchone()[0]
    print(f"Total availability records: {count}")
    
    if count > 0:
        # Show sample availability
        cur.execute("""
            SELECT da.id, da.doctor_id, d.name, da.day_of_week, da.start_time, da.end_time, da.is_available
            FROM doctor_availability da
            JOIN doctors d ON da.doctor_id = d.id
            ORDER BY da.doctor_id, da.day_of_week, da.start_time
            LIMIT 20
        """)
        
        records = cur.fetchall()
        print("\nSample availability records:")
        print("=" * 80)
        for r in records:
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_name = days[r[3]] if r[3] < 7 else 'Unknown'
            print(f"Dr. {r[2]:<25} | {day_name:<10} | {r[4]} - {r[5]} | Available: {r[6]}")
    
    # Check how many doctors have availability
    cur.execute("""
        SELECT COUNT(DISTINCT doctor_id) as count 
        FROM doctor_availability
    """)
    docs_with_avail = cur.fetchone()[0]
    print(f"\nDoctors with availability records: {docs_with_avail}")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    check_availability()
