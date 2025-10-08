"""
Drop and recreate sp_get_doctors_by_specialists with correct return type
"""
from db import execute_query

def update_procedure():
    print("Dropping old sp_get_doctors_by_specialists...")
    try:
        execute_query("DROP FUNCTION IF EXISTS sp_get_doctors_by_specialists(TEXT[])", fetch=False)
        print("✅ Dropped old function")
    except Exception as e:
        print(f"⚠️  Error dropping: {e}")
    
    print("\nCreating new sp_get_doctors_by_specialists...")
    procedure_sql = """
        CREATE OR REPLACE FUNCTION sp_get_doctors_by_specialists(p_specializations TEXT[])
        RETURNS TABLE(
            id INT,
            name VARCHAR,
            specialization VARCHAR,
            rating DECIMAL,
            fees DECIMAL,
            hospital VARCHAR,
            next_available_date DATE,
            start_time TIME,
            end_time TIME,
            slot_id INT
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT 
                d.id,
                d.name::VARCHAR,
                d.specialization::VARCHAR,
                d.rating,
                d.consultation_fee as fees,
                d.hospital::VARCHAR,
                (CURRENT_DATE + INTERVAL '1 day')::DATE as next_available_date,
                '09:00:00'::TIME as start_time,
                '17:00:00'::TIME as end_time,
                d.id as slot_id
            FROM doctors d
            WHERE d.specialization = ANY(p_specializations)
            AND d.available = TRUE
            ORDER BY d.rating DESC, d.specialization;
        END;
        $$ LANGUAGE plpgsql;
    """
    
    try:
        execute_query(procedure_sql, fetch=False)
        print("✅ Created new function with correct return type")
    except Exception as e:
        print(f"❌ Error creating: {e}")
    
    # Test it
    print("\nTesting new function...")
    try:
        result = execute_query("SELECT * FROM sp_get_doctors_by_specialists(ARRAY['Family Medicine']) LIMIT 1")
        if result:
            print(f"✅ Test successful! Sample result: {result[0]}")
        else:
            print("⚠️  No results returned")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    update_procedure()
