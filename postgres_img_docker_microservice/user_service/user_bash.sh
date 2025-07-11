#!/bin/bash

# Step 1: Stop and remove existing container
echo "Stopping and removing existing container..."
docker rm -f user-app-comp 2>/dev/null || echo "Container not found."
docker rm -f user-db 2>/dev/null || echo "DB container not found."

# Step 2: Remove existing image
echo "Removing existing image..."
docker rmi user-compose 2>/dev/null || echo "Image not found."


# Step 3: Start the PostgreSQL container
echo "Starting PostgreSQL container 'user-db'..."
docker run -d \
  --name user-db \
  --network library-network \
  -e POSTGRES_USER=kibria \
  -e POSTGRES_PASSWORD=kibria \
  -e POSTGRES_DB=users \
  -p 5451:5432 \
  postgres:15

# Step 4: Build a new image
echo "Building new Docker image 'user-compose'..."
docker build -t user-compose .

# Step 5: Run a new container from the image
echo "Running new container 'user-app-comp'..."
docker run -d -p 8081:8001 --network library-network --name user-app-comp user-compose

echo "Done."
