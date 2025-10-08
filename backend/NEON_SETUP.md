# Neon DB Integration Guide

## Overview

This Healthcare Voice Agent now uses [Neon](https://neon.tech) - a serverless PostgreSQL database that provides:

- ⚡ Serverless architecture with instant cold starts
- 🔄 Automatic scaling based on usage
- 🌿 Database branching for development/staging
- 💰 Generous free tier (0.5 GB storage, 100 hours compute/month)
- 🔒 Built-in security with SSL/TLS encryption

## Quick Start

### 1. Get Your Neon Database

1. **Sign up** at [neon.tech](https://neon.tech)
2. **Create a new project**
   - Click "New Project"
   - Choose a region (closest to your users)
   - Name your project (e.g., "healthcare-voice-agent")
3. **Copy the connection string**
   - Format: `postgresql://user:password@host/dbname?sslmode=require`

### 2. Configure Your Application

Update your `.env` file in the `backend/` directory:

```bash
# Neon Database Configuration
NEON_DATABASE_URL=postgresql://neondb_owner:your_password@ep-xxx.neon.tech/neondb?sslmode=require
```

### 3. Run the Setup Script

```bash
cd backend
chmod +x setup_neon.sh
./setup_neon.sh
```

This script will:
- ✅ Check Python installation
- ✅ Create/activate virtual environment
- ✅ Install dependencies
- ✅ Test database connection
- ✅ Initialize database schema

## Manual Setup (Alternative)

If you prefer manual setup:

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Test Connection

```bash
python test_neon_connection.py
```

### 3. Initialize Database

```bash
python init_neon_schema.py
```

### 4. Start the Application

```bash
uvicorn main:app --reload
```

## Database Schema

The following tables are automatically created:

### Core Tables

| Table | Description |
|-------|-------------|
| `patients` | User accounts and personal information |
| `doctors` | Healthcare provider profiles |
| `appointments` | Appointment bookings and schedules |
| `doctor_availability` | Doctor working hours by day |
| `medical_records` | Patient medical documents |
| `prescriptions` | Medication prescriptions |
| `voice_transcripts` | AI voice agent conversation logs |
| `notifications` | User notifications |

### Key Features

- 🔐 **Foreign key constraints** ensure data integrity
- 📊 **Indexes** on frequently queried columns for performance
- 🔄 **Automatic timestamps** with triggers
- 🆔 **Auto-incrementing IDs** with SERIAL type
- 🔒 **UNIQUE constraints** prevent duplicate entries

## Database Utilities

### Connection Helper

```python
from db import get_db_connection

# Get a connection
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM patients")
results = cursor.fetchall()
cursor.close()
conn.close()
```

### Context Manager (Recommended)

```python
from db import get_db_cursor

# Automatically handles commit/rollback
with get_db_cursor() as cursor:
    cursor.execute("INSERT INTO patients (...) VALUES (...)")
    # Auto-commits on success, auto-rolls back on error
```

### Execute Query Helper

```python
from db import execute_query

# Fetch results
patients = execute_query("SELECT * FROM patients WHERE id = %s", (patient_id,))

# Execute without fetching
execute_query("UPDATE patients SET name = %s WHERE id = %s", 
              ("John Doe", 1), fetch=False)
```

## Neon Features

### Database Branching

Create isolated database branches for testing:

```bash
# In Neon Console
1. Go to your project
2. Click "Branches"
3. Click "New Branch"
4. Use the branch connection string for testing
```

### Connection Pooling

Neon includes built-in connection pooling. Use the pooler endpoint:

```
postgresql://user:pass@ep-xxx-pooler.neon.tech/dbname
```

### Monitoring

View your database metrics in the Neon Console:
- Active connections
- Query performance
- Storage usage
- Compute time

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NEON_DATABASE_URL` | Yes | Full PostgreSQL connection string |
| `DB_HOST` | No | Fallback: Database host |
| `DB_PORT` | No | Fallback: Database port (default: 5432) |
| `DB_NAME` | No | Fallback: Database name |
| `DB_USER` | No | Fallback: Database user |
| `DB_PASSWORD` | No | Fallback: Database password |

**Note**: If `NEON_DATABASE_URL` is set, it takes priority over individual parameters.

## Troubleshooting

### Connection Timeout

```
Error: connection timeout
```

**Solutions**:
1. Check your internet connection
2. Verify the connection string is correct
3. Ensure your Neon project is active (not suspended)

### SSL Required Error

```
Error: SSL connection is required
```

**Solution**: Ensure your connection string includes `?sslmode=require`:
```
postgresql://user:pass@host/db?sslmode=require
```

### Table Already Exists

```
Error: relation "patients" already exists
```

**Solution**: This is normal if running `init_neon_schema.py` multiple times. The script uses `CREATE TABLE IF NOT EXISTS`.

### Authentication Failed

```
Error: password authentication failed
```

**Solutions**:
1. Reset your password in Neon Console
2. Copy the new connection string
3. Update `.env` file

## Migration from Local PostgreSQL

If you're migrating from a local PostgreSQL database:

### 1. Export Data

```bash
pg_dump -U postgres healthcare > backup.sql
```

### 2. Import to Neon

```bash
psql "postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require" < backup.sql
```

### 3. Update Connection

Update `NEON_DATABASE_URL` in `.env` file.

## Performance Tips

1. **Use connection pooling** - Include `-pooler` in your host
2. **Add indexes** - Already included for common queries
3. **Use transactions** - Batch multiple operations
4. **Optimize queries** - Use EXPLAIN ANALYZE to check query plans

## Security Best Practices

1. ✅ **Never commit `.env`** - Already in `.gitignore`
2. ✅ **Use environment variables** - No hardcoded credentials
3. ✅ **Enable SSL** - Required by default in Neon
4. ✅ **Rotate passwords** - Regenerate periodically in Neon Console
5. ✅ **Use read-only roles** - For reporting/analytics queries

## Support

- 📖 [Neon Documentation](https://neon.tech/docs)
- 💬 [Neon Discord Community](https://discord.gg/neon)
- 🐛 [Report Issues](https://github.com/your-repo/issues)

## Cost Optimization

### Free Tier Limits
- Storage: 0.5 GB
- Compute: 100 hours/month
- Always-on: No (scales to zero)

### Tips to Stay in Free Tier
1. ✅ Let database scale to zero when idle
2. ✅ Use connection pooling to reduce compute time
3. ✅ Optimize queries to run faster
4. ✅ Delete old logs and test data periodically

## Next Steps

1. ✅ Test the connection: `python test_neon_connection.py`
2. ✅ Initialize schema: `python init_neon_schema.py`
3. ✅ Start your app: `uvicorn main:app --reload`
4. 📚 Read the [API Documentation](http://localhost:8000/docs)

---

**Need Help?** Check the troubleshooting section or open an issue on GitHub.
