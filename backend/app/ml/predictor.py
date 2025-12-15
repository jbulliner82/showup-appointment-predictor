"""
Machine Learning predictor for appointment no-shows
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from datetime import datetime
import joblib
import os

class NoShowPredictor:
    def __init__(self):
        self.model = None
        self.model_path = "app/ml/noshow_model.pkl"
        
    def prepare_features(self, appointments_df, patients_df):
        """
        Extract features from appointment and patient data.
        """
        # Merge appointments with patient history
        data = appointments_df.merge(
            patients_df[['id', 'noshow_rate', 'total_appointments', 'is_new_patient']], 
            left_on='patient_id', 
            right_on='id',
            how='left'
        )
        
        # Extract time-based features
        data['appointment_datetime'] = pd.to_datetime(data['appointment_datetime'])
        data['day_of_week'] = data['appointment_datetime'].dt.dayofweek  # 0=Monday, 6=Sunday
        data['hour_of_day'] = data['appointment_datetime'].dt.hour
        data['is_morning'] = (data['hour_of_day'] < 12).astype(int)
        data['is_monday'] = (data['day_of_week'] == 0).astype(int)
        data['is_friday'] = (data['day_of_week'] == 4).astype(int)
        
        # Patient history features
        data['patient_noshow_rate'] = data['noshow_rate'].fillna(0)
        data['patient_appointment_count'] = data['total_appointments'].fillna(0)
        data['is_new_patient_int'] = data['is_new_patient'].fillna(True).astype(int)
        
        # Select features for model
        feature_columns = [
            'day_of_week',
            'hour_of_day', 
            'is_morning',
            'is_monday',
            'is_friday',
            'patient_noshow_rate',
            'patient_appointment_count',
            'is_new_patient_int'
        ]
        
        X = data[feature_columns]
        y = data['did_noshow'].astype(int) if 'did_noshow' in data.columns else None
        
        return X, y, feature_columns
    
    def train(self, appointments_df, patients_df):
        """
        Train the no-show prediction model.
        """
        print("Preparing features...")
        X, y, feature_columns = self.prepare_features(appointments_df, patients_df)
        
        # Remove rows with missing target
        valid_mask = ~y.isna()
        X = X[valid_mask]
        y = y[valid_mask]
        
        print(f"Training on {len(X)} appointments...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model = LogisticRegression(random_state=42, max_iter=1000)
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1_score': f1_score(y_test, y_pred)
        }
        
        print(f"Model trained!")
        print(f"Accuracy: {metrics['accuracy']:.2%}")
        print(f"Precision: {metrics['precision']:.2%}")
        print(f"Recall: {metrics['recall']:.2%}")
        
        # Save model
        self.save_model()
        
        return metrics
    
    def predict(self, appointment_data, patient_data):
        """
        Predict no-show risk for a single appointment.
        """
        if self.model is None:
            self.load_model()
            
        # Create DataFrames
        apt_df = pd.DataFrame([appointment_data])
        pat_df = pd.DataFrame([patient_data])
        
        # Prepare features
        X, _, _ = self.prepare_features(apt_df, pat_df)
        
        # Get probability
        probability = self.model.predict_proba(X)[0][1]  # Probability of no-show
        risk_score = int(probability * 100)
        
        # Classify risk level
        if risk_score >= 70:
            risk_level = "high"
        elif risk_score >= 40:
            risk_level = "medium"
        else:
            risk_level = "low"
            
        return {
            'probability': probability,
            'risk_score': risk_score,
            'risk_level': risk_level
        }
    
    def save_model(self):
        """Save trained model to disk."""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        print(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """Load trained model from disk."""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            print(f"Model loaded from {self.model_path}")
        else:
            raise FileNotFoundError("No trained model found. Please train the model first.")