#!/bin/bash

# Set the path to your Python executable
PYTHON_EXECUTABLE="python3"

# Set the name of your virtual environment
VENV_NAME="venv"

# Set the python instance in virtual environment
VENV_PATH=$VENV_NAME/bin/

# Set the path to your requirements.txt file
REQUIREMENTS_FILE="requirements.txt"

# Set the command to run your server
SERVER_COMMAND=$VENV_PATH"python3 server.py"  # Adjust this to your actual server command

# Unique identifier to filter the correct process
IDENTIFIER="server.py"

# Path to the lock file
LOCK_FILE="server.lock"

# Function to check if the server is running
is_server_running() {
    ps aux | grep "$SERVER_COMMAND" | grep "$IDENTIFIER" | grep -v grep
}

# Check if the lock file exists (indicating another instance is running)
if [ -e "$LOCK_FILE" ]; then
    echo "Another instance of the server is already running. Exiting."
    exit 1
fi

# Create virtual environment if not exists
if [ ! -d "$VENV_NAME" ]; then
    $PYTHON_EXECUTABLE -m venv $VENV_NAME
fi

# Activate the virtual environment
source $VENV_NAME/bin/activate

# Install requirements
$VENV_PATH/pip install -r $REQUIREMENTS_FILE

# Run server using nohup (detach from terminal)
nohup $SERVER_COMMAND > logs/server.log 2>&1 &

# Inform the user
echo "Virtual environment activated. Server is running in the background."

# Monitor and restart the server if it stops in the background
(while true; do
    if ! is_server_running; then
        echo "Server is not running. Restarting..."
        nohup $SERVER_COMMAND > logs/server.log 2>&1 &
        echo "Server restarted."
    fi
    sleep 10  # Adjust the sleep interval as needed
done) &  # Run the subshell in the background
