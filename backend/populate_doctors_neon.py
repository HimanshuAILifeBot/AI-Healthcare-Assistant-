"""
Populate Neon DB with Doctor Data
This script adds comprehensive doctor data across all specializations
"""

from db import execute_query, get_db_cursor
import sys

# Sample hospitals data (simplified - will be stored in doctor.hospital field)
HOSPITALS = [
    "City General Hospital",
    "St. Mary's Medical Center",
    "Metro Health Institute",
    "Central Healthcare Complex"
]

def add_doctors_data():
    """Add comprehensive doctor data to Neon DB"""
    
    doctors_data = [
        # Cardiology - Heart specialists
        ('Dr. Michael Chen', 'michael.chen@cityhospital.com', '+1-555-0101', 'Cardiology', 'MD, FACC', 15, 500.00, 4.8, True, 
         'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=400', HOSPITALS[0], 
         'Renowned cardiologist specializing in interventional cardiology and heart failure management.'),
        
        ('Dr. Sarah Thompson', 'sarah.thompson@stmarys.com', '+1-555-0102', 'Cardiology', 'MD, FACC', 12, 480.00, 4.7, True,
         'https://images.unsplash.com/photo-1594824476967-48c8b964273f?w=400', HOSPITALS[1],
         'Expert in cardiac imaging and preventive cardiology.'),
        
        ('Dr. Robert Kim', 'robert.kim@metro.health', '+1-555-0103', 'Cardiology', 'MD, PhD', 20, 600.00, 4.9, True,
         'https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=400', HOSPITALS[2],
         'Leading expert in electrophysiology and arrhythmia management.'),
        
        # Dermatology - Skin specialists
        ('Dr. Emily Watson', 'emily.watson@cityhospital.com', '+1-555-0201', 'Dermatology', 'MD, FAAD', 10, 350.00, 4.7, True,
         'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=400', HOSPITALS[0],
         'Specializes in cosmetic dermatology and skin cancer treatment.'),
        
        ('Dr. Carlos Rivera', 'carlos.rivera@stmarys.com', '+1-555-0202', 'Dermatology', 'MD, FAAD', 14, 380.00, 4.8, True,
         'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=400', HOSPITALS[1],
         'Expert in medical dermatology and psoriasis treatment.'),
        
        # Neurology - Brain and nervous system
        ('Dr. Rachel Miller', 'rachel.miller@metro.health', '+1-555-0301', 'Neurology', 'MD, FAAN', 13, 520.00, 4.8, True,
         'https://images.unsplash.com/photo-1594824476967-48c8b964273f?w=400', HOSPITALS[2],
         'Specializes in stroke treatment and neurovascular diseases.'),
        
        ('Dr. David Wilson', 'david.wilson@central.health', '+1-555-0302', 'Neurology', 'MD, PhD, FAAN', 19, 580.00, 4.9, True,
         'https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=400', HOSPITALS[3],
         'Leading expert in movement disorders and Parkinson\'s disease.'),
        
        # Orthopedics - Bone and joint specialists
        ('Dr. Kevin Martinez', 'kevin.martinez@cityhospital.com', '+1-555-0401', 'Orthopedics', 'MD, FAAOS', 17, 450.00, 4.9, True,
         'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=400', HOSPITALS[0],
         'Specializes in sports medicine and joint replacement surgery.'),
        
        ('Dr. Michelle Davis', 'michelle.davis@stmarys.com', '+1-555-0402', 'Orthopedics', 'MD, FAAOS', 9, 400.00, 4.6, True,
         'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=400', HOSPITALS[1],
         'Expert in pediatric orthopedics and spine surgery.'),
        
        # Pediatrics - Children specialists
        ('Dr. Maria Gonzalez', 'maria.gonzalez@metro.health', '+1-555-0501', 'Pediatrics', 'MD, FAAP', 8, 300.00, 4.7, True,
         'https://images.unsplash.com/photo-1594824476967-48c8b964273f?w=400', HOSPITALS[2],
         'Compassionate pediatrician specializing in childhood development.'),
        
        ('Dr. Christopher White', 'chris.white@central.health', '+1-555-0502', 'Pediatrics', 'MD, FAAP', 14, 320.00, 4.8, True,
         'https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=400', HOSPITALS[3],
         'Expert in pediatric infectious diseases and immunology.'),
        
        # Gastroenterology - Digestive system
        ('Dr. Antonio Garcia', 'antonio.garcia@cityhospital.com', '+1-555-0601', 'Gastroenterology', 'MD, FACG', 13, 460.00, 4.8, True,
         'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=400', HOSPITALS[0],
         'Specializes in inflammatory bowel disease and endoscopy.'),
        
        ('Dr. Helen Cooper', 'helen.cooper@stmarys.com', '+1-555-0602', 'Gastroenterology', 'MD, FACG', 18, 500.00, 4.9, True,
         'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=400', HOSPITALS[1],
         'Expert in liver diseases and therapeutic endoscopy.'),
        
        # Oncology - Cancer specialists
        ('Dr. Alexander Turner', 'alex.turner@metro.health', '+1-555-0701', 'Oncology', 'MD, FASCO', 20, 650.00, 4.9, True,
         'https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=400', HOSPITALS[2],
         'Leading oncologist specializing in breast cancer treatment.'),
        
        ('Dr. Victoria Hall', 'victoria.hall@central.health', '+1-555-0702', 'Oncology', 'MD, PhD', 16, 620.00, 4.8, True,
         'https://images.unsplash.com/photo-1594824476967-48c8b964273f?w=400', HOSPITALS[3],
         'Expert in hematologic malignancies and bone marrow transplants.'),
        
        # Psychiatry - Mental health
        ('Dr. Daniel Kim', 'daniel.kim@cityhospital.com', '+1-555-0801', 'Psychiatry', 'MD, FAPA', 11, 380.00, 4.7, True,
         'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=400', HOSPITALS[0],
         'Specializes in anxiety disorders and cognitive behavioral therapy.'),
        
        ('Dr. Rebecca Foster', 'rebecca.foster@stmarys.com', '+1-555-0802', 'Psychiatry', 'MD, FAPA', 14, 400.00, 4.8, True,
         'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=400', HOSPITALS[1],
         'Expert in mood disorders and psychopharmacology.'),
        
        # Ophthalmology - Eye specialists
        ('Dr. Matthew Baker', 'matthew.baker@metro.health', '+1-555-0901', 'Ophthalmology', 'MD, FACS', 14, 420.00, 4.8, True,
         'https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=400', HOSPITALS[2],
         'Specializes in cataract surgery and refractive procedures.'),
        
        ('Dr. Jennifer Adams', 'jennifer.adams@central.health', '+1-555-0902', 'Ophthalmology', 'MD, FACS', 10, 400.00, 4.7, True,
         'https://images.unsplash.com/photo-1594824476967-48c8b964273f?w=400', HOSPITALS[3],
         'Expert in retinal diseases and diabetic eye care.'),
        
        # Pulmonology - Lung specialists
        ('Dr. Charles Roberts', 'charles.roberts@cityhospital.com', '+1-555-1001', 'Pulmonology', 'MD, FCCP', 17, 480.00, 4.8, True,
         'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=400', HOSPITALS[0],
         'Specializes in COPD, asthma, and critical care medicine.'),
        
        ('Dr. Angela Collins', 'angela.collins@stmarys.com', '+1-555-1002', 'Pulmonology', 'MD, FCCP', 13, 460.00, 4.7, True,
         'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=400', HOSPITALS[1],
         'Expert in interstitial lung disease and pulmonary hypertension.'),
        
        # Endocrinology - Hormone specialists
        ('Dr. Joseph Morris', 'joseph.morris@metro.health', '+1-555-1101', 'Endocrinology', 'MD, FACE', 12, 440.00, 4.7, True,
         'https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=400', HOSPITALS[2],
         'Specializes in diabetes management and thyroid disorders.'),
        
        ('Dr. Christina Reed', 'christina.reed@central.health', '+1-555-1102', 'Endocrinology', 'MD, FACE', 16, 470.00, 4.8, True,
         'https://images.unsplash.com/photo-1594824476967-48c8b964273f?w=400', HOSPITALS[3],
         'Expert in metabolic disorders and hormone replacement therapy.'),
        
        # Nephrology - Kidney specialists
        ('Dr. Wayne Barnes', 'wayne.barnes@cityhospital.com', '+1-555-1201', 'Nephrology', 'MD, FASN', 19, 520.00, 4.9, True,
         'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=400', HOSPITALS[0],
         'Leading expert in kidney transplantation and dialysis.'),
        
        ('Dr. Theresa Kelly', 'theresa.kelly@stmarys.com', '+1-555-1202', 'Nephrology', 'MD, FASN', 10, 480.00, 4.6, True,
         'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=400', HOSPITALS[1],
         'Specializes in chronic kidney disease and hypertension.'),
        
        # Family Medicine - Primary care
        ('Dr. Jesse Freeman', 'jesse.freeman@metro.health', '+1-555-1301', 'Family Medicine', 'MD, FAAFP', 11, 250.00, 4.7, True,
         'https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=400', HOSPITALS[2],
         'Comprehensive primary care for patients of all ages.'),
        
        ('Dr. Joan Wells', 'joan.wells@central.health', '+1-555-1302', 'Family Medicine', 'MD, FAAFP', 15, 270.00, 4.8, True,
         'https://images.unsplash.com/photo-1594824476967-48c8b964273f?w=400', HOSPITALS[3],
         'Expert in preventive medicine and chronic disease management.'),
        
        # Emergency Medicine
        ('Dr. Ivan Mills', 'ivan.mills@cityhospital.com', '+1-555-1401', 'Emergency Medicine', 'MD, FACEP', 12, 400.00, 4.7, True,
         'https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=400', HOSPITALS[0],
         'Experienced emergency physician with trauma expertise.'),
        
        ('Dr. Paula Lane', 'paula.lane@stmarys.com', '+1-555-1402', 'Emergency Medicine', 'MD, FACEP', 8, 380.00, 4.8, True,
         'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=400', HOSPITALS[1],
         'Specializes in critical care and emergency procedures.'),
        
        # Obstetrics and Gynecology
        ('Dr. Bobby Porter', 'bobby.porter@metro.health', '+1-555-1501', 'Obstetrics and Gynecology', 'MD, FACOG', 14, 420.00, 4.8, True,
         'https://images.unsplash.com/photo-1622253692010-333f2da6031d?w=400', HOSPITALS[2],
         'Comprehensive women\'s health care and high-risk obstetrics.'),
        
        ('Dr. Martha Fisher', 'martha.fisher@central.health', '+1-555-1502', 'Obstetrics and Gynecology', 'MD, FACOG', 18, 450.00, 4.9, True,
         'https://images.unsplash.com/photo-1594824476967-48c8b964273f?w=400', HOSPITALS[3],
         'Expert in minimally invasive gynecologic surgery.'),
    ]
    
    print("🚀 Populating Neon DB with Doctor Data...")
    print("=" * 70)
    
    # SQL query to insert doctors
    insert_query = """
    INSERT INTO doctors (
        name, email, phone, specialization, qualification, experience_years,
        consultation_fee, rating, available, image_url, hospital, bio
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    try:
        # Check if doctors already exist
        existing_count = execute_query("SELECT COUNT(*) as count FROM doctors")
        if existing_count and existing_count[0]['count'] > 0:
            print(f"⚠️  Warning: {existing_count[0]['count']} doctors already exist in database")
            response = input("Do you want to add more doctors? (y/n): ")
            if response.lower() != 'y':
                print("❌ Operation cancelled")
                return
        
        # Insert all doctors
        success_count = 0
        failed_count = 0
        
        with get_db_cursor() as cursor:
            for doctor_data in doctors_data:
                try:
                    cursor.execute(insert_query, doctor_data)
                    success_count += 1
                    print(f"✅ Added: {doctor_data[0]} - {doctor_data[3]}")
                except Exception as e:
                    failed_count += 1
                    print(f"❌ Failed to add {doctor_data[0]}: {str(e)}")
        
        print("=" * 70)
        print(f"✅ Successfully added {success_count} doctors")
        if failed_count > 0:
            print(f"❌ Failed to add {failed_count} doctors")
        
        # Show statistics
        print("\n📊 Database Statistics:")
        stats = execute_query("""
            SELECT 
                specialization,
                COUNT(*) as doctor_count,
                ROUND(AVG(consultation_fee), 2) as avg_fee,
                ROUND(AVG(rating), 2) as avg_rating
            FROM doctors
            GROUP BY specialization
            ORDER BY doctor_count DESC, specialization
        """)
        
        print("\n{:<35} {:<10} {:<12} {:<10}".format("Specialization", "Doctors", "Avg Fee", "Avg Rating"))
        print("-" * 70)
        for stat in stats:
            print("{:<35} {:<10} ${:<11} {:<10}".format(
                stat['specialization'],
                stat['doctor_count'],
                stat['avg_fee'],
                stat['avg_rating']
            ))
        
        total_doctors = execute_query("SELECT COUNT(*) as count FROM doctors")
        print("\n" + "=" * 70)
        print(f"🎉 Total Doctors in Database: {total_doctors[0]['count']}")
        print("✅ Doctor data population complete!")
        
    except Exception as e:
        print(f"\n❌ Error populating doctor data: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Ensure database schema is initialized: python init_neon_schema.py")
        print("   2. Check your database connection: python test_neon_connection.py")
        print("   3. Verify NEON_DATABASE_URL in .env file")
        sys.exit(1)

if __name__ == "__main__":
    add_doctors_data()
