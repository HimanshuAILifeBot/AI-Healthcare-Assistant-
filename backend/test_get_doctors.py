"""
Test sp_get_doctors_by_specialists with array input
"""
from db import get_db_connection

def test_get_doctors_by_specialists():
    conn = get_db_connection()
    cur = conn.cursor()
    
    print("Testing sp_get_doctors_by_specialists with array input")
    print("=" * 60)
    
    # Test with single specialization
    print("\n1️⃣ Testing with single specialization: ['Family Medicine']")
    cur.execute("SELECT * FROM sp_get_doctors_by_specialists(ARRAY['Family Medicine'])")
    doctors = cur.fetchall()
    print(f"   Found {len(doctors)} doctors:")
    for doc in doctors:
        print(f"   - ID: {doc[0]}, Name: {doc[1]}, Specialization: {doc[2]}, Experience: {doc[3]}yr, Rating: {doc[4]}")
    
    # Test with multiple specializations
    print("\n2️⃣ Testing with multiple specializations: ['Cardiology', 'Neurology']")
    cur.execute("SELECT * FROM sp_get_doctors_by_specialists(ARRAY['Cardiology', 'Neurology'])")
    doctors = cur.fetchall()
    print(f"   Found {len(doctors)} doctors:")
    for doc in doctors[:5]:  # Show first 5
        print(f"   - ID: {doc[0]}, Name: {doc[1]}, Specialization: {doc[2]}, Experience: {doc[3]}yr, Rating: {doc[4]}")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    test_get_doctors_by_specialists()
