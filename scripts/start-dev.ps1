# PowerShell: build and start services detached
param()

Write-Host "Building images..."
docker compose build

Write-Host "Starting services (detached)..."
docker compose up -d

Write-Host "Services started. API: http://localhost:8000  Web: http://localhost:8501"
