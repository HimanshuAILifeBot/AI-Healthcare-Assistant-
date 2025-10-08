
from db import execute_query, get_db_cursor
from config import Config

def add_doctors():
    """
    Add doctors to Neon DB with updated schema
    Schema: name, email, phone, specialization, qualification, experience_years, 
            consultation_fee, rating, available, image_url, hospital, bio
    """
    
    # Hospital names for rotation
    hospitals = [
        'City General Hospital',
        'Saint Mary Medical Center', 
        'Metro Health Institute',
        'University Medical Center'
    ]
    
    doctors_to_add = [
        # Cardiology - Heart specialists
        ('Dr. Michael Chen', 'Cardiology', 15, 4.8, 0),
        ('Dr. Sarah Thompson', 'Cardiology', 12, 4.7, 1),
        ('Dr. Robert Kim', 'Cardiology', 20, 4.9, 2),
        ('Dr. Lisa Anderson', 'Cardiology', 8, 4.6, 3),
        ('Dr. Ahmed Hassan', 'Cardiology', 18, 4.8, 0),
        
        # Dermatology - Skin specialists
        ('Dr. Emily Watson', 'Dermatology', 10, 4.7, 2),
        ('Dr. Carlos Rivera', 'Dermatology', 14, 4.8, 3),
        ('Dr. Jennifer Park', 'Dermatology', 7, 4.6, 4),
        ('Dr. Marcus Johnson', 'Dermatology', 16, 4.9, 1),
        
        # Neurology - Brain and nervous system
        ('Dr. Rachel Miller', 'Neurology', 13, 4.8, 2),
        ('Dr. David Wilson', 'Neurology', 19, 4.9, 3),
        ('Dr. Priya Patel', 'Neurology', 11, 4.7, 4),
        ('Dr. Thomas Brown', 'Neurology', 22, 4.8, 1),
        
        # Orthopedics - Bone and joint specialists
        ('Dr. Kevin Martinez', 'Orthopedics', 17, 4.9, 2),
        ('Dr. Michelle Davis', 'Orthopedics', 9, 4.6, 3),
        ('Dr. Jason Lee', 'Orthopedics', 21, 4.8, 4),
        ('Dr. Amanda Rodriguez', 'Orthopedics', 12, 4.7, 1),
        ('Dr. Steven Clark', 'Orthopedics', 25, 4.9, 2),
        
        # Pediatrics - Children specialists
        ('Dr. Maria Gonzalez', 'Pediatrics', 8, 4.7, 3),
        ('Dr. Christopher White', 'Pediatrics', 14, 4.8, 4),
        ('Dr. Nicole Taylor', 'Pediatrics', 6, 4.6, 1),
        ('Dr. Benjamin Moore', 'Pediatrics', 11, 4.7, 2),
        ('Dr. Samantha Jackson', 'Pediatrics', 16, 4.9, 3),
        
        # Gastroenterology - Digestive system
        ('Dr. Antonio Garcia', 'Gastroenterology', 13, 4.8, 4),
        ('Dr. Helen Cooper', 'Gastroenterology', 18, 4.9, 1),
        ('Dr. Ryan Phillips', 'Gastroenterology', 10, 4.6, 2),
        ('Dr. Natalie Evans', 'Gastroenterology', 15, 4.7, 3),
        
        # Oncology - Cancer specialists
        ('Dr. Alexander Turner', 'Oncology', 20, 4.9, 4),
        ('Dr. Victoria Hall', 'Oncology', 16, 4.8, 1),
        ('Dr. Gabriel Santos', 'Oncology', 12, 4.7, 2),
        ('Dr. Catherine Wright', 'Oncology', 24, 4.9, 3),
        
        # Psychiatry - Mental health
        ('Dr. Daniel Kim', 'Psychiatry', 11, 4.7, 4),
        ('Dr. Rebecca Foster', 'Psychiatry', 14, 4.8, 1),
        ('Dr. Luis Rodriguez', 'Psychiatry', 9, 4.6, 2),
        ('Dr. Ashley Chen', 'Psychiatry', 17, 4.8, 3),
        ('Dr. Peter Williams', 'Psychiatry', 13, 4.7, 4),
        
        # Urology - Urinary system
        ('Dr. Jonathan Bell', 'Urology', 16, 4.8, 1),
        ('Dr. Diana Murphy', 'Urology', 12, 4.7, 2),
        ('Dr. Eric Thompson', 'Urology', 19, 4.9, 3),
        ('Dr. Stephanie Cook', 'Urology', 8, 4.6, 4),
        
        # Ophthalmology - Eye specialists
        ('Dr. Matthew Baker', 'Ophthalmology', 14, 4.8, 1),
        ('Dr. Jennifer Adams', 'Ophthalmology', 10, 4.7, 2),
        ('Dr. Richard Green', 'Ophthalmology', 18, 4.9, 3),
        ('Dr. Laura Mitchell', 'Ophthalmology', 7, 4.6, 4),
        
        # Otolaryngology - Ear, Nose, Throat
        ('Dr. Paul Nelson', 'Otolaryngology', 15, 4.8, 1),
        ('Dr. Karen Scott', 'Otolaryngology', 11, 4.7, 2),
        ('Dr. Andrew Carter', 'Otolaryngology', 20, 4.9, 3),
        ('Dr. Monica Perez', 'Otolaryngology', 9, 4.6, 4),
        
        # Pulmonology - Lung specialists
        ('Dr. Charles Roberts', 'Pulmonology', 17, 4.8, 1),
        ('Dr. Angela Collins', 'Pulmonology', 13, 4.7, 2),
        ('Dr. Frank Edwards', 'Pulmonology', 22, 4.9, 3),
        ('Dr. Melissa Stewart', 'Pulmonology', 8, 4.6, 4),
        
        # Endocrinology - Hormone specialists
        ('Dr. Joseph Morris', 'Endocrinology', 12, 4.7, 1),
        ('Dr. Christina Reed', 'Endocrinology', 16, 4.8, 2),
        ('Dr. Mark Bailey', 'Endocrinology', 9, 4.6, 3),
        ('Dr. Sandra Rivera', 'Endocrinology', 14, 4.8, 4),
        
        # Rheumatology - Joint and autoimmune
        ('Dr. Gregory Cooper', 'Rheumatology', 18, 4.9, 1),
        ('Dr. Deborah Hughes', 'Rheumatology', 11, 4.7, 2),
        ('Dr. Carl Peterson', 'Rheumatology', 15, 4.8, 3),
        ('Dr. Janet Price', 'Rheumatology', 13, 4.7, 4),
        
        # Nephrology - Kidney specialists
        ('Dr. Wayne Barnes', 'Nephrology', 19, 4.9, 1),
        ('Dr. Theresa Kelly', 'Nephrology', 10, 4.6, 2),
        ('Dr. Eugene Howard', 'Nephrology', 16, 4.8, 3),
        ('Dr. Jacqueline Ward', 'Nephrology', 12, 4.7, 4),
        
        # Allergist/Immunologist
        ('Dr. Ralph Torres', 'Allergist/Immunologist', 14, 4.8, 1),
        ('Dr. Frances Wood', 'Allergist/Immunologist', 8, 4.6, 2),
        ('Dr. Harold Watson', 'Allergist/Immunologist', 17, 4.9, 3),
        ('Dr. Denise Brooks', 'Allergist/Immunologist', 11, 4.7, 4),
        
        # General Surgery
        ('Dr. Arthur Bennett', 'General Surgery', 20, 4.9, 1),
        ('Dr. Gloria Gray', 'General Surgery', 15, 4.8, 2),
        ('Dr. Lawrence James', 'General Surgery', 25, 4.9, 3),
        ('Dr. Teresa Ross', 'General Surgery', 12, 4.7, 4),
        ('Dr. Philip Henderson', 'General Surgery', 18, 4.8, 1),
        
        # Infectious Disease
        ('Dr. Roger Butler', 'Infectious Disease', 16, 4.8, 2),
        ('Dr. Judith Powell', 'Infectious Disease', 13, 4.7, 3),
        ('Dr. Gerald Jenkins', 'Infectious Disease', 21, 4.9, 4),
        ('Dr. Marie Perry', 'Infectious Disease', 9, 4.6, 1),
        
        # Hematology - Blood specialists
        ('Dr. Harold Russell', 'Hematology', 17, 4.8, 2),
        ('Dr. Shirley Griffin', 'Hematology', 14, 4.7, 3),
        ('Dr. Albert Washington', 'Hematology', 19, 4.9, 4),
        ('Dr. Ruby Diaz', 'Hematology', 10, 4.6, 1),
        
        # Geriatrics - Elderly care
        ('Dr. Eugene Butler', 'Geriatrics', 23, 4.9, 2),
        ('Dr. Phyllis Hayes', 'Geriatrics', 18, 4.8, 3),
        ('Dr. Leonard Myers', 'Geriatrics', 26, 4.9, 4),
        ('Dr. Beverly Ford', 'Geriatrics', 15, 4.7, 1),
        
        # Plastic Surgery
        ('Dr. Norman Hamilton', 'Plastic Surgery', 12, 4.7, 2),
        ('Dr. Kathleen Graham', 'Plastic Surgery', 8, 4.6, 3),
        ('Dr. Douglas Sullivan', 'Plastic Surgery', 16, 4.8, 4),
        ('Dr. Ann Wallace', 'Plastic Surgery', 14, 4.8, 1),
        
        # Family Medicine - Primary care
        ('Dr. Jesse Freeman', 'Family Medicine', 11, 4.7, 2),
        ('Dr. Joan Wells', 'Family Medicine', 15, 4.8, 3),
        ('Dr. Billy Woods', 'Family Medicine', 7, 4.6, 4),
        ('Dr. Dorothy West', 'Family Medicine', 19, 4.9, 1),
        ('Dr. Victor Chapman', 'Family Medicine', 13, 4.7, 2),
        
        # Anesthesiology
        ('Dr. Craig Mason', 'Anesthesiology', 16, 4.8, 3),
        ('Dr. Marilyn Hunt', 'Anesthesiology', 12, 4.7, 4),
        ('Dr. Tony Black', 'Anesthesiology', 20, 4.9, 1),
        ('Dr. Julie Gibson', 'Anesthesiology', 9, 4.6, 2),
        
        # Radiology - Medical imaging
        ('Dr. Eugene Kennedy', 'Radiology', 18, 4.8, 3),
        ('Dr. Cheryl Hawkins', 'Radiology', 14, 4.7, 4),
        ('Dr. Keith Hansen', 'Radiology', 22, 4.9, 1),
        ('Dr. Alice Pierce', 'Radiology', 10, 4.6, 2),
        
        # Physical Medicine & Rehabilitation
        ('Dr. Todd George', 'Physical Medicine & Rehabilitation', 13, 4.7, 3),
        ('Dr. Evelyn Stone', 'Physical Medicine & Rehabilitation', 17, 4.8, 4),
        ('Dr. Curtis Knight', 'Physical Medicine & Rehabilitation', 11, 4.7, 1),
        ('Dr. Brenda Fox', 'Physical Medicine & Rehabilitation', 15, 4.8, 2),
        
        # Additional specialized fields
        ('Dr. Ivan Mills', 'Emergency Medicine', 12, 4.7, 1),
        ('Dr. Paula Lane', 'Emergency Medicine', 8, 4.8, 2),
        ('Dr. Roy Boyd', 'Emergency Medicine', 15, 4.9, 3),
        ('Dr. Irene Arnold', 'Emergency Medicine', 10, 4.6, 4),
        
        ('Dr. Louis Reid', 'Pathology', 20, 4.8, 1),
        ('Dr. Donna Fleming', 'Pathology', 16, 4.7, 2),
        ('Dr. Willie Hunter', 'Pathology', 24, 4.9, 3),
        ('Dr. Lois Mason', 'Pathology', 11, 4.6, 4),
        
        ('Dr. Bobby Porter', 'Obstetrics and Gynecology', 14, 4.8, 1),
        ('Dr. Martha Fisher', 'Obstetrics and Gynecology', 18, 4.9, 2),
        ('Dr. Ralph Palmer', 'Obstetrics and Gynecology', 9, 4.6, 3),
        ('Dr. Gloria Fuller', 'Obstetrics and Gynecology', 13, 4.7, 4)
    ]

    
    print("🏥 Adding doctors to Neon DB...")
    print("=" * 60)
    
    try:
        # Counter for success
        success_count = 0
        
        with get_db_cursor() as cursor:
            for name, specialization, experience, rating, hospital_idx in doctors_to_add:
                # Generate email from name
                email = name.lower().replace('dr. ', '').replace(' ', '.') + '@healthcare.com'
                
                # Generate phone number
                phone = f'+1-555-{1000 + success_count:04d}'
                
                # Generate qualification
                qualifications = {
                    'Cardiology': 'MD, FACC, Board Certified Cardiologist',
                    'Dermatology': 'MD, Board Certified Dermatologist',
                    'Neurology': 'MD, PhD, Board Certified Neurologist',
                    'Orthopedics': 'MD, FAAOS, Board Certified Orthopedic Surgeon',
                    'Pediatrics': 'MD, FAAP, Board Certified Pediatrician',
                    'Gastroenterology': 'MD, FACG, Board Certified Gastroenterologist',
                    'Oncology': 'MD, FASCO, Board Certified Oncologist',
                    'Psychiatry': 'MD, Board Certified Psychiatrist',
                    'Urology': 'MD, FACS, Board Certified Urologist',
                    'Ophthalmology': 'MD, Board Certified Ophthalmologist',
                    'Otolaryngology': 'MD, Board Certified ENT Specialist',
                    'Pulmonology': 'MD, FCCP, Board Certified Pulmonologist',
                    'Endocrinology': 'MD, Board Certified Endocrinologist',
                    'Rheumatology': 'MD, Board Certified Rheumatologist',
                    'Nephrology': 'MD, Board Certified Nephrologist',
                    'Allergist/Immunologist': 'MD, Board Certified Allergist',
                    'General Surgery': 'MD, FACS, Board Certified Surgeon',
                    'Infectious Disease': 'MD, Board Certified Infectious Disease Specialist',
                    'Hematology': 'MD, Board Certified Hematologist',
                    'Geriatrics': 'MD, Board Certified Geriatrician',
                    'Plastic Surgery': 'MD, FACS, Board Certified Plastic Surgeon',
                    'Family Medicine': 'MD, Board Certified Family Physician',
                    'Anesthesiology': 'MD, Board Certified Anesthesiologist',
                    'Radiology': 'MD, Board Certified Radiologist',
                    'Physical Medicine & Rehabilitation': 'MD, Board Certified PM&R Specialist',
                    'Emergency Medicine': 'MD, Board Certified Emergency Physician',
                    'Pathology': 'MD, Board Certified Pathologist',
                    'Obstetrics and Gynecology': 'MD, FACOG, Board Certified OB/GYN'
                }
                qualification = qualifications.get(specialization, 'MD, Board Certified Physician')
                
                # Calculate consultation fee based on experience and rating
                base_fee = 100
                experience_bonus = experience * 5
                rating_bonus = (rating - 4.0) * 50
                consultation_fee = base_fee + experience_bonus + rating_bonus
                
                # Get hospital name
                hospital = hospitals[hospital_idx % len(hospitals)]
                
                # Generate bio
                bio = f"Experienced {specialization} specialist with {experience} years of practice at {hospital}. Committed to providing excellent patient care."
                
                # Image URL (placeholder - you can update these with real images later)
                image_url = f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&size=200&background=random"
                
                # Insert doctor
                cursor.execute("""
                    INSERT INTO doctors (
                        name, email, phone, specialization, qualification, 
                        experience_years, consultation_fee, rating, available, 
                        image_url, hospital, bio
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (email) DO NOTHING
                """, (
                    name, email, phone, specialization, qualification,
                    experience, consultation_fee, rating, True,
                    image_url, hospital, bio
                ))
                
                success_count += 1
                if success_count % 10 == 0:
                    print(f"✅ Added {success_count} doctors...")
        
        print("=" * 60)
        print(f"✅ Successfully added {success_count} doctors to Neon DB!")
        print("\n📊 Summary by Specialization:")
        
        # Get count by specialization
        specializations = execute_query("""
            SELECT specialization, COUNT(*) as count 
            FROM doctors 
            GROUP BY specialization 
            ORDER BY count DESC
        """)
        
        for spec in specializations:
            print(f"   • {spec['specialization']}: {spec['count']} doctors")
        
        print("\n🎉 Doctor data population complete!")
        
    except Exception as error:
        print(f"\n❌ Error adding doctors: {error}")
        raise

if __name__ == '__main__':
    add_doctors()
