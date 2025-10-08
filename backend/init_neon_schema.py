"""
Initialize Neon Database Schema
This script creates all necessary tables for the Healthcare Voice Agent
"""

from db import execute_query
import sys

def create_patients_table():
    """Create patients table"""
    query = """
    CREATE TABLE IF NOT EXISTS patients (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        phone VARCHAR(20),
        password_hash VARCHAR(255) NOT NULL,
        date_of_birth DATE,
        gender VARCHAR(20),
        blood_group VARCHAR(10),
        address TEXT,
        emergency_contact VARCHAR(20),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    execute_query(query, fetch=False)
    print("✅ Patients table created")

def create_doctors_table():
    """Create doctors table"""
    query = """
    CREATE TABLE IF NOT EXISTS doctors (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        phone VARCHAR(20),
        specialization VARCHAR(100) NOT NULL,
        qualification VARCHAR(255),
        experience_years INTEGER,
        consultation_fee DECIMAL(10, 2),
        rating DECIMAL(3, 2) DEFAULT 0.0,
        available BOOLEAN DEFAULT TRUE,
        image_url TEXT,
        hospital VARCHAR(255),
        bio TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    execute_query(query, fetch=False)
    print("✅ Doctors table created")

def create_appointments_table():
    """Create appointments table"""
    query = """
    CREATE TABLE IF NOT EXISTS appointments (
        id SERIAL PRIMARY KEY,
        patient_id INTEGER REFERENCES patients(id) ON DELETE CASCADE,
        doctor_id INTEGER REFERENCES doctors(id) ON DELETE CASCADE,
        appointment_date DATE NOT NULL,
        appointment_time TIME NOT NULL,
        status VARCHAR(50) DEFAULT 'scheduled',
        symptoms TEXT,
        diagnosis TEXT,
        prescription TEXT,
        notes TEXT,
        payment_status VARCHAR(50) DEFAULT 'pending',
        payment_amount DECIMAL(10, 2),
        booking_id VARCHAR(100) UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT unique_appointment UNIQUE(doctor_id, appointment_date, appointment_time)
    );
    """
    execute_query(query, fetch=False)
    print("✅ Appointments table created")

def create_availability_table():
    """Create doctor availability table"""
    query = """
    CREATE TABLE IF NOT EXISTS doctor_availability (
        id SERIAL PRIMARY KEY,
        doctor_id INTEGER REFERENCES doctors(id) ON DELETE CASCADE,
        day_of_week INTEGER NOT NULL CHECK (day_of_week BETWEEN 0 AND 6),
        start_time TIME NOT NULL,
        end_time TIME NOT NULL,
        is_available BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT unique_availability UNIQUE(doctor_id, day_of_week, start_time)
    );
    """
    execute_query(query, fetch=False)
    print("✅ Doctor availability table created")

def create_medical_records_table():
    """Create medical records table"""
    query = """
    CREATE TABLE IF NOT EXISTS medical_records (
        id SERIAL PRIMARY KEY,
        patient_id INTEGER REFERENCES patients(id) ON DELETE CASCADE,
        appointment_id INTEGER REFERENCES appointments(id) ON DELETE SET NULL,
        record_type VARCHAR(50),
        title VARCHAR(255),
        description TEXT,
        file_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    execute_query(query, fetch=False)
    print("✅ Medical records table created")

def create_prescriptions_table():
    """Create prescriptions table"""
    query = """
    CREATE TABLE IF NOT EXISTS prescriptions (
        id SERIAL PRIMARY KEY,
        appointment_id INTEGER REFERENCES appointments(id) ON DELETE CASCADE,
        patient_id INTEGER REFERENCES patients(id) ON DELETE CASCADE,
        doctor_id INTEGER REFERENCES doctors(id) ON DELETE CASCADE,
        medicines JSONB,
        dosage_instructions TEXT,
        duration VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    execute_query(query, fetch=False)
    print("✅ Prescriptions table created")

def create_voice_transcripts_table():
    """Create voice transcripts table for AI agent conversations"""
    query = """
    CREATE TABLE IF NOT EXISTS voice_transcripts (
        id SERIAL PRIMARY KEY,
        patient_id INTEGER REFERENCES patients(id) ON DELETE CASCADE,
        transcript TEXT NOT NULL,
        intent VARCHAR(100),
        entities JSONB,
        sentiment VARCHAR(50),
        language VARCHAR(10) DEFAULT 'en',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    execute_query(query, fetch=False)
    print("✅ Voice transcripts table created")

def create_notifications_table():
    """Create notifications table"""
    query = """
    CREATE TABLE IF NOT EXISTS notifications (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES patients(id) ON DELETE CASCADE,
        title VARCHAR(255) NOT NULL,
        message TEXT NOT NULL,
        type VARCHAR(50),
        is_read BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    execute_query(query, fetch=False)
    print("✅ Notifications table created")

def create_indexes():
    """Create indexes for better query performance"""
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_appointments_patient ON appointments(patient_id);",
        "CREATE INDEX IF NOT EXISTS idx_appointments_doctor ON appointments(doctor_id);",
        "CREATE INDEX IF NOT EXISTS idx_appointments_date ON appointments(appointment_date);",
        "CREATE INDEX IF NOT EXISTS idx_appointments_status ON appointments(status);",
        "CREATE INDEX IF NOT EXISTS idx_doctors_specialization ON doctors(specialization);",
        "CREATE INDEX IF NOT EXISTS idx_doctors_available ON doctors(available);",
        "CREATE INDEX IF NOT EXISTS idx_patients_email ON patients(email);",
        "CREATE INDEX IF NOT EXISTS idx_doctors_email ON doctors(email);",
        "CREATE INDEX IF NOT EXISTS idx_medical_records_patient ON medical_records(patient_id);",
        "CREATE INDEX IF NOT EXISTS idx_voice_transcripts_patient ON voice_transcripts(patient_id);",
        "CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id);",
    ]
    
    for index_query in indexes:
        execute_query(index_query, fetch=False)
    
    print("✅ All indexes created")

def create_triggers():
    """Create triggers for automatic timestamp updates"""
    trigger_function = """
    CREATE OR REPLACE FUNCTION update_updated_at_column()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = CURRENT_TIMESTAMP;
        RETURN NEW;
    END;
    $$ language 'plpgsql';
    """
    execute_query(trigger_function, fetch=False)
    
    tables = ['patients', 'doctors', 'appointments']
    for table in tables:
        trigger_query = f"""
        DROP TRIGGER IF EXISTS update_{table}_updated_at ON {table};
        CREATE TRIGGER update_{table}_updated_at
        BEFORE UPDATE ON {table}
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
        """
        execute_query(trigger_query, fetch=False)
    
    print("✅ Triggers created")

def main():
    """Main function to initialize all database tables"""
    print("🚀 Initializing Neon DB Schema for Healthcare Voice Agent...")
    print("=" * 60)
    
    try:
        create_patients_table()
        create_doctors_table()
        create_appointments_table()
        create_availability_table()
        create_medical_records_table()
        create_prescriptions_table()
        create_voice_transcripts_table()
        create_notifications_table()
        create_indexes()
        create_triggers()
        
        print("=" * 60)
        print("✅ Database schema initialization complete!")
        print("\n📊 Summary:")
        print("   • 8 tables created")
        print("   • 11 indexes created")
        print("   • 3 triggers created")
        print("\n🎉 Your Neon DB is ready to use!")
        
    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        print("\n💡 Troubleshooting tips:")
        print("   1. Check your NEON_DATABASE_URL in .env file")
        print("   2. Ensure your Neon project is active")
        print("   3. Verify network connectivity")
        sys.exit(1)

if __name__ == "__main__":
    main()
