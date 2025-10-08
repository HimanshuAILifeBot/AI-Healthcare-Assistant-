"""
Create missing stored procedures for Neon DB
These procedures were not in the initial set but are needed by the application
"""

from db import execute_query

def create_missing_procedures():
    """Create sp_get_specialists and other missing procedures"""
    
    print("📝 Creating missing stored procedures for Neon DB...")
    print("=" * 60)
    
    procedures = []
    
    # 1. sp_get_specialists - Maps symptoms to specialist types
    # This is a simplified version that maps common symptoms to specializations
    procedures.append("""
        CREATE OR REPLACE FUNCTION sp_get_specialists(p_symptoms TEXT[])
        RETURNS TABLE(specialization VARCHAR) AS $$
        DECLARE
            symptom TEXT;
            found_specializations TEXT[];
        BEGIN
            -- Initialize empty array
            found_specializations := ARRAY[]::TEXT[];
            
            -- Loop through each symptom
            FOREACH symptom IN ARRAY p_symptoms
            LOOP
                -- Convert to lowercase for case-insensitive matching
                symptom := LOWER(TRIM(symptom));
                
                -- Map symptoms to specializations
                CASE 
                    -- Family Medicine / General / Fever related
                    WHEN symptom LIKE ANY(ARRAY['%fever%', '%temperature%', '%cold%', '%cough%', '%flu%', '%viral%']) THEN
                        IF NOT 'Family Medicine' = ANY(found_specializations) THEN
                            found_specializations := array_append(found_specializations, 'Family Medicine');
                        END IF;
                    
                    -- Cardiology
                    WHEN symptom LIKE ANY(ARRAY['%chest pain%', '%heart%', '%cardiac%', '%blood pressure%', '%bp%', '%hypertension%', '%palpitation%']) THEN
                        IF NOT 'Cardiology' = ANY(found_specializations) THEN
                            found_specializations := array_append(found_specializations, 'Cardiology');
                        END IF;
                    
                    -- Orthopedics
                    WHEN symptom LIKE ANY(ARRAY['%bone%', '%joint%', '%fracture%', '%back pain%', '%knee%', '%arthritis%', '%sprain%']) THEN
                        IF NOT 'Orthopedics' = ANY(found_specializations) THEN
                            found_specializations := array_append(found_specializations, 'Orthopedics');
                        END IF;
                    
                    -- Dermatology
                    WHEN symptom LIKE ANY(ARRAY['%skin%', '%rash%', '%acne%', '%itch%', '%allergy%']) THEN
                        IF NOT 'Dermatology' = ANY(found_specializations) THEN
                            found_specializations := array_append(found_specializations, 'Dermatology');
                        END IF;
                    
                    -- Pediatrics
                    WHEN symptom LIKE ANY(ARRAY['%child%', '%baby%', '%infant%', '%kid%']) THEN
                        IF NOT 'Pediatrics' = ANY(found_specializations) THEN
                            found_specializations := array_append(found_specializations, 'Pediatrics');
                        END IF;
                    
                    -- ENT (Ear, Nose, Throat)
                    WHEN symptom LIKE ANY(ARRAY['%ear%', '%nose%', '%throat%', '%sinus%', '%hearing%', '%tonsil%']) THEN
                        IF NOT 'ENT' = ANY(found_specializations) THEN
                            found_specializations := array_append(found_specializations, 'ENT');
                        END IF;
                    
                    -- Neurology
                    WHEN symptom LIKE ANY(ARRAY['%headache%', '%migraine%', '%seizure%', '%nerve%', '%brain%', '%paralysis%']) THEN
                        IF NOT 'Neurology' = ANY(found_specializations) THEN
                            found_specializations := array_append(found_specializations, 'Neurology');
                        END IF;
                    
                    -- Gastroenterology
                    WHEN symptom LIKE ANY(ARRAY['%stomach%', '%digestion%', '%diarrhea%', '%constipation%', '%gastric%', '%liver%', '%abdomen%']) THEN
                        IF NOT 'Gastroenterology' = ANY(found_specializations) THEN
                            found_specializations := array_append(found_specializations, 'Gastroenterology');
                        END IF;
                    
                    -- Ophthalmology
                    WHEN symptom LIKE ANY(ARRAY['%eye%', '%vision%', '%blind%', '%cataract%', '%sight%']) THEN
                        IF NOT 'Ophthalmology' = ANY(found_specializations) THEN
                            found_specializations := array_append(found_specializations, 'Ophthalmology');
                        END IF;
                    
                    -- Gynecology
                    WHEN symptom LIKE ANY(ARRAY['%pregnant%', '%menstrual%', '%period%', '%ovarian%', '%uterus%', '%pregnancy%']) THEN
                        IF NOT 'Gynecology' = ANY(found_specializations) THEN
                            found_specializations := array_append(found_specializations, 'Gynecology');
                        END IF;
                    
                    -- Psychiatry
                    WHEN symptom LIKE ANY(ARRAY['%depression%', '%anxiety%', '%mental%', '%stress%', '%mood%', '%insomnia%']) THEN
                        IF NOT 'Psychiatry' = ANY(found_specializations) THEN
                            found_specializations := array_append(found_specializations, 'Psychiatry');
                        END IF;
                    
                    -- Default: Family Medicine for unrecognized symptoms
                    ELSE
                        IF NOT 'Family Medicine' = ANY(found_specializations) THEN
                            found_specializations := array_append(found_specializations, 'Family Medicine');
                        END IF;
                END CASE;
            END LOOP;
            
            -- Return each specialization as a row
            RETURN QUERY
            SELECT unnest(found_specializations)::VARCHAR;
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
        AND routine_name = 'sp_get_specialists'
        ORDER BY routine_name
    """)
    
    if procedures_list:
        print("✅ Verified procedures in database:")
        for proc in procedures_list:
            print(f"   - {proc['routine_name']}")
    else:
        print("❌ No procedures found in verification")

if __name__ == "__main__":
    create_missing_procedures()
