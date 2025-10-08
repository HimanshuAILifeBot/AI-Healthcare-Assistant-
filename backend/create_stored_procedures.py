"""
Create stored procedures for Neon DB
Adapted from the original SQL functions to work with the new schema
"""

from db import execute_query

def create_stored_procedures():
    """Create all necessary stored procedures for the application"""
    
    print("📝 Creating stored procedures for Neon DB...")
    print("=" * 60)
    
    procedures = []
    
    # 1. Login function - adapted for new schema (no separate users table)
    procedures.append("""
        CREATE OR REPLACE FUNCTION sp_login_user(p_email TEXT, p_password TEXT)
        RETURNS TABLE(
            id INT,
            email VARCHAR,
            password VARCHAR
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT p.id, p.email::VARCHAR, p.password_hash::VARCHAR
            FROM patients p
            WHERE p.email = p_email AND p.password_hash = p_password;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # 2. Get patient details - adapted for new schema
    procedures.append("""
        CREATE OR REPLACE FUNCTION sp_get_patient_details(p_user_id INT)
        RETURNS TABLE(
            name TEXT,
            date_of_birth DATE,
            gender TEXT,
            contact_number TEXT,
            medical_record_number TEXT,
            blood_group TEXT,
            marital_status TEXT,
            id INT
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT 
                p.name::TEXT,
                p.date_of_birth,
                p.gender::TEXT,
                p.phone::TEXT as contact_number,
                'MRN' || LPAD(p.id::TEXT, 6, '0') as medical_record_number,
                p.blood_group::TEXT,
                'Single'::TEXT as marital_status,  -- Default value
                p.id
            FROM patients p
            WHERE p.id = p_user_id;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # 3. Get patient ID - simple version
    procedures.append("""
        CREATE OR REPLACE FUNCTION sp_get_patient_id(p_user_id INT)
        RETURNS TABLE(id INT) AS $$
        BEGIN
            RETURN QUERY
            SELECT p.id
            FROM patients p
            WHERE p.id = p_user_id;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # 4. Get medical history - adapted for new schema
    procedures.append("""
        CREATE OR REPLACE FUNCTION sp_get_medical_history(p_patient_id INT)
        RETURNS TABLE(
            past_diagnoses TEXT,
            surgeries TEXT,
            hospital_admissions TEXT,
            immunization_records TEXT,
            family_medical_history TEXT,
            lifestyle_factors TEXT
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT 
                mr.description as past_diagnoses,
                ''::TEXT as surgeries,
                ''::TEXT as hospital_admissions,
                ''::TEXT as immunization_records,
                ''::TEXT as family_medical_history,
                ''::TEXT as lifestyle_factors
            FROM medical_records mr
            WHERE mr.patient_id = p_patient_id
            LIMIT 1;
            
            -- If no records found, return empty row
            IF NOT FOUND THEN
                RETURN QUERY
                SELECT 
                    ''::TEXT, ''::TEXT, ''::TEXT, 
                    ''::TEXT, ''::TEXT, ''::TEXT;
            END IF;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # 5. Get doctors by specialist (accepts array of specializations)
    procedures.append("""
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
                (CURRENT_DATE + INTERVAL '1 day')::DATE as next_available_date,  -- Tomorrow
                '09:00:00'::TIME as start_time,  -- Default morning slot
                '17:00:00'::TIME as end_time,    -- Default evening slot
                d.id as slot_id  -- Use doctor ID as temporary slot_id
            FROM doctors d
            WHERE d.specialization = ANY(p_specializations)
            AND d.available = TRUE
            ORDER BY d.rating DESC, d.specialization;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # 6. Create appointment
    procedures.append("""
        CREATE OR REPLACE FUNCTION sp_create_appointment(
            p_patient_id INT,
            p_doctor_id INT,
            p_appointment_date DATE,
            p_appointment_time TIME,
            p_symptoms TEXT
        )
        RETURNS TABLE(appointment_id INT) AS $$
        DECLARE
            v_appointment_id INT;
        BEGIN
            INSERT INTO appointments (
                patient_id, doctor_id, appointment_date, 
                appointment_time, symptoms, status, payment_status
            )
            VALUES (
                p_patient_id, p_doctor_id, p_appointment_date,
                p_appointment_time, p_symptoms, 'scheduled', 'pending'
            )
            RETURNING id INTO v_appointment_id;
            
            RETURN QUERY SELECT v_appointment_id;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    # Execute each procedure
    success_count = 0
    for i, proc_sql in enumerate(procedures, 1):
        try:
            execute_query(proc_sql, fetch=False)
            print(f"✅ Created procedure {i}/{len(procedures)}")
            success_count += 1
        except Exception as e:
            print(f"❌ Error creating procedure {i}: {e}")
    
    print("=" * 60)
    print(f"✅ Successfully created {success_count}/{len(procedures)} stored procedures!")
    
    # Verify procedures were created
    print("\n📋 Verifying procedures...")
    procedures_list = execute_query("""
        SELECT routine_name 
        FROM information_schema.routines 
        WHERE routine_schema = 'public' 
        AND routine_type = 'FUNCTION'
        AND routine_name LIKE 'sp_%'
        ORDER BY routine_name
    """)
    
    print("\n✅ Available stored procedures:")
    for proc in procedures_list:
        print(f"   • {proc['routine_name']}")
    
    print("\n🎉 Stored procedures setup complete!")

if __name__ == '__main__':
    create_stored_procedures()
