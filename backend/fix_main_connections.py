"""
Script to fix all database connection issues in main.py
Replace old conn.cursor() pattern with get_db_cursor() context manager
"""

import re

def fix_main_py():
    with open('/Users/himanshujha/PycharmProjects/Healthcare voice agent /Healthcare-voice-agent/backend/main.py', 'r') as f:
        content = f.read()
    
    # Pattern 1: Fix patient-details endpoint
    old_pattern_1 = r'''@app\.get\("/patient-details/\{user_id\}", response_model=PatientDetailsResponse\)
def get_patient_details\(user_id: int\):
    logger\.info\(f"Fetching patient details for user_id=\{user_id\}"\)
    cur = conn\.cursor\(\)
    try:
        cur\.execute\("SELECT \* FROM sp_get_patient_details\(%s\);", \(user_id,\)\)
        row = cur\.fetchone\(\)
        logger\.info\(f"Fetched row: \{row\}"\)
        cur\.close\(\)
    except Exception as e:
        logger\.error\(f"DB error in patient-details: \{e\}"\)
        conn\.rollback\(\)
        cur\.close\(\)
        raise HTTPException\(status_code=500, detail=f"Database error: \{e\}"\)
    if row:
        return jsonable_encoder\(\{
            "name": row\[0\], "date_of_birth": row\[1\], "gender": row\[2\], "contact_number": row\[3\],
            "medical_record_number": row\[4\], "blood_group": row\[5\], "marital_status": row\[6\], "id": row\[7\]
        \}\)
    raise HTTPException\(status_code=404, detail="Patient not found"\)'''
    
    new_pattern_1 = '''@app.get("/patient-details/{user_id}", response_model=PatientDetailsResponse)
def get_patient_details(user_id: int):
    logger.info(f"Fetching patient details for user_id={user_id}")
    try:
        with get_db_cursor() as cur:
            cur.execute("SELECT * FROM sp_get_patient_details(%s);", (user_id,))
            row = cur.fetchone()
            logger.info(f"Fetched row: {row}")
            
            if row:
                return jsonable_encoder({
                    "name": row[0], "date_of_birth": row[1], "gender": row[2], "contact_number": row[3],
                    "medical_record_number": row[4], "blood_group": row[5], "marital_status": row[6], "id": row[7]
                })
            raise HTTPException(status_code=404, detail="Patient not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"DB error in patient-details: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")'''
    
    content = re.sub(old_pattern_1, new_pattern_1, content, flags=re.DOTALL)
    
    # Save fixed content
    with open('/Users/himanshujha/PycharmProjects/Healthcare voice agent /Healthcare-voice-agent/backend/main_fixed.py', 'w') as f:
        f.write(content)
    
    print("Fixed version saved to main_fixed.py")
    print("Review and then: mv main_fixed.py main.py")

if __name__ == '__main__':
    fix_main_py()
