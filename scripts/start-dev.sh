#!/usr/bin/env bash
# Start services (detached) using docker compose
set -euo pipefail

echo "Building images..."
docker compose build

echo "Starting services in background..."
docker compose up -d

echo "Services started. API: http://localhost:8000  Web: http://localhost:8501"
