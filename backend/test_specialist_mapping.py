"""
Test script to verify specialist mapping
"""
from langgraph_llm_agents import find_matching_specialization

# Simulated database specializations (based on your logs)
db_specializations = [
    'Hematology', 'Infectious Disease', 'Ophthalmology', 'Cardiology', 
    'Gastroenterology', 'Pulmonology', 'Pathology', 'Geriatrics', 'Urology', 
    'General Surgery', 'Physical Medicine & Rehabilitation', 'Plastic Surgery', 
    'Neurology', 'Anesthesiology', 'Pediatrics', 'Otolaryngology', 'Psychiatry', 
    'Dermatology', 'Oncology', 'Obstetrics and Gynecology', 'Emergency Medicine', 
    'Orthopedics', 'Radiology', 'Rheumatology', 'Nephrology', 'Endocrinology', 
    'Family Medicine', 'Allergist/Immunologist'
]

# Test cases
test_specialists = [
    'Neurologist',
    'Pediatrician',
    'Cardiologist',
    'Dermatologist',
    'Orthopedist',
    'Brain Specialist',
    'Heart Doctor',
    'Skin Doctor',
    'Child Doctor'
]

print("=" * 70)
print("SPECIALIST MAPPING TEST")
print("=" * 70)

success_count = 0
fail_count = 0

for specialist in test_specialists:
    result = find_matching_specialization(specialist, db_specializations)
    if result:
        print(f"✅ '{specialist}' -> '{result}'")
        success_count += 1
    else:
        print(f"❌ '{specialist}' -> NO MATCH FOUND")
        fail_count += 1

print("\n" + "=" * 70)
print(f"RESULTS: {success_count} successful, {fail_count} failed")
print("=" * 70)

# Specific test for the issue
print("\n" + "=" * 70)
print("TESTING THE REPORTED ISSUE:")
print("=" * 70)

reported_specialists = ['Neurologist', 'Pediatrician']
print(f"Input specialists: {reported_specialists}")
print()

mapped = []
for specialist in reported_specialists:
    result = find_matching_specialization(specialist, db_specializations)
    if result:
        print(f"✅ '{specialist}' successfully mapped to '{result}'")
        mapped.append(result)
    else:
        print(f"❌ '{specialist}' FAILED to map")

print()
print(f"Expected: ['Neurology', 'Pediatrics']")
print(f"Got: {mapped}")
print()

if len(mapped) == 2 and 'Neurology' in mapped and 'Pediatrics' in mapped:
    print("✅ TEST PASSED: Both specialists mapped correctly!")
else:
    print("❌ TEST FAILED: Mapping incomplete or incorrect")
