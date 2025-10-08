"""
Script to test Neon DB connection
"""

from db import get_db_connection, execute_query
from config import Config

def test_connection():
    """Test database connection"""
    print("🔍 Testing Neon DB Connection...")
    print("=" * 60)
    
    # Check configuration
    if Config.NEON_DATABASE_URL:
        print("✅ Using Neon DATABASE_URL")
        print(f"   Connection: {Config.NEON_DATABASE_URL[:50]}...")
    else:
        print("⚠️  Using individual DB parameters")
        print(f"   Host: {Config.DB_HOST}")
        print(f"   Database: {Config.DB_NAME}")
        print(f"   User: {Config.DB_USER}")
    
    print("\n🔌 Attempting connection...")
    
    try:
        conn = get_db_connection()
        print("✅ Connection successful!")
        
        # Test a simple query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        print(f"\n📊 PostgreSQL Version:")
        print(f"   {version}")
        
        # Test execute_query helper
        print("\n🧪 Testing query helpers...")
        result = execute_query("SELECT current_database(), current_user;")
        print(f"✅ Current database: {result[0]['current_database']}")
        print(f"✅ Current user: {result[0]['current_user']}")
        
        # List existing tables
        print("\n📋 Existing tables:")
        tables = execute_query("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        
        if tables:
            for table in tables:
                print(f"   • {table['table_name']}")
        else:
            print("   (No tables found - run init_neon_schema.py to create them)")
        
        print("\n" + "=" * 60)
        print("✅ All tests passed! Your Neon DB is ready to use.")
        return True
        
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Check your .env file has NEON_DATABASE_URL")
        print("   2. Verify the connection string format:")
        print("      postgresql://user:pass@host/dbname?sslmode=require")
        print("   3. Ensure your Neon project is active")
        print("   4. Check your IP is allowed (Neon allows all by default)")
        return False

if __name__ == "__main__":
    test_connection()
