$ErrorActionPreference = 'Stop'
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
docker compose up --build -d
Write-Host 'Yatranook is starting. Open http://localhost:8080 after containers become healthy.'
docker compose ps
