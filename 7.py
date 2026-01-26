# student_records.py

import json

# Step 1: Create a dictionary to store student records
student_records = {
    101: {
        "name": "Amit",
        "age": 20,
        "course": "Computer Science",
        "grade": "A"
    },
    102: {
        "name": "Sneha",
        "age": 21,
        "course": "Information Technology",
        "grade": "B"
    },
    103: {
        "name": "Rahul",
        "age": 19,
        "course": "Electronics",
        "grade": "A+"
    }
}
print("Student IDs:", student_records.keys())
print("Student Details:")
print(student_records[101])
# Update grade
student_records[102]["grade"] = "A"

# Delete a student record
del student_records[103]
print("\nAll Student Records:")
for student_id, details in student_records.items():
    print(f"ID: {student_id}")
    for key, value in details.items():
        print(f"  {key}: {value}")
json_data = json.dumps(student_records, indent=4)
print("\nJSON Format:")
print(json_data)
with open("student_records.json", "w") as file:
    file.write(json_data)

print("\nData saved to student_records.json")
with open("student_records.json", "r") as file:
    loaded_data = json.load(file)
print("\nLoaded Data from JSON File:")
for student_id, details in loaded_data.items():
    print(f"\nStudent ID: {student_id}")
    print(f"Name  : {details['name']}")
    print(f"Age   : {details['age']}")
    print(f"Course: {details['course']}")
    print(f"Grade : {details['grade']}")
