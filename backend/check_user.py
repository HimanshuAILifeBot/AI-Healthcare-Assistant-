"""
Check user in database
"""
from db import get_db_connection

def check_user():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Check if user exists
    cur.execute("""
        SELECT id, name, email, password_hash 
        FROM patients 
        WHERE email = 'himanshujha7489@gmail.com'
    """)
    
    user = cur.fetchone()
    if user:
        print(f"✅ User found:")
        print(f"   ID: {user['id']}")
        print(f"   Name: {user['name']}")
        print(f"   Email: {user['email']}")
        print(f"   Password Hash: {user['password_hash']}")
    else:
        print("❌ User not found")
    
    # Also test the stored procedure
    print("\n" + "="*60)
    print("Testing stored procedure:")
    cur.execute("SELECT * FROM sp_login_user(%s, %s)", 
                ('himanshujha7489@gmail.com', '12345'))
    result = cur.fetchone()
    
    if result:
        print(f"✅ Stored procedure returned:")
        print(f"   Result: {result}")
    else:
        print("❌ Stored procedure returned no results")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    check_user()
