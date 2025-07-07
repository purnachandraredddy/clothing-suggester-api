# Troubleshooting Guide

## Web Interface Issues

### Problem: Can't access the web interface

**Symptoms:**
- Browser shows "This site can't be reached" or "Connection refused"
- Page doesn't load when visiting http://localhost:5002

**Solutions:**

1. **Check if services are running:**
   ```bash
   # Check if API is running
   curl http://localhost:5001/health
   
   # Check if web interface is running
   curl http://localhost:5002/
   ```

2. **Start the services in the correct order:**
   ```bash
   # Terminal 1: Start API first
   python app.py
   
   # Terminal 2: Start web interface
   python web_interface.py
   ```

3. **Try different URLs:**
   - http://127.0.0.1:5002 (instead of localhost)
   - http://0.0.0.0:5002
   - http://[your-ip]:5002

4. **Check port conflicts:**
   ```bash
   # Check what's using port 5002
   lsof -i :5002
   
   # Check what's using port 5001
   lsof -i :5001
   ```

### Problem: Web interface loads but shows "API Not Connected"

**Symptoms:**
- Web page loads but shows red "❌ API Not Connected" message
- Can't get clothing recommendations

**Solutions:**

1. **Make sure API is running:**
   ```bash
   # Start the API
   python app.py
   ```

2. **Check API health:**
   ```bash
   curl http://localhost:5001/health
   ```

3. **Test API directly:**
   ```bash
   curl -X POST http://localhost:5001/predict \
     -H "Content-Type: application/json" \
     -d '{"temperature": 15, "humidity": 50, "wind_speed": 5}'
   ```

### Problem: Web interface shows errors in browser console

**Symptoms:**
- Page loads but JavaScript errors appear in browser console
- Buttons don't work or forms don't submit

**Solutions:**

1. **Clear browser cache:**
   - Press Ctrl+Shift+R (or Cmd+Shift+R on Mac)
   - Or open in incognito/private mode

2. **Check browser console:**
   - Press F12 to open developer tools
   - Look for errors in the Console tab

3. **Try different browser:**
   - Chrome, Firefox, Safari, Edge

### Problem: "Connection refused" errors

**Symptoms:**
- Error messages about connection being refused
- Services won't start

**Solutions:**

1. **Check if ports are already in use:**
   ```bash
   # Kill processes using the ports
   sudo lsof -ti:5001 | xargs kill -9
   sudo lsof -ti:5002 | xargs kill -9
   ```

2. **Use different ports:**
   ```bash
   # Edit app.py to use port 5003
   # Edit web_interface.py to use port 5004
   ```

### Problem: Model loading errors

**Symptoms:**
- API starts but shows model loading errors
- Predictions fail

**Solutions:**

1. **Train the model first:**
   ```bash
   python train_model.py
   ```

2. **Check model file exists:**
   ```bash
   ls -la data/
   ```

3. **Recreate the model:**
   ```bash
   rm -f data/clothing_model.joblib
   python train_model.py
   ```

## Quick Test Script

Run the test script to check everything:

```bash
python test_web_interface.py
```

This will test:
- API health endpoint
- API prediction endpoint
- Web interface homepage
- Web interface API connection
- Web interface prediction endpoint

## Common Commands

```bash
# Start API
python app.py

# Start web interface
python web_interface.py

# Train model
python train_model.py

# Test everything
python test_web_interface.py

# Check running processes
ps aux | grep python

# Check ports
netstat -tulpn | grep :500
```

## Expected Behavior

When everything is working correctly:

1. **API (port 5001):**
   - Shows "🚀 Starting Clothing Recommendation API"
   - Shows "✅ Model loaded successfully!"
   - Responds to health checks
   - Returns predictions

2. **Web Interface (port 5002):**
   - Shows "🌐 Starting Web Interface..."
   - Shows "✅ API Connected - Ready to use!" on the page
   - Form accepts weather data
   - Returns clothing recommendations

3. **Browser:**
   - Page loads without errors
   - Form works and submits data
   - Shows recommendations with confidence scores 