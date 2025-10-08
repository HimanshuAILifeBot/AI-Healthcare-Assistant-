"""
Test sp_get_specialists stored procedure
"""
from db import get_db_connection

def test_sp_get_specialists():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Test with fever
    print("Testing with symptom: fever")
    cur.execute("SELECT * FROM sp_get_specialists(ARRAY['fever'])")
    results = cur.fetchall()
    print(f"Results: {results}")
    
    # Test with multiple symptoms
    print("\nTesting with symptoms: fever, headache, chest pain")
    cur.execute("SELECT * FROM sp_get_specialists(ARRAY['fever', 'headache', 'chest pain'])")
    results = cur.fetchall()
    print(f"Results: {results}")
    
    # Now test if we have doctors with those specializations
    print("\n" + "="*60)
    print("Checking available doctor specializations:")
    cur.execute("SELECT DISTINCT specialization FROM doctors ORDER BY specialization")
    specializations = cur.fetchall()
    print("Available specializations in database:")
    for spec in specializations:
        print(f"  - {spec[0]}")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    test_sp_get_specialists()
