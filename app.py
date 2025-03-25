import os
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, redirect, url_for
import joblib

# Custom modules
from model import StudentPerformanceModel
from visualization import StudentPerformanceVisualizer

app = Flask(__name__, 
            static_folder='app/static',
            template_folder='app/templates')

# Check if dataset exists, generate if it doesn't
if not os.path.exists('data/student_data.csv'):
    import data_generator

# Check if model directory exists, create if it doesn't
if not os.path.exists('models'):
    os.makedirs('models')

# Check if static images directory exists, create if it doesn't
if not os.path.exists('app/static/images'):
    os.makedirs('app/static/images')

# Load dataset
try:
    df = pd.read_csv('data/student_data.csv')
except:
    raise Exception("Could not load dataset. Please generate it first using data_generator.py")

# Generate visualizations if they don't exist
if not os.path.exists('app/static/images/performance_distribution.png'):
    visualizer = StudentPerformanceVisualizer()
    visualizer.generate_all_visualizations()

# Initialize and train model if it doesn't exist
model = StudentPerformanceModel()
if not os.path.exists('models/student_performance_model.pkl'):
    model.train()
else:
    model.load_model()

# Helper function to get subject name from column name
def get_readable_subject_name(col_name):
    return col_name.replace('_Marks', '').replace('_', ' ')

@app.route('/')
def index():
    """Home page"""
    # Calculate statistics for the dashboard
    student_count = len(df)
    avg_attendance = round(df['Attendance_Percentage'].mean(), 2)
    avg_percentage = round(df['Percentage'].mean(), 2)
    excellent_count = len(df[df['Performance'] == 'Excellent'])
    
    return render_template('index.html', 
                          student_count=student_count,
                          avg_attendance=avg_attendance,
                          avg_percentage=avg_percentage,
                          excellent_count=excellent_count)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Prediction page"""
    if request.method == 'POST':
        # Get form data
        student_name = request.form['student_name']
        attendance = int(request.form['attendance'])
        engineering_maths = int(request.form['engineering_maths'])
        microprocessor = int(request.form['microprocessor'])
        programming = int(request.form['programming'])
        software_engineering = int(request.form['software_engineering'])
        dsa = int(request.form['dsa'])
        
        # Calculate total and percentage
        total_marks = engineering_maths + microprocessor + programming + software_engineering + dsa
        percentage = total_marks / 5
        
        # Create a DataFrame for prediction
        student_data = pd.DataFrame({
            'Attendance_Percentage': [attendance],
            'Engineering_Maths_3_Marks': [engineering_maths],
            'Microprocessor_Marks': [microprocessor],
            'Principles_of_Programming_Language_Marks': [programming],
            'Software_Engineering_Marks': [software_engineering],
            'Data_Structure_and_Algorithm_Marks': [dsa]
        })
        
        # Make prediction
        prediction = model.predict(student_data)
        
        # Find lowest scoring subject
        subject_marks = {
            'Engineering Maths 3': engineering_maths,
            'Microprocessor': microprocessor,
            'Principles of Programming Language': programming,
            'Software Engineering': software_engineering,
            'Data Structure and Algorithm': dsa
        }
        lowest_subject = min(subject_marks, key=subject_marks.get)
        
        return render_template('predict.html',
                              prediction=prediction,
                              student_name=student_name,
                              attendance=attendance,
                              engineering_maths=engineering_maths,
                              microprocessor=microprocessor,
                              programming=programming,
                              software_engineering=software_engineering,
                              dsa=dsa,
                              total_marks=total_marks,
                              percentage=round(percentage, 2),
                              lowest_subject=lowest_subject)
    
    return render_template('predict.html')

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    # Calculate statistics for the dashboard
    student_count = len(df)
    avg_attendance = round(df['Attendance_Percentage'].mean(), 2)
    avg_percentage = round(df['Percentage'].mean(), 2)
    excellent_count = len(df[df['Performance'] == 'Excellent'])
    
    # Calculate average marks for each subject
    subject_cols = [col for col in df.columns if col.endswith('_Marks')]
    subject_avgs = {get_readable_subject_name(col): round(df[col].mean(), 2) for col in subject_cols}
    
    # Find highest and lowest average scoring subjects
    highest_subject = max(subject_avgs, key=subject_avgs.get)
    lowest_subject = min(subject_avgs, key=subject_avgs.get)
    highest_subject_avg = subject_avgs[highest_subject]
    lowest_subject_avg = subject_avgs[lowest_subject]
    
    return render_template('dashboard.html',
                          student_count=student_count,
                          avg_attendance=avg_attendance,
                          avg_percentage=avg_percentage,
                          excellent_count=excellent_count,
                          highest_subject=highest_subject,
                          lowest_subject=lowest_subject,
                          highest_subject_avg=highest_subject_avg,
                          lowest_subject_avg=lowest_subject_avg)

@app.route('/students')
def students():
    """Students list page"""
    # Get performance counts
    performance_counts = df['Performance'].value_counts().to_dict()
    
    # Get top performers (top 5 students by percentage)
    top_performers = df.sort_values('Percentage', ascending=False).head(5)
    
    return render_template('students.html',
                          students=df.to_dict('records'),
                          performance_counts=performance_counts,
                          top_performers=top_performers.to_dict('records'))

if __name__ == '__main__':
    app.run(debug=True) 