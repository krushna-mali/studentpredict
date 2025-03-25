import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

class StudentPerformanceVisualizer:
    def __init__(self, data_path='data/student_data.csv'):
        self.data_path = data_path
        self.df = pd.read_csv(data_path)
        self.subjects = [
            'Engineering_Maths_3_Marks', 
            'Microprocessor_Marks', 
            'Principles_of_Programming_Language_Marks', 
            'Software_Engineering_Marks', 
            'Data_Structure_and_Algorithm_Marks'
        ]
        # Create output directory
        if not os.path.exists('app/static/images'):
            os.makedirs('app/static/images')

    def performance_distribution(self):
        """Generate performance distribution chart"""
        plt.figure(figsize=(10, 6))
        sns.countplot(x='Performance', data=self.df, palette='viridis')
        plt.title('Distribution of Student Performance', fontsize=16)
        plt.xlabel('Performance Category', fontsize=12)
        plt.ylabel('Number of Students', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save the figure
        output_path = 'app/static/images/performance_distribution.png'
        plt.savefig(output_path)
        plt.close()
        return output_path

    def attendance_vs_performance(self):
        """Generate attendance vs performance chart"""
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='Performance', y='Attendance_Percentage', data=self.df, palette='viridis')
        plt.title('Attendance vs Performance', fontsize=16)
        plt.xlabel('Performance Category', fontsize=12)
        plt.ylabel('Attendance Percentage', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save the figure
        output_path = 'app/static/images/attendance_vs_performance.png'
        plt.savefig(output_path)
        plt.close()
        return output_path

    def subject_performance(self):
        """Generate subject performance comparison chart"""
        # Melt the dataframe to get subjects in one column
        subject_cols = [col for col in self.df.columns if col.endswith('_Marks')]
        melted_df = pd.melt(self.df, 
                           id_vars=['Student_ID', 'Performance'], 
                           value_vars=subject_cols,
                           var_name='Subject', 
                           value_name='Marks')
        
        # Clean subject names for display
        melted_df['Subject'] = melted_df['Subject'].apply(lambda x: x.replace('_Marks', '').replace('_', ' '))
        
        plt.figure(figsize=(12, 8))
        sns.boxplot(x='Subject', y='Marks', hue='Performance', data=melted_df, palette='viridis')
        plt.title('Subject-wise Performance Comparison', fontsize=16)
        plt.xlabel('Subject', fontsize=12)
        plt.ylabel('Marks', fontsize=12)
        plt.xticks(rotation=45)
        plt.legend(title='Performance Category')
        plt.tight_layout()
        
        # Save the figure
        output_path = 'app/static/images/subject_performance.png'
        plt.savefig(output_path)
        plt.close()
        return output_path

    def correlation_heatmap(self):
        """Generate correlation heatmap between features"""
        # Select numerical columns
        numerical_cols = ['Attendance_Percentage'] + self.subjects + ['Total_Marks', 'Percentage']
        
        # Calculate correlation
        corr = self.df[numerical_cols].corr()
        
        plt.figure(figsize=(12, 10))
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', mask=mask)
        plt.title('Correlation Between Different Features', fontsize=16)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Save the figure
        output_path = 'app/static/images/correlation_heatmap.png'
        plt.savefig(output_path)
        plt.close()
        return output_path

    def attendance_marks_scatter(self):
        """Generate scatter plot for attendance vs total marks"""
        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            x='Attendance_Percentage', 
            y='Total_Marks',
            hue='Performance',
            size='Percentage',
            sizes=(50, 200),
            data=self.df,
            palette='viridis'
        )
        plt.title('Relationship Between Attendance and Total Marks', fontsize=16)
        plt.xlabel('Attendance Percentage', fontsize=12)
        plt.ylabel('Total Marks', fontsize=12)
        plt.grid(alpha=0.3)
        plt.tight_layout()
        
        # Save the figure
        output_path = 'app/static/images/attendance_marks_scatter.png'
        plt.savefig(output_path)
        plt.close()
        return output_path

    def generate_all_visualizations(self):
        """Generate all visualizations and return their paths"""
        paths = {}
        paths['performance_distribution'] = self.performance_distribution()
        paths['attendance_vs_performance'] = self.attendance_vs_performance()
        paths['subject_performance'] = self.subject_performance()
        paths['correlation_heatmap'] = self.correlation_heatmap()
        paths['attendance_marks_scatter'] = self.attendance_marks_scatter()
        return paths

# Example usage
if __name__ == "__main__":
    # Check if dataset exists, generate if it doesn't
    if not os.path.exists('data/student_data.csv'):
        import data_generator
    
    visualizer = StudentPerformanceVisualizer()
    paths = visualizer.generate_all_visualizations()
    print("Visualizations generated successfully!") 