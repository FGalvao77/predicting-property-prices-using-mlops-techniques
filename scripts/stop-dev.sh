#!/usr/bin/env bash
# Stop and remove services
set -euo pipefail

echo "Stopping services..."
docker compose down

echo "Services stopped"
