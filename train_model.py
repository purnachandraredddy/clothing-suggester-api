#!/usr/bin/env python3
"""
Train Clothing Recommendation Model

This script generates synthetic weather data and trains a decision tree classifier
to recommend appropriate clothing based on weather conditions.
"""

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def generate_weather_data(n_samples=1000):
    """
    Generate synthetic weather data with realistic ranges.
    
    Args:
        n_samples (int): Number of samples to generate
        
    Returns:
        tuple: (features, labels)
    """
    np.random.seed(42)  # For reproducible results
    
    # Generate weather conditions
    temperature = np.random.uniform(-10, 40, n_samples)  # Celsius
    humidity = np.random.uniform(20, 95, n_samples)      # Percentage
    wind_speed = np.random.uniform(0, 30, n_samples)     # km/h
    
    # Create features DataFrame
    features = pd.DataFrame({
        'temperature': temperature,
        'humidity': humidity,
        'wind_speed': wind_speed
    })
    
    # Define clothing recommendations based on weather conditions
    labels = []
    
    for i in range(n_samples):
        temp = features.iloc[i]['temperature']
        humidity = features.iloc[i]['humidity']
        wind = features.iloc[i]['wind_speed']
        
        # ☀️ Hot Weather (Above 30°C / 86°F)
        if temp > 30:
            if humidity > 70:
                labels.append("Light cotton clothes, sandals, sunscreen, hat, stay hydrated")
            else:
                labels.append("Lightweight breathable clothes, sunglasses, light colors")
        
        # 🌤️ Warm Weather (20–30°C / 68–86°F)
        elif 20 <= temp <= 30:
            if wind > 15:
                labels.append("T-shirt with light jacket, secure footwear, hair tied up")
            elif humidity > 80:
                labels.append("Light clothes, deodorant, breathable fabrics")
            else:
                labels.append("T-shirts, jeans, sneakers, light cardigan for AC")
        
        # 🌧️ Rainy Weather (high humidity + moderate temp)
        elif humidity > 85 and 10 <= temp <= 25:
            labels.append("Waterproof jacket, quick-dry pants, rubber boots, umbrella")
        
        # ❄️ Cold Weather (Below 10°C / 50°F)
        elif temp < 10:
            if wind > 20:
                labels.append("Heavy winter coat, scarf, gloves, insulated boots, layered clothing")
            else:
                labels.append("Warm sweater, winter coat, dark colors, moisturizer")
        
        # 🌬️ Windy Weather (high wind + moderate temp)
        elif wind > 20 and 10 <= temp <= 25:
            labels.append("Windbreaker jacket, closed shoes, hair secured, protective eyewear")
        
        # 🌤️ Mild Weather (10-20°C / 50-68°F)
        elif 10 <= temp < 20:
            if humidity > 75:
                labels.append("Light jacket, quick-dry clothes, comfortable shoes")
            else:
                labels.append("Light sweater, jeans, sneakers, light layers")
        
        # Default for other conditions
        else:
            labels.append("Comfortable casual clothes, weather-appropriate footwear")
    
    return features, labels

def train_model(features, labels):
    """
    Train the decision tree classifier.
    
    Args:
        features (DataFrame): Weather features
        labels (list): Clothing recommendations
        
    Returns:
        DecisionTreeClassifier: Trained model
    """
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.2, random_state=42
    )
    
    # Create and train the model
    model = DecisionTreeClassifier(
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"✅ Model trained successfully!")
    print(f"📊 Accuracy: {accuracy:.2%}")
    print(f"📈 Training samples: {len(X_train)}")
    print(f"🧪 Test samples: {len(X_test)}")
    
    # Print detailed classification report
    print("\n📋 Classification Report:")
    print(classification_report(y_test, y_pred))
    
    return model

def save_model(model, filename='model.joblib'):
    """
    Save the trained model to disk.
    
    Args:
        model: Trained model
        filename (str): Output filename
    """
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Save model
    model_path = os.path.join('data', filename)
    joblib.dump(model, model_path)
    print(f"💾 Model saved to: {model_path}")

def generate_sample_recommendations():
    """
    Generate sample recommendations to demonstrate the model.
    """
    print("\n🎯 Sample Recommendations:")
    print("=" * 50)
    
    sample_conditions = [
        (35, 60, 5, "☀️ Hot Weather"),
        (25, 50, 8, "🌤️ Warm Weather"),
        (15, 90, 10, "🌧️ Rainy Weather"),
        (5, 70, 25, "❄️ Cold & Windy"),
        (-5, 80, 5, "❄️ Cold Weather"),
        (20, 40, 25, "🌬️ Windy Weather"),
        (12, 75, 8, "🌤️ Mild Weather")
    ]
    
    for temp, humidity, wind, condition in sample_conditions:
        print(f"\n{condition} ({temp}°C, {humidity}% humidity, {wind} km/h wind):")
        
        if temp > 30:
            print("   👕 Lightweight, breathable fabrics (cotton/linen)")
            print("   🎨 Light colors (white, beige, pastels)")
            print("   👟 Sandals, flip-flops, breathable sneakers")
            print("   ☀️ Sunscreen (SPF 30+), sunglasses, hat")
            print("   💧 Stay hydrated!")
        
        elif 20 <= temp <= 30:
            print("   👕 T-shirts, jeans, skirts, polos")
            print("   🧥 Light cardigans for indoor AC")
            print("   🎨 Bright or pastel colors")
            print("   👟 Sneakers, loafers, sandals")
            print("   ☀️ Light sunscreen if staying out long")
        
        elif humidity > 85 and 10 <= temp <= 25:
            print("   🧥 Waterproof jackets, raincoats")
            print("   👖 Quick-dry pants or jeans")
            print("   🎨 Darker colors (hides mud/splashes)")
            print("   👢 Waterproof shoes, rubber boots")
            print("   ☔ Carry umbrella, anti-frizz products")
        
        elif temp < 10:
            print("   🧥 Layered clothing: thermals, sweaters, winter coats")
            print("   🧣 Scarves, gloves, beanies")
            print("   🎨 Dark shades (navy, black, maroon)")
            print("   👢 Insulated boots, leather shoes")
            print("   💄 Moisturizer, lip balm, warm beverages")
        
        elif wind > 20 and 10 <= temp <= 25:
            print("   🧥 Windbreaker jackets")
            print("   💇 Hair tied up (avoid wind tangle)")
            print("   👟 Closed shoes or secure footwear")
            print("   👓 Protective eyewear if dusty")
            print("   ⚠️ Avoid light scarves or loose hats")

def main():
    """Main function to train and save the model."""
    print("🤖 Clothing Recommendation Model Training")
    print("=" * 50)
    
    # Generate training data
    print("📊 Generating training data...")
    features, labels = generate_weather_data(n_samples=2000)
    
    print(f"📈 Generated {len(features)} training samples")
    print(f"🎯 Unique recommendations: {len(set(labels))}")
    
    # Train the model
    print("\n🧠 Training the model...")
    model = train_model(features, labels)
    
    # Save the model
    print("\n💾 Saving the model...")
    save_model(model)
    
    # Generate sample recommendations
    generate_sample_recommendations()
    
    print("\n🎉 Training completed successfully!")
    print("\n📋 Model Features:")
    print("   • Temperature (°C)")
    print("   • Humidity (%)")
    print("   • Wind Speed (km/h)")
    
    print("\n🌐 To use the model:")
    print("   • API: python app.py")
    print("   • Web Interface: http://localhost:5001")
    print("   • Test: python test_api.py")

if __name__ == "__main__":
    main() 