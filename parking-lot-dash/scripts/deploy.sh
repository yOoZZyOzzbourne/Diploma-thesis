#!/bin/bash
# Deploy script for Parking Lot Dash application to remote server

REMOTE_USER="parkoviste"
REMOTE_HOST="158.196.15.41"
REMOTE_PATH="~/parking-lot-dash"

echo "==================================="
echo "Parking Lot Dash - Deploy"
echo "==================================="
echo ""
echo "Deploying to: ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}"
echo ""

# Check if we can connect
echo "Testing connection..."
ssh -q ${REMOTE_USER}@${REMOTE_HOST} exit
if [ $? -ne 0 ]; then
    echo "Error: Cannot connect to ${REMOTE_USER}@${REMOTE_HOST}"
    echo "Please check your SSH configuration and credentials"
    exit 1
fi
echo "✓ Connection successful"
echo ""

# Create remote directory if it doesn't exist
echo "Creating remote directory..."
ssh ${REMOTE_USER}@${REMOTE_HOST} "mkdir -p ${REMOTE_PATH}"
echo "✓ Remote directory ready"
echo ""

# Sync files (excluding venv, __pycache__, .git, etc.)
echo "Syncing files..."
rsync -avz --progress \
    --exclude 'venv/' \
    --exclude '__pycache__/' \
    --exclude '*.pyc' \
    --exclude '.git/' \
    --exclude '.DS_Store' \
    --exclude '*.db' \
    --exclude '.env' \
    ./ ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_PATH}/

if [ $? -ne 0 ]; then
    echo "Error: Failed to sync files"
    exit 1
fi
echo "✓ Files synced"
echo ""

# Run setup on remote server
echo "Running setup on remote server..."
ssh ${REMOTE_USER}@${REMOTE_HOST} "cd ${REMOTE_PATH} && chmod +x scripts/*.sh && ./scripts/setup.sh"
if [ $? -ne 0 ]; then
    echo "Error: Setup failed on remote server"
    exit 1
fi
echo "✓ Setup complete on remote server"
echo ""

echo "==================================="
echo "Deployment complete!"
echo "==================================="
echo ""
echo "To start the application on the remote server:"
echo "1. SSH to the server: ssh ${REMOTE_USER}@${REMOTE_HOST}"
echo "2. Navigate to: cd parking-lot-dash"
echo "3. Edit .env file: nano .env"
echo "4. Start app: ./scripts/start.sh"
echo ""
echo "Or run remotely:"
echo "ssh ${REMOTE_USER}@${REMOTE_HOST} 'cd parking-lot-dash && ./scripts/start.sh'"
echo ""
