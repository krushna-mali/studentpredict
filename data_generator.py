import pandas as pd
import numpy as np
import random

# List of Indian names
first_names = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Reyansh", "Ayaan", "Atharva", 
    "Krishna", "Ishaan", "Shaurya", "Advait", "Dhruv", "Kabir", "Ritvik", "Aarush", 
    "Kayaan", "Darsh", "Veer", "Samar", "Siddharth", "Shreyash", "Arnav", "Pranav", 
    "Aryan", "Aanya", "Aadhya", "Anika", "Ananya", "Diya", "Saanvi", "Sara", "Ahana", 
    "Aarohi", "Anvi", "Prisha", "Riya", "Ira", "Myra", "Saisha", "Shanaya", "Meera", 
    "Amyra", "Pari", "Aisha", "Kiara", "Zara", "Siya", "Navya", "Trisha"
]

last_names = [
    "Sharma", "Singh", "Kumar", "Patel", "Rao", "Verma", "Reddy", "Joshi", "Gupta", 
    "Malhotra", "Shah", "Bansal", "Kapoor", "Chopra", "Khanna", "Arora", "Das", 
    "Chatterjee", "Patil", "Mittal", "Mehta", "Bose", "Sengupta", "Chauhan", "Bhatia", 
    "Datta", "Sinha", "Desai", "Nair", "Agarwal", "Mukherjee", "Yadav", "Chauhan", 
    "Trivedi", "Dubey", "Mehra", "Pandey", "Anand", "Iyer", "Varma", "Mishra", "Jain"
]

# Generate 100 student records
np.random.seed(42)  # For reproducibility
num_students = 100

# Student IDs
student_ids = [f"S{str(i+1).zfill(3)}" for i in range(num_students)]

# Generate names
names = []
for _ in range(num_students):
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    names.append(f"{first_name} {last_name}")

# Generate attendance (55% to 100%)
attendance = np.random.randint(55, 101, size=num_students)

# Generate marks for each subject (0 to 100)
subjects = [
    "Engineering_Maths_3", 
    "Microprocessor", 
    "Principles_of_Programming_Language", 
    "Software_Engineering", 
    "Data_Structure_and_Algorithm"
]

# Dictionary to store data
data = {
    "Student_ID": student_ids,
    "Name": names,
    "Attendance_Percentage": attendance
}

# Generate marks for each subject
for subject in subjects:
    # Higher attendance generally correlates with better marks
    # Base marks influenced by attendance
    base_marks = np.clip(attendance * 0.7 + np.random.normal(15, 10, num_students), 0, 100)
    data[f"{subject}_Marks"] = np.round(base_marks).astype(int)

# Create DataFrame
df = pd.DataFrame(data)

# Calculate total marks and percentage
total_marks = df[[f"{subject}_Marks" for subject in subjects]].sum(axis=1)
percentage = total_marks / 5  # 5 subjects, each with max 100 marks

df["Total_Marks"] = total_marks
df["Percentage"] = percentage

# Add a performance category
def assign_performance(percentage):
    if percentage >= 80:
        return "Excellent"
    elif percentage >= 70:
        return "Very Good"
    elif percentage >= 60:
        return "Good"
    elif percentage >= 50:
        return "Average"
    else:
        return "Below Average"

df["Performance"] = df["Percentage"].apply(assign_performance)

# Save the dataset
df.to_csv("data/student_data.csv", index=False)

print(f"Generated dataset for {num_students} students and saved to data/student_data.csv") 