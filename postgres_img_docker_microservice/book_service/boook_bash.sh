#!/bin/bash

# Step 1: Stop and remove existing containers
echo "Stopping and removing existing containers..."
docker rm -f book-app-comp 2>/dev/null || echo "App container not found."
docker rm -f book-db 2>/dev/null || echo "DB container not found."

# Step 2: Remove existing image
echo "Removing existing app image..."
docker rmi book-compose 2>/dev/null || echo "Image not found."

# Step 3:   Start the PostgreSQL container 
echo "Starting PostgreSQL container 'book-db'..."
docker run -d \
  --name book-db \
  --network library-network \
  -e POSTGRES_USER=kibria \
  -e POSTGRES_PASSWORD=kibria \
  -e POSTGRES_DB=books \
  -p 5452:5432 \
  postgres:15



# Step 4: Build a new app image
echo "Building new Docker image 'book-compose'..."
docker build -t book-compose .


# Step 5: Wait a few seconds to ensure DB is ready
echo "Waiting for database to initialize..."
sleep 5

# Step 6: Run the app container
echo "Running new container 'book-app-comp'..."
docker run -d \
  --name book-app-comp \
  --network library-network \
  -p 8082:8002 \
  book-compose

echo "Done. Both DB and app are running."
