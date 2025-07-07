#!/usr/bin/env python3
"""
Web Interface for Clothing Recommendation API

This creates a simple web interface where users can input weather conditions
and get clothing recommendations through a browser.
"""

from flask import Flask, render_template_string, request, jsonify
import requests
import json

app = Flask(__name__)

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>👕 Clothing Recommendation System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .form-section {
            padding: 40px;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
            font-size: 1.1em;
        }
        
        .form-group input {
            width: 100%;
            padding: 15px;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            font-size: 1.1em;
            transition: border-color 0.3s ease;
        }
        
        .form-group input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .submit-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1.2em;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s ease;
        }
        
        .submit-btn:hover {
            transform: translateY(-2px);
        }
        
        .result-section {
            padding: 40px;
            background: #f8f9fa;
            border-top: 1px solid #e1e5e9;
        }
        
        .result-card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        .weather-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }
        
        .weather-item {
            text-align: center;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        
        .weather-item .value {
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
        }
        
        .weather-item .label {
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }
        
        .recommendation {
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
            border-radius: 10px;
            margin-bottom: 15px;
        }
        
        .recommendation h3 {
            font-size: 1.8em;
            margin-bottom: 10px;
        }
        
        .confidence {
            text-align: center;
            color: #666;
            font-size: 1.1em;
        }
        
        .error {
            background: #ff6b6b;
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            color: #666;
        }
        
        .examples {
            margin-top: 30px;
            padding: 20px;
            background: #e3f2fd;
            border-radius: 10px;
        }
        
        .examples h4 {
            color: #1976d2;
            margin-bottom: 15px;
        }
        
        .example-btn {
            display: inline-block;
            margin: 5px;
            padding: 8px 15px;
            background: #1976d2;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9em;
        }
        
        .example-btn:hover {
            background: #1565c0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>👕 Clothing Recommendation</h1>
            <p>Get intelligent clothing suggestions based on weather conditions</p>
        </div>
        
        <div class="form-section">
            <form id="weatherForm">
                <div class="form-group">
                    <label for="temperature">🌡️ Temperature (°C)</label>
                    <input type="number" id="temperature" name="temperature" step="0.1" required 
                           placeholder="e.g., 15" min="-50" max="50">
                </div>
                
                <div class="form-group">
                    <label for="humidity">💧 Humidity (%)</label>
                    <input type="number" id="humidity" name="humidity" step="0.1" required 
                           placeholder="e.g., 50" min="0" max="100">
                </div>
                
                <div class="form-group">
                    <label for="wind_speed">💨 Wind Speed (km/h)</label>
                    <input type="number" id="wind_speed" name="wind_speed" step="0.1" required 
                           placeholder="e.g., 5" min="0" max="50">
                </div>
                
                <button type="submit" class="submit-btn">🔮 Get Recommendation</button>
            </form>
            
            <div class="examples">
                <h4>💡 Quick Examples:</h4>
                <button class="example-btn" onclick="fillExample('hot')">Hot Weather (25°C)</button>
                <button class="example-btn" onclick="fillExample('mild')">Mild Weather (15°C)</button>
                <button class="example-btn" onclick="fillExample('cold')">Cold Weather (5°C)</button>
                <button class="example-btn" onclick="fillExample('very-hot')">Very Hot (30°C)</button>
                <button class="example-btn" onclick="fillExample('very-cold')">Very Cold (-2°C)</button>
            </div>
        </div>
        
        <div class="result-section" id="resultSection" style="display: none;">
            <div class="result-card">
                <div id="loading" class="loading">
                    <p>🔮 Getting your recommendation...</p>
                </div>
                
                <div id="error" class="error" style="display: none;">
                    <p id="errorMessage"></p>
                </div>
                
                <div id="result" style="display: none;">
                    <div class="weather-info" id="weatherInfo"></div>
                    <div class="recommendation" id="recommendation"></div>
                    <div class="confidence" id="confidence"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function fillExample(type) {
            const examples = {
                'hot': { temperature: 25, humidity: 60, wind_speed: 3 },
                'mild': { temperature: 15, humidity: 50, wind_speed: 5 },
                'cold': { temperature: 5, humidity: 80, wind_speed: 10 },
                'very-hot': { temperature: 30, humidity: 40, wind_speed: 2 },
                'very-cold': { temperature: -2, humidity: 90, wind_speed: 15 }
            };
            
            const example = examples[type];
            document.getElementById('temperature').value = example.temperature;
            document.getElementById('humidity').value = example.humidity;
            document.getElementById('wind_speed').value = example.wind_speed;
        }
        
        document.getElementById('weatherForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const temperature = parseFloat(document.getElementById('temperature').value);
            const humidity = parseFloat(document.getElementById('humidity').value);
            const wind_speed = parseFloat(document.getElementById('wind_speed').value);
            
            // Show result section and loading
            document.getElementById('resultSection').style.display = 'block';
            document.getElementById('loading').style.display = 'block';
            document.getElementById('error').style.display = 'none';
            document.getElementById('result').style.display = 'none';
            
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        temperature: temperature,
                        humidity: humidity,
                        wind_speed: wind_speed
                    })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    // Hide loading, show result
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('result').style.display = 'block';
                    
                    // Update weather info
                    document.getElementById('weatherInfo').innerHTML = `
                        <div class="weather-item">
                            <div class="value">${data.weather_conditions.temperature}°C</div>
                            <div class="label">Temperature</div>
                        </div>
                        <div class="weather-item">
                            <div class="value">${data.weather_conditions.humidity}%</div>
                            <div class="label">Humidity</div>
                        </div>
                        <div class="weather-item">
                            <div class="value">${data.weather_conditions.wind_speed} km/h</div>
                            <div class="label">Wind Speed</div>
                        </div>
                    `;
                    
                    // Update recommendation
                    document.getElementById('recommendation').innerHTML = `
                        <h3>👕 ${data.suggestion}</h3>
                        <p>Recommended clothing for your weather conditions</p>
                    `;
                    
                    // Update confidence
                    document.getElementById('confidence').innerHTML = `
                        <p>🎯 Confidence: ${(data.confidence * 100).toFixed(1)}%</p>
                        <p>⏰ ${new Date(data.timestamp).toLocaleString()}</p>
                    `;
                    
                } else {
                    throw new Error(data.error || 'Failed to get recommendation');
                }
                
            } catch (error) {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('error').style.display = 'block';
                document.getElementById('errorMessage').textContent = error.message;
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main web interface."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    """Proxy the prediction request to the API."""
    try:
        data = request.get_json()
        
        # Forward the request to the API
        api_response = requests.post(
            'http://localhost:5001/predict',
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        return jsonify(api_response.json()), api_response.status_code
        
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'API server is not running. Please start the API first.'}), 503
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🌐 Starting Web Interface...")
    print("📡 Web interface will be available at http://localhost:5002")
    print("🔧 Make sure the API is running on http://localhost:5001")
    print()
    app.run(host='0.0.0.0', port=5002, debug=False) 