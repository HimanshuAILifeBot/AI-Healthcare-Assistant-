"""
Simple script to add doctors to Neon DB - adds all doctors from add_doctors.py
"""

from db import execute_query
import time

def add_all_doctors():
    """Add all doctors to Neon DB"""
    
    hospitals = ['City General Hospital', 'Saint Mary Medical Center', 'Metro Health Institute', 'University Medical Center']
    
    # All doctors with (name, specialization, experience, rating, hospital_idx)
    all_doctors = [
        ('Dr. Michael Chen', 'Cardiology', 15, 4.8, 0), ('Dr. Sarah Thompson', 'Cardiology', 12, 4.7, 1),
        ('Dr. Robert Kim', 'Cardiology', 20, 4.9, 2), ('Dr. Lisa Anderson', 'Cardiology', 8, 4.6, 3),
        ('Dr. Ahmed Hassan', 'Cardiology', 18, 4.8, 0), ('Dr. Emily Watson', 'Dermatology', 10, 4.7, 1),
        ('Dr. Carlos Rivera', 'Dermatology', 14, 4.8, 2), ('Dr. Jennifer Park', 'Dermatology', 7, 4.6, 3),
        ('Dr. Marcus Johnson', 'Dermatology', 16, 4.9, 0), ('Dr. Rachel Miller', 'Neurology', 13, 4.8, 1),
        ('Dr. David Wilson', 'Neurology', 19, 4.9, 2), ('Dr. Priya Patel', 'Neurology', 11, 4.7, 3),
        ('Dr. Thomas Brown', 'Neurology', 22, 4.8, 0), ('Dr. Kevin Martinez', 'Orthopedics', 17, 4.9, 1),
        ('Dr. Michelle Davis', 'Orthopedics', 9, 4.6, 2), ('Dr. Jason Lee', 'Orthopedics', 21, 4.8, 3),
        ('Dr. Amanda Rodriguez', 'Orthopedics', 12, 4.7, 0), ('Dr. Steven Clark', 'Orthopedics', 25, 4.9, 1),
        ('Dr. Maria Gonzalez', 'Pediatrics', 8, 4.7, 2), ('Dr. Christopher White', 'Pediatrics', 14, 4.8, 3),
        ('Dr. Nicole Taylor', 'Pediatrics', 6, 4.6, 0), ('Dr. Benjamin Moore', 'Pediatrics', 11, 4.7, 1),
        ('Dr. Samantha Jackson', 'Pediatrics', 16, 4.9, 2), ('Dr. Antonio Garcia', 'Gastroenterology', 13, 4.8, 3),
        ('Dr. Helen Cooper', 'Gastroenterology', 18, 4.9, 0), ('Dr. Ryan Phillips', 'Gastroenterology', 10, 4.6, 1),
        ('Dr. Natalie Evans', 'Gastroenterology', 15, 4.7, 2), ('Dr. Alexander Turner', 'Oncology', 20, 4.9, 3),
        ('Dr. Victoria Hall', 'Oncology', 16, 4.8, 0), ('Dr. Gabriel Santos', 'Oncology', 12, 4.7, 1),
        ('Dr. Catherine Wright', 'Oncology', 24, 4.9, 2), ('Dr. Daniel Kim', 'Psychiatry', 11, 4.7, 3),
        ('Dr. Rebecca Foster', 'Psychiatry', 14, 4.8, 0), ('Dr. Luis Rodriguez', 'Psychiatry', 9, 4.6, 1),
        ('Dr. Ashley Chen', 'Psychiatry', 17, 4.8, 2), ('Dr. Peter Williams', 'Psychiatry', 13, 4.7, 3),
        ('Dr. Jonathan Bell', 'Urology', 16, 4.8, 0), ('Dr. Diana Murphy', 'Urology', 12, 4.7, 1),
        ('Dr. Eric Thompson', 'Urology', 19, 4.9, 2), ('Dr. Stephanie Cook', 'Urology', 8, 4.6, 3),
        ('Dr. Matthew Baker', 'Ophthalmology', 14, 4.8, 0), ('Dr. Jennifer Adams', 'Ophthalmology', 10, 4.7, 1),
        ('Dr. Richard Green', 'Ophthalmology', 18, 4.9, 2), ('Dr. Laura Mitchell', 'Ophthalmology', 7, 4.6, 3),
        ('Dr. Paul Nelson', 'Otolaryngology', 15, 4.8, 0), ('Dr. Karen Scott', 'Otolaryngology', 11, 4.7, 1),
        ('Dr. Andrew Carter', 'Otolaryngology', 20, 4.9, 2), ('Dr. Monica Perez', 'Otolaryngology', 9, 4.6, 3),
        ('Dr. Charles Roberts', 'Pulmonology', 17, 4.8, 0), ('Dr. Angela Collins', 'Pulmonology', 13, 4.7, 1),
        ('Dr. Frank Edwards', 'Pulmonology', 22, 4.9, 2), ('Dr. Melissa Stewart', 'Pulmonology', 8, 4.6, 3),
        ('Dr. Joseph Morris', 'Endocrinology', 12, 4.7, 0), ('Dr. Christina Reed', 'Endocrinology', 16, 4.8, 1),
        ('Dr. Mark Bailey', 'Endocrinology', 9, 4.6, 2), ('Dr. Sandra Rivera', 'Endocrinology', 14, 4.8, 3),
        ('Dr. Gregory Cooper', 'Rheumatology', 18, 4.9, 0), ('Dr. Deborah Hughes', 'Rheumatology', 11, 4.7, 1),
        ('Dr. Carl Peterson', 'Rheumatology', 15, 4.8, 2), ('Dr. Janet Price', 'Rheumatology', 13, 4.7, 3),
        ('Dr. Wayne Barnes', 'Nephrology', 19, 4.9, 0), ('Dr. Theresa Kelly', 'Nephrology', 10, 4.6, 1),
        ('Dr. Eugene Howard', 'Nephrology', 16, 4.8, 2), ('Dr. Jacqueline Ward', 'Nephrology', 12, 4.7, 3),
        ('Dr. Ralph Torres', 'Allergist/Immunologist', 14, 4.8, 0), ('Dr. Frances Wood', 'Allergist/Immunologist', 8, 4.6, 1),
        ('Dr. Harold Watson', 'Allergist/Immunologist', 17, 4.9, 2), ('Dr. Denise Brooks', 'Allergist/Immunologist', 11, 4.7, 3),
        ('Dr. Arthur Bennett', 'General Surgery', 20, 4.9, 0), ('Dr. Gloria Gray', 'General Surgery', 15, 4.8, 1),
        ('Dr. Lawrence James', 'General Surgery', 25, 4.9, 2), ('Dr. Teresa Ross', 'General Surgery', 12, 4.7, 3),
        ('Dr. Philip Henderson', 'General Surgery', 18, 4.8, 0), ('Dr. Roger Butler', 'Infectious Disease', 16, 4.8, 1),
        ('Dr. Judith Powell', 'Infectious Disease', 13, 4.7, 2), ('Dr. Gerald Jenkins', 'Infectious Disease', 21, 4.9, 3),
        ('Dr. Marie Perry', 'Infectious Disease', 9, 4.6, 0), ('Dr. Harold Russell', 'Hematology', 17, 4.8, 1),
        ('Dr. Shirley Griffin', 'Hematology', 14, 4.7, 2), ('Dr. Albert Washington', 'Hematology', 19, 4.9, 3),
        ('Dr. Ruby Diaz', 'Hematology', 10, 4.6, 0), ('Dr. Eugene Butler', 'Geriatrics', 23, 4.9, 1),
        ('Dr. Phyllis Hayes', 'Geriatrics', 18, 4.8, 2), ('Dr. Leonard Myers', 'Geriatrics', 26, 4.9, 3),
        ('Dr. Beverly Ford', 'Geriatrics', 15, 4.7, 0), ('Dr. Norman Hamilton', 'Plastic Surgery', 12, 4.7, 1),
        ('Dr. Kathleen Graham', 'Plastic Surgery', 8, 4.6, 2), ('Dr. Douglas Sullivan', 'Plastic Surgery', 16, 4.8, 3),
        ('Dr. Ann Wallace', 'Plastic Surgery', 14, 4.8, 0), ('Dr. Jesse Freeman', 'Family Medicine', 11, 4.7, 1),
        ('Dr. Joan Wells', 'Family Medicine', 15, 4.8, 2), ('Dr. Billy Woods', 'Family Medicine', 7, 4.6, 3),
        ('Dr. Dorothy West', 'Family Medicine', 19, 4.9, 0), ('Dr. Victor Chapman', 'Family Medicine', 13, 4.7, 1),
        ('Dr. Craig Mason', 'Anesthesiology', 16, 4.8, 2), ('Dr. Marilyn Hunt', 'Anesthesiology', 12, 4.7, 3),
        ('Dr. Tony Black', 'Anesthesiology', 20, 4.9, 0), ('Dr. Julie Gibson', 'Anesthesiology', 9, 4.6, 1),
        ('Dr. Eugene Kennedy', 'Radiology', 18, 4.8, 2), ('Dr. Cheryl Hawkins', 'Radiology', 14, 4.7, 3),
        ('Dr. Keith Hansen', 'Radiology', 22, 4.9, 0), ('Dr. Alice Pierce', 'Radiology', 10, 4.6, 1),
        ('Dr. Todd George', 'Physical Medicine & Rehabilitation', 13, 4.7, 2), ('Dr. Evelyn Stone', 'Physical Medicine & Rehabilitation', 17, 4.8, 3),
        ('Dr. Curtis Knight', 'Physical Medicine & Rehabilitation', 11, 4.7, 0), ('Dr. Brenda Fox', 'Physical Medicine & Rehabilitation', 15, 4.8, 1),
        ('Dr. Ivan Mills', 'Emergency Medicine', 12, 4.7, 0), ('Dr. Paula Lane', 'Emergency Medicine', 8, 4.8, 1),
        ('Dr. Roy Boyd', 'Emergency Medicine', 15, 4.9, 2), ('Dr. Irene Arnold', 'Emergency Medicine', 10, 4.6, 3),
        ('Dr. Louis Reid', 'Pathology', 20, 4.8, 0), ('Dr. Donna Fleming', 'Pathology', 16, 4.7, 1),
        ('Dr. Willie Hunter', 'Pathology', 24, 4.9, 2), ('Dr. Lois Mason', 'Pathology', 11, 4.6, 3),
        ('Dr. Bobby Porter', 'Obstetrics and Gynecology', 14, 4.8, 0), ('Dr. Martha Fisher', 'Obstetrics and Gynecology', 18, 4.9, 1),
        ('Dr. Ralph Palmer', 'Obstetrics and Gynecology', 9, 4.6, 2), ('Dr. Gloria Fuller', 'Obstetrics and Gynecology', 13, 4.7, 3)
    ]
    
    print(f"🏥 Adding {len(all_doctors)} doctors to Neon DB...")
    start_time = time.time()
    
    added_count = 0
    for idx, (name, specialization, experience, rating, hospital_idx) in enumerate(all_doctors, 1):
        try:
            email = name.lower().replace('dr. ', '').replace(' ', '.') + '@healthcare.com'
            phone = f'+1-555-{1000 + idx:04d}'
            qualification = 'MD, Board Certified'
            consultation_fee = round(100 + (experience * 5) + ((rating - 4.0) * 50), 2)
            hospital = hospitals[hospital_idx % len(hospitals)]
            bio = f"Experienced {specialization} specialist with {experience} years of practice at {hospital}."
            image_url = f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&size=200"
            
            execute_query("""
                INSERT INTO doctors (
                    name, email, phone, specialization, qualification,
                    experience_years, consultation_fee, rating, available,
                    image_url, hospital, bio
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (email) DO NOTHING
            """, (name, email, phone, specialization, qualification, experience, 
                  consultation_fee, rating, True, image_url, hospital, bio), fetch=False)
            
            added_count += 1
            if added_count % 20 == 0:
                print(f"  ✓ Added {added_count}/{len(all_doctors)} doctors...")
                
        except Exception as e:
            print(f"  ✗ Error adding {name}: {e}")
    
    elapsed = time.time() - start_time
    print(f"\n✅ Successfully added {added_count} doctors in {elapsed:.2f} seconds!")
    
    # Show summary
    summary = execute_query("SELECT specialization, COUNT(*) as count FROM doctors GROUP BY specialization ORDER BY count DESC")
    print(f"\n📊 Doctors by Specialization:")
    for row in summary:
        print(f"   • {row['specialization']}: {row['count']}")

if __name__ == '__main__':
    add_all_doctors()
