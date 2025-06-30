# User Service Docker Setup

This is a FastAPI user service that can be containerized using Docker.

## Prerequisites

- Docker
- PostgreSQL (running separately)

## Building and Running

### 1. Build the Docker image
```bash
docker build -t user-service .
```

### 2. Run PostgreSQL container
```bash
docker run --name postgres-db -e POSTGRES_DB=user_service -e POSTGRES_USER=kibria -e POSTGRES_PASSWORD=kibria123 -p 5432:5432 -d postgres:15-alpine
```

### 3. Run the user service container
```bash
docker run --name user-service-app -p 8000:8000 -e DATABASE_URL="postgresql+asyncpg://kibria:kibria123@host.docker.internal:5432/user_service" user-service
```

## Access the Application

- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Docker Commands

### Build image
```bash
docker build -t user-service .
```

### Run container
```bash
docker run -p 8000:8000 user-service
```

### Stop containers
```bash
docker stop user-service-app
docker stop postgres-db
```

### Remove containers
```bash
docker rm user-service-app
docker rm postgres-db
```

### View logs
```bash
docker logs user-service-app
```
