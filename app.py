#!/usr/bin/env python3
"""
Clothing Recommendation Flask API

This Flask application serves clothing recommendations based on weather conditions
using a pre-trained machine learning model.
"""

from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
import os
from datetime import datetime

app = Flask(__name__)

# Global variable to store the loaded model
model = None

def load_model(model_path='model.joblib'):
    """
    Load the trained model from disk.
    
    Args:
        model_path (str): Path to the saved model file
        
    Returns:
        The loaded model or None if loading fails
    """
    try:
        if os.path.exists(model_path):
            return joblib.load(model_path)
        else:
            print(f"❌ Model file not found at {model_path}")
            print("💡 Please run 'python train_model.py' first to train and save the model")
            return None
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None

def validate_input(data):
    """
    Validate the input data for prediction.
    
    Args:
        data (dict): Input data containing weather conditions
        
    Returns:
        tuple: (is_valid, error_message)
    """
    required_fields = ['temperature', 'humidity', 'wind_speed']
    
    # Check if all required fields are present
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    
    # Validate data types and ranges
    try:
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        wind_speed = float(data['wind_speed'])
        
        # Check reasonable ranges
        if not (-50 <= temperature <= 50):
            return False, "Temperature must be between -50 and 50°C"
        
        if not (0 <= humidity <= 100):
            return False, "Humidity must be between 0 and 100%"
        
        if not (0 <= wind_speed <= 50):
            return False, "Wind speed must be between 0 and 50 km/h"
            
    except (ValueError, TypeError):
        return False, "All weather values must be numeric"
    
    return True, ""

@app.route('/')
def home():
    """Serve the web interface HTML."""
    try:
        with open('static/index.html', 'r', encoding='utf-8') as f:
            return f.read(), 200, {'Content-Type': 'text/html'}
    except FileNotFoundError:
        # Fallback to API info if HTML file not found
        return jsonify({
            'message': '👕 Clothing Recommendation API',
            'version': '1.0.0',
            'endpoints': {
                'GET /': 'API information',
                'POST /predict': 'Get clothing recommendation',
                'GET /health': 'Health check'
            },
            'usage': {
                'method': 'POST',
                'endpoint': '/predict',
                'body': {
                    'temperature': 'float (Celsius)',
                    'humidity': 'float (percentage)',
                    'wind_speed': 'float (km/h)'
                }
            }
        })

@app.route('/health')
def health_check():
    """Health check endpoint."""
    model_status = "loaded" if model is not None else "not_loaded"
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'model_status': model_status,
        'model_loaded': model is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict clothing recommendation based on weather conditions.
    
    Expected JSON payload:
    {
        "temperature": 15.0,
        "humidity": 50.0,
        "wind_speed": 5.0
    }
    
    Returns:
    {
        "suggestion": "Light jacket",
        "confidence": 0.95,
        "weather_conditions": {...}
    }
    """
    # Check if model is loaded
    if model is None:
        return jsonify({
            'error': 'Model not loaded. Please ensure the model file exists.',
            'solution': 'Run "python train_model.py" to train and save the model'
        }), 500
    
    # Get JSON data from request
    try:
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'No JSON data provided'}), 400
    except Exception as e:
        return jsonify({'error': f'Invalid JSON: {str(e)}'}), 400
    
    # Validate input data
    is_valid, error_message = validate_input(data)
    if not is_valid:
        return jsonify({'error': error_message}), 400
    
    try:
        # Prepare features for prediction
        features = np.array([
            float(data['temperature']),
            float(data['humidity']),
            float(data['wind_speed'])
        ]).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(features)[0]
        
        # Get prediction probabilities for confidence
        probabilities = model.predict_proba(features)[0]
        confidence = float(max(probabilities))
        
        # Prepare response
        response = {
            'suggestion': prediction,
            'confidence': round(confidence, 3),
            'weather_conditions': {
                'temperature': float(data['temperature']),
                'humidity': float(data['humidity']),
                'wind_speed': float(data['wind_speed'])
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'error': f'Prediction failed: {str(e)}'
        }), 500

@app.route('/predict/batch', methods=['POST'])
def predict_batch():
    """
    Predict clothing recommendations for multiple weather conditions.
    
    Expected JSON payload:
    {
        "weather_conditions": [
            {"temperature": 15.0, "humidity": 50.0, "wind_speed": 5.0},
            {"temperature": 25.0, "humidity": 60.0, "wind_speed": 3.0}
        ]
    }
    """
    # Check if model is loaded
    if model is None:
        return jsonify({
            'error': 'Model not loaded. Please ensure the model file exists.'
        }), 500
    
    # Get JSON data from request
    try:
        data = request.get_json()
        if data is None or 'weather_conditions' not in data:
            return jsonify({'error': 'No weather_conditions array provided'}), 400
    except Exception as e:
        return jsonify({'error': f'Invalid JSON: {str(e)}'}), 400
    
    weather_conditions = data['weather_conditions']
    
    if not isinstance(weather_conditions, list):
        return jsonify({'error': 'weather_conditions must be an array'}), 400
    
    if len(weather_conditions) == 0:
        return jsonify({'error': 'weather_conditions array cannot be empty'}), 400
    
    if len(weather_conditions) > 100:  # Limit batch size
        return jsonify({'error': 'Batch size cannot exceed 100 predictions'}), 400
    
    results = []
    
    for i, condition in enumerate(weather_conditions):
        # Validate each condition
        is_valid, error_message = validate_input(condition)
        if not is_valid:
            return jsonify({
                'error': f'Invalid weather condition at index {i}: {error_message}'
            }), 400
        
        try:
            # Prepare features for prediction
            features = np.array([
                float(condition['temperature']),
                float(condition['humidity']),
                float(condition['wind_speed'])
            ]).reshape(1, -1)
            
            # Make prediction
            prediction = model.predict(features)[0]
            probabilities = model.predict_proba(features)[0]
            confidence = float(max(probabilities))
            
            results.append({
                'index': i,
                'suggestion': prediction,
                'confidence': round(confidence, 3),
                'weather_conditions': {
                    'temperature': float(condition['temperature']),
                    'humidity': float(condition['humidity']),
                    'wind_speed': float(condition['wind_speed'])
                }
            })
            
        except Exception as e:
            return jsonify({
                'error': f'Prediction failed for condition at index {i}: {str(e)}'
            }), 500
    
    return jsonify({
        'predictions': results,
        'count': len(results),
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500

def main():
    """Initialize and run the Flask application."""
    global model
    
    print("🚀 Starting Clothing Recommendation API")
    print("=" * 40)
    
    # Load the model
    print("📦 Loading trained model...")
    model = load_model()
    
    if model is None:
        print("❌ Failed to load model. Please run 'python train_model.py' first.")
        return
    
    print("✅ Model loaded successfully!")
    print("🌐 Starting Flask server...")
    print("📡 API will be available at http://localhost:5001")
    print("🔧 Use Ctrl+C to stop the server")
    print()
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5001, debug=False)

if __name__ == '__main__':
    main() 