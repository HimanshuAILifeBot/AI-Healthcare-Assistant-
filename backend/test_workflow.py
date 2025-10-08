"""
Test the full workflow: symptoms -> specialists -> doctors
"""
from db import get_db_connection

def test_full_workflow():
    conn = get_db_connection()
    cur = conn.cursor()
    
    print("=" * 60)
    print("Testing full workflow: fever -> specialists -> doctors")
    print("=" * 60)
    
    # Step 1: Get specialists for fever
    print("\n1️⃣ Getting specialists for symptom: fever")
    cur.execute("SELECT * FROM sp_get_specialists(ARRAY['fever'])")
    specialists = cur.fetchall()
    print(f"   Specialists: {[s[0] for s in specialists]}")
    
    # Step 2: Get doctors for each specialist
    for specialist in specialists:
        specialization = specialist[0]
        print(f"\n2️⃣ Getting doctors for specialization: {specialization}")
        cur.execute("SELECT * FROM sp_get_doctors_by_specialists(%s)", (specialization,))
        doctors = cur.fetchall()
        print(f"   Found {len(doctors)} doctors")
        if doctors:
            for doc in doctors[:3]:  # Show first 3
                print(f"   - Dr. {doc[1]} (ID: {doc[0]})")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    test_full_workflow()
