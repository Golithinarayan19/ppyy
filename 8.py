# -------------------------------
# TXT FILE HANDLING
# -------------------------------

try:
    # 1. Create and write to a text file
    with open("users.txt", "w") as file:
        file.write("Name: Narayan\n")
        file.write("Role: Intern\n")
        file.write("Department: Data Science\n")

    print("Text file created and data written successfully.\n")

    # 2. Read file contents
    with open("users.txt", "r") as file:
        content = file.read()
        print("Reading from users.txt:")
        print(content)

    # 3. Append data to file
    with open("users.txt", "a") as file:
        file.write("Status: Active\n")

    print("Data appended successfully.\n")

except FileNotFoundError:
    print("File not found!")
except IOError:
    print("An I/O error occurred!")
# -------------------------------
# CSV FILE HANDLING
# -------------------------------

import csv

try:
    # 4. Create and write to a CSV file
    with open("students.csv", "w", newline="") as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow(["ID", "Name", "Age", "Course"])

        # Write multiple rows
        writer.writerow([1, "Anita", 21, "AI"])
        writer.writerow([2, "Rahul", 22, "ML"])
        writer.writerow([3, "Sneha", 20, "Data Science"])

    print("CSV file created and data written successfully.\n")

    # 5. Read CSV data
    with open("students.csv", "r") as file:
        reader = csv.reader(file)
        print("Reading from students.csv:")
        for row in reader:
            print(row)

except Exception as e:
    print("Error:", e)
