# PowerShell: stop and remove services
param()

Write-Host "Stopping services..."
docker compose down

Write-Host "Services stopped"
