#!/usr/bin/env python3
"""
Test suite for the Clothing Recommendation API

This module contains comprehensive tests for the Flask API endpoints.
"""

import pytest
import json
import requests
import time
import os
import sys
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_model():
    """Mock the trained model for testing."""
    mock_model = MagicMock()
    
    # Mock prediction
    mock_model.predict.return_value = ['Light jacket']
    
    # Mock prediction probabilities
    mock_model.predict_proba.return_value = [[0.1, 0.8, 0.1]]  # High confidence for Light jacket
    
    return mock_model

class TestHomeEndpoint:
    """Test the home endpoint."""
    
    def test_home_endpoint(self, client):
        """Test that the home endpoint returns API information."""
        response = client.get('/')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert 'message' in data
        assert 'endpoints' in data
        assert 'usage' in data
        assert data['message'] == '👕 Clothing Recommendation API'

class TestHealthEndpoint:
    """Test the health check endpoint."""
    
    def test_health_endpoint(self, client):
        """Test that the health endpoint returns status information."""
        response = client.get('/health')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert 'status' in data
        assert 'timestamp' in data
        assert 'model_status' in data
        assert data['status'] == 'healthy'

class TestPredictEndpoint:
    """Test the prediction endpoint."""
    
    def test_predict_valid_input(self, client, mock_model):
        """Test prediction with valid input data."""
        with patch('app.model', mock_model):
            test_data = {
                'temperature': 15.0,
                'humidity': 50.0,
                'wind_speed': 5.0
            }
            
            response = client.post('/predict',
                                 data=json.dumps(test_data),
                                 content_type='application/json')
            
            data = json.loads(response.data)
            
            assert response.status_code == 200
            assert 'suggestion' in data
            assert 'confidence' in data
            assert 'weather_conditions' in data
            assert data['suggestion'] == 'Light jacket'
            assert isinstance(data['confidence'], float)
    
    def test_predict_missing_field(self, client):
        """Test prediction with missing required field."""
        test_data = {
            'temperature': 15.0,
            'humidity': 50.0
            # Missing wind_speed
        }
        
        response = client.post('/predict',
                             data=json.dumps(test_data),
                             content_type='application/json')
        
        data = json.loads(response.data)
        
        assert response.status_code == 400
        assert 'error' in data
        assert 'Missing required field' in data['error']
    
    def test_predict_invalid_temperature(self, client):
        """Test prediction with invalid temperature range."""
        test_data = {
            'temperature': 100.0,  # Too high
            'humidity': 50.0,
            'wind_speed': 5.0
        }
        
        response = client.post('/predict',
                             data=json.dumps(test_data),
                             content_type='application/json')
        
        data = json.loads(response.data)
        
        assert response.status_code == 400
        assert 'error' in data
        assert 'Temperature must be between' in data['error']
    
    def test_predict_invalid_humidity(self, client):
        """Test prediction with invalid humidity range."""
        test_data = {
            'temperature': 15.0,
            'humidity': 150.0,  # Too high
            'wind_speed': 5.0
        }
        
        response = client.post('/predict',
                             data=json.dumps(test_data),
                             content_type='application/json')
        
        data = json.loads(response.data)
        
        assert response.status_code == 400
        assert 'error' in data
        assert 'Humidity must be between' in data['error']
    
    def test_predict_invalid_wind_speed(self, client):
        """Test prediction with invalid wind speed range."""
        test_data = {
            'temperature': 15.0,
            'humidity': 50.0,
            'wind_speed': 100.0  # Too high
        }
        
        response = client.post('/predict',
                             data=json.dumps(test_data),
                             content_type='application/json')
        
        data = json.loads(response.data)
        
        assert response.status_code == 400
        assert 'error' in data
        assert 'Wind speed must be between' in data['error']
    
    def test_predict_non_numeric_values(self, client):
        """Test prediction with non-numeric values."""
        test_data = {
            'temperature': 'hot',
            'humidity': 50.0,
            'wind_speed': 5.0
        }
        
        response = client.post('/predict',
                             data=json.dumps(test_data),
                             content_type='application/json')
        
        data = json.loads(response.data)
        
        assert response.status_code == 400
        assert 'error' in data
        assert 'All weather values must be numeric' in data['error']
    
    def test_predict_no_json_data(self, client):
        """Test prediction with no JSON data."""
        response = client.post('/predict')
        
        data = json.loads(response.data)
        
        assert response.status_code == 400
        assert 'error' in data
        assert 'No JSON data provided' in data['error']
    
    def test_predict_invalid_json(self, client):
        """Test prediction with invalid JSON."""
        response = client.post('/predict',
                             data='invalid json',
                             content_type='application/json')
        
        data = json.loads(response.data)
        
        assert response.status_code == 400
        assert 'error' in data
        assert 'Invalid JSON' in data['error']

class TestBatchPredictEndpoint:
    """Test the batch prediction endpoint."""
    
    def test_batch_predict_valid_input(self, client, mock_model):
        """Test batch prediction with valid input data."""
        with patch('app.model', mock_model):
            test_data = {
                'weather_conditions': [
                    {'temperature': 15.0, 'humidity': 50.0, 'wind_speed': 5.0},
                    {'temperature': 25.0, 'humidity': 60.0, 'wind_speed': 3.0}
                ]
            }
            
            response = client.post('/predict/batch',
                                 data=json.dumps(test_data),
                                 content_type='application/json')
            
            data = json.loads(response.data)
            
            assert response.status_code == 200
            assert 'predictions' in data
            assert 'count' in data
            assert len(data['predictions']) == 2
            assert data['count'] == 2
            
            for prediction in data['predictions']:
                assert 'suggestion' in prediction
                assert 'confidence' in prediction
                assert 'weather_conditions' in prediction
                assert prediction['suggestion'] == 'Light jacket'
    
    def test_batch_predict_empty_array(self, client):
        """Test batch prediction with empty weather conditions array."""
        test_data = {
            'weather_conditions': []
        }
        
        response = client.post('/predict/batch',
                             data=json.dumps(test_data),
                             content_type='application/json')
        
        data = json.loads(response.data)
        
        assert response.status_code == 400
        assert 'error' in data
        assert 'weather_conditions array cannot be empty' in data['error']
    
    def test_batch_predict_too_large(self, client):
        """Test batch prediction with too many conditions."""
        test_data = {
            'weather_conditions': [
                {'temperature': 15.0, 'humidity': 50.0, 'wind_speed': 5.0}
            ] * 101  # More than 100
        }
        
        response = client.post('/predict/batch',
                             data=json.dumps(test_data),
                             content_type='application/json')
        
        data = json.loads(response.data)
        
        assert response.status_code == 400
        assert 'error' in data
        assert 'Batch size cannot exceed 100' in data['error']
    
    def test_batch_predict_invalid_condition(self, client):
        """Test batch prediction with invalid condition in array."""
        test_data = {
            'weather_conditions': [
                {'temperature': 15.0, 'humidity': 50.0, 'wind_speed': 5.0},
                {'temperature': 100.0, 'humidity': 50.0, 'wind_speed': 5.0}  # Invalid
            ]
        }
        
        response = client.post('/predict/batch',
                             data=json.dumps(test_data),
                             content_type='application/json')
        
        data = json.loads(response.data)
        
        assert response.status_code == 400
        assert 'error' in data
        assert 'Invalid weather condition at index 1' in data['error']

class TestErrorHandlers:
    """Test error handling."""
    
    def test_404_error(self, client):
        """Test 404 error handling."""
        response = client.get('/nonexistent')
        data = json.loads(response.data)
        
        assert response.status_code == 404
        assert 'error' in data
        assert 'Endpoint not found' in data['error']

def test_validate_input_function():
    """Test the validate_input function directly."""
    from app import validate_input
    
    # Test valid input
    valid_data = {'temperature': 15.0, 'humidity': 50.0, 'wind_speed': 5.0}
    is_valid, error = validate_input(valid_data)
    assert is_valid
    assert error == ""
    
    # Test missing field
    invalid_data = {'temperature': 15.0, 'humidity': 50.0}
    is_valid, error = validate_input(invalid_data)
    assert not is_valid
    assert 'Missing required field' in error
    
    # Test invalid temperature
    invalid_temp = {'temperature': 100.0, 'humidity': 50.0, 'wind_speed': 5.0}
    is_valid, error = validate_input(invalid_temp)
    assert not is_valid
    assert 'Temperature must be between' in error

if __name__ == '__main__':
    pytest.main([__file__]) 