# 👕 Intelligent Clothing Recommendation System

> **AI-powered clothing suggestions based on weather conditions**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.0+-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Project Overview

We are building an **intelligent clothing suggestion API** that predicts suitable clothing (e.g., *T-shirt*, *Light jacket*, *Coat*) based on environmental conditions: **temperature, humidity, and wind speed**.

Our aim is to create:
✅ A machine learning model that provides **realistic, user-satisfying predictions**  
✅ A **Flask REST API** that serves predictions in real time  
✅ A solution ready for **deployment and scaling**

## 🚀 What We Are Achieving

👉 Enable applications (e.g. weather apps, smart wardrobe, IoT devices) to suggest clothing to users automatically, enhancing convenience and personalization.

👉 Build a model that generalizes well across various weather conditions by:
- Sourcing or generating **representative data**
- Applying **machine learning best practices** (clean splits, avoiding overfitting)
- Saving and serving a **ready-to-use model** via API

👉 Lay the foundation for future enhancements (e.g. integration with real weather feeds, user feedback loops).

## 🛠 How We Are Tackling the Project

### 1️⃣ **Sourcing the Data**

Since no public dataset directly maps weather conditions to clothing, we **simulate realistic weather scenarios** by generating synthetic data using statistical distributions:
- Temperature: -5°C to 35°C
- Humidity: 20-100%
- Wind Speed: 0-20 km/h

We apply **rule-based logic** to assign clothing labels:
- **T-shirt** for warm temperatures
- **Light jacket** for mild temperatures  
- **Coat** for cold temperatures

This ensures our dataset reflects plausible combinations for training.

### 2️⃣ **Model Training**

We use `DecisionTreeClassifier` — a good choice for interpretable, fast models that handle mixed feature scales well.

**Steps:**
- **Train-test split** (80-20) to evaluate generalization performance
- **Limit tree depth** (e.g. `max_depth=5`) to avoid overfitting
- **Performance check**: classification report on test data (precision, recall, F1)

We can easily extend this with hyperparameter tuning or more advanced models (e.g. Random Forest).

### 3️⃣ **Model Persistence (Joblib Use)**

After training, we use **`joblib`** to serialize the model:

```python
joblib.dump(model, 'model.joblib')
```

**Why `joblib`?**
- Optimized for storing large numpy arrays efficiently (better than pickle for scikit-learn models)
- Quick loading at runtime → our Flask app can instantly load the model:

```python
model = joblib.load('model.joblib')
```

This allows us to **decouple training from serving**:
- Train once → save model → deploy API → update model later without changing the API.

### 4️⃣ **Serving Predictions**

We build a **Flask API** with a `/predict` POST endpoint.

**Steps:**
- Accept JSON payload (temperature, humidity, wind_speed)
- Convert to DataFrame → model predicts label → return as JSON

**Example request:**
```json
{
  "temperature": 15,
  "humidity": 50,
  "wind_speed": 5
}
```

**Example response:**
```json
{
  "suggestion": "Light jacket"
}
```

## ✅ End-to-End Pipeline

```
1️⃣ Data generation or collection → 
2️⃣ Model training → 
3️⃣ Evaluation + tuning → 
4️⃣ Save model using joblib → 
5️⃣ Flask app loads model → 
6️⃣ Real-time prediction API → 
7️⃣ Future: deploy in cloud, CI/CD, monitoring
```

## ⚡ Why This Approach Ensures User-Satisfying Predictions

✔ Data represents realistic weather scenarios  
✔ Decision tree interpretable + tunable  
✔ Controlled overfitting (max depth)  
✔ API is lightweight, fast, and ready for integration  
✔ Model easily updatable as we gather real user data  

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd flask_app_docker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Train the model**
   ```bash
   python train_model.py
   ```

4. **Run the Flask API**
   ```bash
   python app.py
   ```

5. **Test the API**
   ```bash
   curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"temperature": 15, "humidity": 50, "wind_speed": 5}'
   ```

## 📁 Project Structure

```
flask_app_docker/
├── README.md
├── requirements.txt
├── train_model.py          # Model training script
├── app.py                  # Flask API application
├── model.joblib           # Trained model (generated)
├── data/                  # Data directory
│   └── synthetic_data.csv # Generated training data
├── tests/                 # Test files
│   └── test_api.py
└── docker/                # Docker configuration
    ├── Dockerfile
    └── docker-compose.yml
```

## 🔧 API Documentation

### POST /predict

Predicts clothing suggestion based on weather conditions.

**Request Body:**
```json
{
  "temperature": float,  // Temperature in Celsius (-5 to 35)
  "humidity": float,     // Humidity percentage (20 to 100)
  "wind_speed": float    // Wind speed in km/h (0 to 20)
}
```

**Response:**
```json
{
  "suggestion": "string",  // Clothing suggestion
  "confidence": float      // Model confidence score
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"temperature": 15, "humidity": 50, "wind_speed": 5}'
```

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/
```

## 🐳 Docker Deployment

### Build and run with Docker

```bash
# Build the image
docker build -t clothing-recommender .

# Run the container
docker run -p 5000:5000 clothing-recommender
```

### Using Docker Compose

```bash
docker-compose up --build
```

## 🔮 Future Enhancements

- [ ] Integrate with live weather APIs to collect real user data
- [ ] Collect user feedback to fine-tune the model
- [ ] Deploy using Docker, AWS/GCP
- [ ] Add more clothing categories and weather conditions
- [ ] Implement user preferences and personalization
- [ ] Add model versioning and A/B testing capabilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Scikit-learn for the machine learning framework
- Flask for the web framework
- The open-source community for inspiration and tools

---

**Built with ❤️ for intelligent clothing recommendations** 