# collections_demo.py
# TASK 6: Lists, Tuples & Sets

print("====== PYTHON COLLECTIONS DEMO ======\n")

# --------------------------------------------------
# 1. LIST: Store student names (Mutable)
# --------------------------------------------------
students = ["Narayan", "Anita", "Ravi", "Priya", "Ravi"]

print("Original student list:")
print(students, "\n")

# Add elements
students.append("Kiran")
print("After adding a student:")
print(students, "\n")

# Remove elements
students.remove("Anita")
print("After removing a student:")
print(students, "\n")

# Sort elements
students.sort()
print("After sorting students:")
print(students, "\n")

# Iterate over list
print("Iterating over student list:")
for student in students:
    print(f"- {student}")
print()

# --------------------------------------------------
# 2. TUPLE: Fixed data (Immutable)
# --------------------------------------------------
course_info = ("Python Programming", 3, "Months")

print("Course information (Tuple):")
print(course_info)

print("\nAccessing tuple elements:")
print("Course Name:", course_info[0])
print("Duration:", course_info[1], course_info[2])

# Uncommenting below line will cause an error (immutable)
# course_info[0] = "Data Science"

print("\nTuples are IMMUTABLE (cannot be changed).\n")

# --------------------------------------------------
# 3. SET: Remove duplicates
# --------------------------------------------------
student_set = set(students)

print("Converted list to set (duplicates removed):")
print(student_set, "\n")

# Add element to set
student_set.add("Suresh")
print("After adding to set:")
print(student_set, "\n")

# --------------------------------------------------
# 4. SET OPERATIONS
# --------------------------------------------------
online_students = {"Narayan", "Ravi", "Suresh"}
offline_students = {"Priya", "Kiran", "Ravi"}

print("Online Students:", online_students)
print("Offline Students:", offline_students, "\n")

# Union
print("Union (All students):")
print(online_students | offline_students, "\n")

# Intersection
print("Intersection (Common students):")
print(online_students & offline_students, "\n")

# Difference
print("Difference (Online but not Offline):")
print(online_students - offline_students, "\n")

# --------------------------------------------------
# 5. MUTABLE vs IMMUTABLE COMPARISON
# --------------------------------------------------
print("====== MUTABLE vs IMMUTABLE ======")
print("List  -> Mutable  (Can be modified)")
print("Tuple -> Immutable (Cannot be modified)")
print("Set   -> Mutable  (No duplicates, unordered)")

print("\n====== END OF DEMO ======")
