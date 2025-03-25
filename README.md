# Student Performance Predictor

A machine learning web application to predict student performance based on attendance and subject marks.

## Overview

This system uses machine learning to predict student academic performance across five engineering subjects:

1. Engineering Mathematics 3
2. Microprocessor
3. Principles of Programming Language
4. Software Engineering
5. Data Structure and Algorithm

The system analyzes attendance and individual subject marks to predict the overall student performance category as:
- Excellent
- Very Good
- Good
- Average
- Below Average

## Features

- **Random Student Data Generation**: Creates a dataset of 100 Indian students with randomly generated but realistic academic data
- **Performance Prediction**: Predicts student performance using a Random Forest classifier
- **Data Visualization**: Provides insightful visualizations about student performance patterns
- **Interactive Dashboard**: Shows performance metrics and analytics
- **Student Management**: Lists all students with filtering capabilities

## Project Structure

```
├── app.py                     # Main Flask application
├── data_generator.py          # Generates random student data
├── model.py                   # Machine learning model for performance prediction
├── visualization.py           # Data visualization module
├── data/                      # Data storage
│   └── student_data.csv       # Generated student dataset
├── models/                    # Saved ML models
│   └── student_performance_model.pkl
│   └── student_performance_scaler.pkl
├── app/                       # Web application
│   ├── static/                # Static files (CSS, JS, images)
│   │   └── images/            # Visualization images
│   └── templates/             # HTML templates
│       ├── base.html          # Base template
│       ├── index.html         # Home page
│       ├── predict.html       # Prediction page
│       ├── dashboard.html     # Dashboard page
│       └── students.html      # Student listing page
└── requirements.txt           # Project dependencies
```

## Technologies Used

- **Python**: Core programming language
- **Flask**: Web framework
- **Pandas & NumPy**: Data manipulation
- **Scikit-learn**: Machine learning model
- **Matplotlib & Seaborn**: Data visualization
- **Bootstrap**: Frontend framework
- **Chart.js**: Interactive charts

## Installation & Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/student-performance-predictor.git
   cd student-performance-predictor
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Usage

1. **Home Page**: View system overview and summary statistics
2. **Predict Page**: Enter student details to predict their performance
3. **Dashboard**: Explore visualizations and performance analytics
4. **Students Page**: View and search through the list of students

## Model Details

The system uses a Random Forest Classifier that:
- Takes attendance and subject marks as input features
- Predicts performance categories based on learned patterns
- Provides probability estimates for each performance category

## Data Generation

The system generates random but realistic student data with:
- Indian names
- Attendance percentages between 55% and 100%
- Subject marks influenced by attendance (with random variation)
- Performance categories based on overall percentage

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The project uses a machine learning approach to educational data mining
- The UI is built with Bootstrap for responsive design
- Data visualizations are created with Matplotlib and Seaborn