# 🚀 Quick Start - Neon DB Integration

## ✅ Integration Complete!

Your Healthcare Voice Agent is now successfully integrated with Neon DB (Serverless PostgreSQL).

## 📋 What Was Set Up

### 1. Database Connection
- ✅ Updated `config.py` to support Neon DATABASE_URL
- ✅ Enhanced `db.py` with connection helpers and context managers
- ✅ Connection tested and working with PostgreSQL 17.5

### 2. Database Schema
The following tables have been created in your Neon database:

| # | Table Name | Description |
|---|------------|-------------|
| 1 | `patients` | User accounts and personal information |
| 2 | `doctors` | Healthcare provider profiles |
| 3 | `appointments` | Appointment bookings and schedules |
| 4 | `doctor_availability` | Doctor working hours by day |
| 5 | `medical_records` | Patient medical documents |
| 6 | `prescriptions` | Medication prescriptions |
| 7 | `voice_transcripts` | AI voice agent conversation logs |
| 8 | `notifications` | User notifications |

### 3. Performance Optimizations
- ✅ 11 indexes created on frequently queried columns
- ✅ Automatic timestamp triggers for `updated_at` fields
- ✅ Foreign key constraints for data integrity
- ✅ Unique constraints to prevent duplicates

## 🎯 Next Steps

### 1. Start Your Backend Server

```bash
cd backend
source venv/bin/activate  # If not already activated
uvicorn main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Redoc**: http://localhost:8000/redoc

### 2. Start Your Frontend

```bash
# In a new terminal
cd .. # Go to project root
npm run dev
```

The frontend will be available at: http://localhost:5173

### 3. Test the Integration

Try these endpoints:
- **Signup**: `POST http://localhost:8000/signup`
- **Login**: `POST http://localhost:8000/login`
- **Get Doctors**: `GET http://localhost:8000/doctors`
- **Book Appointment**: `POST http://localhost:8000/book-appointment`

## 📊 Database Tools

### View Your Data in Neon Console

1. Go to [neon.tech](https://neon.tech)
2. Login to your account
3. Select your project
4. Click "Tables" to browse data
5. Use the SQL Editor to run queries

### Use the CLI Helper Functions

```python
from db import execute_query, get_db_cursor

# Simple query
patients = execute_query("SELECT * FROM patients LIMIT 10")

# With parameters (safe from SQL injection)
patient = execute_query(
    "SELECT * FROM patients WHERE email = %s",
    ("user@example.com",)
)

# Insert with context manager
with get_db_cursor() as cursor:
    cursor.execute(
        "INSERT INTO patients (name, email, password_hash) VALUES (%s, %s, %s)",
        ("John Doe", "john@example.com", "hashed_password")
    )
```

## 🔧 Useful Commands

### Test Database Connection
```bash
python test_neon_connection.py
```

### Reinitialize Schema (if needed)
```bash
python init_neon_schema.py
```

### Run Full Setup Script
```bash
./setup_neon.sh
```

### Check Python Environment
```bash
python --version
pip list | grep psycopg2
```

## 📚 Documentation

- **Neon Setup Guide**: [backend/NEON_SETUP.md](./NEON_SETUP.md)
- **API Documentation**: http://localhost:8000/docs (after starting server)
- **Neon Docs**: https://neon.tech/docs

## 🎨 Database Schema Visualization

```
patients
  ├─ id (PK)
  ├─ name, email, phone
  ├─ password_hash
  └─ medical info

doctors
  ├─ id (PK)
  ├─ name, specialization
  ├─ consultation_fee
  └─ availability status

appointments
  ├─ id (PK)
  ├─ patient_id (FK → patients)
  ├─ doctor_id (FK → doctors)
  ├─ date, time, status
  └─ payment info

doctor_availability
  ├─ id (PK)
  ├─ doctor_id (FK → doctors)
  ├─ day_of_week
  └─ start_time, end_time

medical_records
  ├─ id (PK)
  ├─ patient_id (FK → patients)
  ├─ appointment_id (FK → appointments)
  └─ record data

prescriptions
  ├─ id (PK)
  ├─ appointment_id (FK → appointments)
  ├─ patient_id (FK → patients)
  └─ medicines (JSONB)

voice_transcripts
  ├─ id (PK)
  ├─ patient_id (FK → patients)
  ├─ transcript, intent
  └─ entities (JSONB)

notifications
  ├─ id (PK)
  ├─ user_id (FK → patients)
  ├─ message
  └─ read status
```

## 🔐 Security Notes

✅ **Your .env file is protected**
- Already in `.gitignore`
- Not committed to Git
- Contains your actual credentials

⚠️ **Important**: The `.env.example` file has been sanitized with placeholder values.

## 💡 Pro Tips

1. **Use Connection Pooling**: Your Neon URL includes `-pooler` for built-in connection pooling
2. **Monitor Usage**: Check your Neon Console for compute time and storage usage
3. **Database Branches**: Create branches in Neon for testing without affecting production
4. **Automatic Backups**: Neon automatically backs up your data
5. **Scale to Zero**: Your database scales to zero when idle (free tier)

## 🐛 Troubleshooting

### Connection Issues?
```bash
python test_neon_connection.py
```

### Tables Not Created?
```bash
python init_neon_schema.py
```

### Environment Issues?
```bash
cat .env | grep NEON_DATABASE_URL
```

### Need to Reset?
Drop all tables in Neon Console SQL Editor:
```sql
DROP TABLE IF EXISTS notifications CASCADE;
DROP TABLE IF EXISTS voice_transcripts CASCADE;
DROP TABLE IF EXISTS prescriptions CASCADE;
DROP TABLE IF EXISTS medical_records CASCADE;
DROP TABLE IF EXISTS appointments CASCADE;
DROP TABLE IF EXISTS doctor_availability CASCADE;
DROP TABLE IF EXISTS doctors CASCADE;
DROP TABLE IF EXISTS patients CASCADE;
```

Then run: `python init_neon_schema.py`

## 📞 Support

- **Neon Issues**: [Neon Discord](https://discord.gg/neon)
- **App Issues**: Check the logs in terminal
- **Documentation**: See [NEON_SETUP.md](./NEON_SETUP.md)

---

## 🎉 Success!

Your Healthcare Voice Agent is now running on:
- **Backend**: Neon PostgreSQL (Serverless)
- **Frontend**: React + Vite
- **AI**: Azure OpenAI + Azure TTS
- **Voice**: ElevenLabs

**Happy Coding! 🚀**
