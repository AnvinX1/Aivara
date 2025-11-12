
#!/bin/bash

# Navigate to the project directory
cd /content/aivara_app/aivara-backend

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt

# Start Uvicorn server in the background
echo "Starting Uvicorn server..."

# Check if Uvicorn is already running on port 8000 and kill it if it is
PID=$(lsof -t -i:8000)
if [ -n "$PID" ]; then
  echo "Killing existing process on port 8000 (PID: $PID)"
  kill -9 $PID
  sleep 2 # Give it a moment to release the port
fi

# Remove any existing aivara.db to ensure a clean start for demonstration
# In a real app, you would handle migrations/persistence differently
if [ -f "aivara.db" ]; then
    echo "Removing existing aivara.db..."
    rm aivara.db
fi

# Start Uvicorn
(uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level info &> uvicorn.log &)
# Capture the PID of the background process
BG_PID=$!

echo "Uvicorn server started in the background. PID: $BG_PID"
echo "Access the API at: http://0.0.0.0:8000"
echo "Check logs at: /content/aivara_app/aivara-backend/uvicorn.log"

# Add a short delay to allow Uvicorn to start up before the script exits
sleep 5

