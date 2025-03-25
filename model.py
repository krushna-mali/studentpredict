import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib

class StudentPerformanceModel:
    def __init__(self):
        self.model = RandomForestClassifier(random_state=42)
        self.scaler = StandardScaler()
        self.features = [
            'Attendance_Percentage',
            'Engineering_Maths_3_Marks',
            'Microprocessor_Marks',
            'Principles_of_Programming_Language_Marks',
            'Software_Engineering_Marks',
            'Data_Structure_and_Algorithm_Marks'
        ]
        self.target = 'Performance'
        
    def prepare_data(self, df):
        """Prepare data for model training/prediction"""
        X = df[self.features]
        
        if self.target in df.columns:
            y = df[self.target]
            # During training, fit and transform
            if not hasattr(self.scaler, 'n_features_in_'):
                X_scaled = self.scaler.fit_transform(X)
            else:
                X_scaled = self.scaler.transform(X)
            return X_scaled, y
        else:
            # During prediction, only transform
            if not hasattr(self.scaler, 'n_features_in_'):
                raise ValueError("Scaler is not fitted. Please train the model first.")
            X_scaled = self.scaler.transform(X)
            return X_scaled
        
    def train(self, data_path='data/student_data.csv'):
        """Train the model with student data"""
        # Load data
        df = pd.read_csv(data_path)
        
        # Split data
        X, y = self.prepare_data(df)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Fit model
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        
        print(f"Model Accuracy: {accuracy:.4f}")
        print("Classification Report:")
        print(report)
        
        # Save model for future use
        self.save_model()
        
        return accuracy, report
    
    def predict(self, student_data):
        """Predict performance for new student data
        
        Args:
            student_data: DataFrame containing student features
            
        Returns:
            Dictionary with predicted performance and probabilities
        """
        # Make sure all features are present
        for feature in self.features:
            if feature not in student_data.columns:
                raise ValueError(f"Missing feature: {feature}")
        
        # Extract and scale features
        X = student_data[self.features]
        
        # Ensure scaler is fitted
        if not hasattr(self.scaler, 'n_features_in_'):
            raise ValueError("Scaler is not fitted. Please train the model first.")
            
        X_scaled = self.scaler.transform(X)
        
        # Make prediction
        predicted_class = self.model.predict(X_scaled)[0]
        probabilities = self.model.predict_proba(X_scaled)[0]
        
        # Get class names and their corresponding probabilities
        classes = self.model.classes_
        class_probabilities = {cls: prob for cls, prob in zip(classes, probabilities)}
        
        return {
            "predicted_performance": predicted_class,
            "probabilities": class_probabilities
        }
    
    def save_model(self, model_path='models/'):
        """Save model to disk"""
        import os
        if not os.path.exists(model_path):
            os.makedirs(model_path)
        
        joblib.dump(self.model, f"{model_path}/student_performance_model.pkl")
        joblib.dump(self.scaler, f"{model_path}/student_performance_scaler.pkl")
        print(f"Model saved to {model_path}")
    
    def load_model(self, model_path='models/'):
        """Load model from disk"""
        self.model = joblib.load(f"{model_path}/student_performance_model.pkl")
        self.scaler = joblib.load(f"{model_path}/student_performance_scaler.pkl")
        print("Model loaded successfully")

# Example usage
if __name__ == "__main__":
    # Check if dataset exists, generate if it doesn't
    import os
    if not os.path.exists('data/student_data.csv'):
        import data_generator
    
    # Train model
    model = StudentPerformanceModel()
    model.train() 