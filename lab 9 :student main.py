# main.py

# Import the student module
import student

# Access and display the information using the module name prefix
print("--- Student Information Report ---")
print(f"Name:            {student.name}")
print(f"Register Number: {student.register_number}")
print(f"Course:          {student.course}")
print("\n--- Marks Obtained ---")

# Loop through the marks dictionary stored in the module
for subject, score in student.marks.items():
    print(f"{subject}: {score}/100")
