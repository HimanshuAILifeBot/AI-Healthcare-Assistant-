"""
List all patients in database
"""
from db import get_db_connection
from psycopg2.extras import RealDictCursor

def list_patients():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Count total patients
    cur.execute("SELECT COUNT(*) as count FROM patients")
    count = cur.fetchone()['count']
    print(f"📊 Total patients in database: {count}")
    
    if count > 0:
        # Show all patients
        cur.execute("""
            SELECT id, name, email, phone, date_of_birth, gender, blood_group, created_at
            FROM patients 
            ORDER BY created_at DESC
            LIMIT 10
        """)
        
        patients = cur.fetchall()
        print("\n" + "="*80)
        print("Recent patients:")
        print("="*80)
        for p in patients:
            print(f"ID: {p['id']} | Name: {p['name']} | Email: {p['email']}")
            print(f"   Phone: {p['phone']} | DOB: {p['date_of_birth']} | Gender: {p['gender']}")
            print(f"   Blood Group: {p['blood_group']} | Created: {p['created_at']}")
            print("-" * 80)
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    list_patients()
