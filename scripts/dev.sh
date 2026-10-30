#!/usr/bin/env sh
set -eu
[ -f .env ] || cp .env.example .env
docker compose up --build -d
docker compose ps
printf '\nOpen http://localhost:8080 after containers become healthy.\n'
