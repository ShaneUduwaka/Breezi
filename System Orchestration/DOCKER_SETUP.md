# DOCKER_SETUP.md
# Docker Setup & Quick Start Guide

## Overview

Breezi System Orchestration is containerized with Docker and docker-compose for easy deployment and development.

## Quick Start

### 1. Development Environment (with Mock Services)

```bash
# Navigate to System Orchestration folder
cd "System Orchestration"

# Start all services with mock STT/TTS
docker-compose -f docker-compose.mock.yml up -d

# Check logs
docker-compose -f docker-compose.mock.yml logs -f app

# Stop services
docker-compose -f docker-compose.mock.yml down
```

### 2. Production Environment (Real Services)

```bash
# Copy .env.production and update with your credentials
cp .env.production .env

# Update .env with:
# - Twilio credentials
# - Google Cloud keys
# - Client database credentials
# - Other provider-specific keys

# Start production stack
docker-compose up -d

# Check logs
docker-compose logs -f app

# Stop services
docker-compose down
```

## Services

### Main Application (`breezi-orchestration`)
- **Port 8000**: FastAPI main endpoint
- **Port 8001**: WebSocket audio streaming

### Redis (`breezi-redis`)
- **Port 6379**: Session storage & cache
- Volume: `redis-data`

### Milvus Vector DB (`breezi-vectordb`)
- **Port 19530**: MetaStore/DataStore
- **Port 9091**: Metrics

### Mock Services (Development Only)
- **Mock STT** (Port 8002): Simulates speech-to-text
- **Mock TTS** (Port 8003): Simulates text-to-speech

## Configuration

### Environment Variables

**Development:**
```bash
# .env.development is pre-configured with mock services
# No changes needed for basic development
```

**Production:**
```bash
# Copy and update .env file
CALL_INGESTION_TYPE=twilio           # or custom_voip, webrtc
STT_PROVIDER=google                  # or aws, azure
TTS_PROVIDER=google                  # or aws, azure
CLIENT_DB_TYPE=rest                  # or sql
```

## Docker Compose Files

### `docker-compose.yml` (Production)
- Real services only
- Requires credentials in `.env`
- Full stack: app + redis + milvus

### `docker-compose.mock.yml` (Development)
- Mock STT/TTS services included
- Pre-configured for testing
- Quick iteration & debugging

## Building Custom Images

### Build app image
```bash
docker build -t breezi:latest .
```

### Build specific version
```bash
docker build -t breezi:v1.0 .
docker tag breezi:v1.0 your-registry/breezi:v1.0
docker push your-registry/breezi:v1.0
```

## Health Checks

All services include health checks:
```bash
# Check app health
curl http://localhost:8000/health

# Check Redis
redis-cli -h localhost ping

# Check Milvus
curl http://localhost:9091/healthz
```

## Logs & Debugging

### View all logs
```bash
docker-compose logs -f
```

### View specific service logs
```bash
docker-compose logs -f app
docker-compose logs -f redis
docker-compose logs -f milvus
```

### Debug container
```bash
docker exec -it breezi-orchestration bash
```

## Volumes

- `redis-data`: Persistent Redis data
- `milvus-data`: Persistent Milvus vector db
- `./logs`: Application logs (on host machine)

## Network

All services connected via `breezi-network` bridge network.

Access between containers:
- App → Redis: `redis://redis:6379`
- App → Milvus: `milvus:19530`
- App → Mock STT: `http://mock-stt:8002`
- App → Mock TTS: `http://mock-tts:8003`

## Performance Optimization

### Resource Limits (edit docker-compose.yml)
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

### Restart Policies
- `no`: Do not automatically restart
- `unless-stopped`: Always restart unless explicitly stopped
- `always`: Always restart
- `on-failure`: Restart only on failure

## Troubleshooting

### Port Already in Use
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 PID
```

### Container Won't Start
```bash
# Check logs
docker-compose logs app

# Rebuild image
docker-compose build --no-cache
```

### Network Issues
```bash
# Check network
docker network inspect breezi-network

# Restart services
docker-compose restart
```

## Production Deployment

### Using Docker Swarm
```bash
docker swarm init
docker stack deploy -c docker-compose.yml breezi
```

### Using Kubernetes
```bash
# Generate k8s manifests from compose
kompose convert -f docker-compose.yml

# Deploy
kubectl apply -f *.yaml
```

### Using Azure Container Instances
```bash
az container create \
  --resource-group myResourceGroup \
  --name breezi \
  --image your-registry/breezi:latest \
  --ports 8000 8001 \
  --registry-login-server your-registry \
  --registry-username username \
  --registry-password password
```

## Security

### Don't Commit Secrets
```bash
# .env files are in .gitignore
# Use secrets manager in production

# Docker secrets for Swarm
docker secret create db_password ./db_password.txt

# Kubernetes secrets
kubectl create secret generic db-creds --from-file=.env.production
```

### Image Scanning
```bash
# Scan for vulnerabilities
docker scan breezi:latest
```

---

**Ready to deploy?** Choose your environment and follow the quick start! 🚀
