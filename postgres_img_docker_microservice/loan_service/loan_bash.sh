#!/bin/bash

# Step 1: Stop and remove existing containers
echo "Stopping and removing existing containers..."
docker rm -f loan-app-comp 2>/dev/null || echo "App container not found."
docker rm -f loan-db 2>/dev/null || echo "DB container not found."

# Step 2: Remove existing image
echo "Removing existing app image..."
docker rmi loan-compose 2>/dev/null || echo "Image not found."

# Step 3: Build a new app image
echo "Building new Docker image 'loan-compose'..."
docker build -t loan-compose .

# Step 4: Start the PostgreSQL container
echo "Starting PostgreSQL container 'loan-db'..."
docker run -d \
  --name loan-db \
  --network library-network \
  -e POSTGRES_USER=kibria \
  -e POSTGRES_PASSWORD=kibria \
  -e POSTGRES_DB=loans \
  -p 5454:5432 \
  postgres:15

# Step 5: Wait a few seconds to ensure DB is ready
echo "Waiting for database to initialize..."
sleep 5

# Step 6: Run the app container
echo "Running new container 'loan-app-comp'..."
docker run -d \
  --name loan-app-comp \
  --network library-network \
  -p 8083:8003 \
  loan-compose

echo "Done. Both DB and app are running."
