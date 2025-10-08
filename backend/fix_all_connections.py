"""Fix all database connection issues in main.py"""

import re

# Read the file
with open('main.py', 'r') as f:
    content = f.read()

# Replace the old pattern of cur = conn.cursor() with context manager
# This is a simple replacement - we'll do more specific fixes if needed

# Pattern for simple cursor usage
old_patterns = [
    (r'cur = conn\.cursor\(\)', 'with get_db_cursor() as cur:'),
    (r'conn\.commit\(\)\s*\n\s*cur\.close\(\)', '# Auto-committed by context manager'),
    (r'conn\.rollback\(\)\s*\n\s*cur\.close\(\)', '# Auto-rolled back by context manager'),
    (r'cur\.close\(\)', '# Closed by context manager'),
]

for old, new in old_patterns:
    content = re.sub(old, new, content)

# Write back
with open('main.py', 'w') as f:
    f.write(content)

print("✅ Fixed database connection patterns")
