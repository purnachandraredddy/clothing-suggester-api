#!/usr/bin/env python3
"""
Clothing Recommendation Model Training Script

This script generates synthetic weather data and trains a decision tree classifier
to predict clothing suggestions based on temperature, humidity, and wind speed.
"""

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

def generate_synthetic_data(n_samples=1000):
    """
    Generate synthetic weather data with clothing labels.
    
    Args:
        n_samples (int): Number of samples to generate
        
    Returns:
        pd.DataFrame: DataFrame with weather features and clothing labels
    """
    np.random.seed(42)  # For reproducibility
    
    # Generate weather features
    temperature = np.random.uniform(-5, 35, n_samples)
    humidity = np.random.uniform(20, 100, n_samples)
    wind_speed = np.random.uniform(0, 20, n_samples)
    
    # Create DataFrame
    data = pd.DataFrame({
        'temperature': temperature,
        'humidity': humidity,
        'wind_speed': wind_speed
    })
    
    # Apply rule-based logic to assign clothing labels
    def assign_clothing(row):
        temp = row['temperature']
        wind = row['wind_speed']
        
        # Base clothing on temperature
        if temp >= 20:
            return 'T-shirt'
        elif temp >= 10:
            return 'Light jacket'
        else:
            return 'Coat'
    
    data['clothing'] = data.apply(assign_clothing, axis=1)
    
    return data

def train_model(data):
    """
    Train a decision tree classifier on the weather data.
    
    Args:
        data (pd.DataFrame): Training data with features and labels
        
    Returns:
        tuple: (trained_model, X_test, y_test, accuracy)
    """
    # Prepare features and target
    X = data[['temperature', 'humidity', 'wind_speed']]
    y = data['clothing']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Train the model
    model = DecisionTreeClassifier(
        max_depth=5,  # Limit depth to avoid overfitting
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    return model, X_test, y_test, accuracy

def save_model_and_data(model, data, model_path='model.joblib', data_path='data/synthetic_data.csv'):
    """
    Save the trained model and training data.
    
    Args:
        model: Trained model
        data (pd.DataFrame): Training data
        model_path (str): Path to save the model
        data_path (str): Path to save the data
    """
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    
    # Save the model
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
    
    # Save the data
    data.to_csv(data_path, index=False)
    print(f"Training data saved to {data_path}")

def main():
    """Main training pipeline."""
    print("🚀 Starting Clothing Recommendation Model Training")
    print("=" * 50)
    
    # Step 1: Generate synthetic data
    print("📊 Generating synthetic weather data...")
    data = generate_synthetic_data(n_samples=1000)
    print(f"Generated {len(data)} samples")
    print(f"Data distribution:\n{data['clothing'].value_counts()}")
    print()
    
    # Step 2: Train the model
    print("🤖 Training Decision Tree Classifier...")
    model, X_test, y_test, accuracy = train_model(data)
    print(f"Model accuracy: {accuracy:.3f}")
    print()
    
    # Step 3: Print detailed evaluation
    print("📈 Model Evaluation:")
    print("-" * 30)
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    # Step 4: Save model and data
    print("💾 Saving model and data...")
    save_model_and_data(model, data)
    
    # Step 5: Test predictions
    print("\n🧪 Testing sample predictions:")
    print("-" * 30)
    test_cases = [
        {'temperature': 25, 'humidity': 60, 'wind_speed': 3},  # Should be T-shirt
        {'temperature': 15, 'humidity': 50, 'wind_speed': 5},  # Should be Light jacket
        {'temperature': 5, 'humidity': 80, 'wind_speed': 10},  # Should be Coat
    ]
    
    for i, case in enumerate(test_cases, 1):
        prediction = model.predict([list(case.values())])[0]
        print(f"Test {i}: {case} → {prediction}")
    
    print("\n✅ Training completed successfully!")
    print("🎯 Model is ready for deployment via Flask API")

if __name__ == "__main__":
    main() 