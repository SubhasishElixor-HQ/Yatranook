#!/usr/bin/env sh
set -eu
mkdir -p backups
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
FILE="backups/yatranook-${STAMP}.dump"
docker compose exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' > "$FILE"
echo "Backup written to $FILE"
echo "Verify with: docker compose exec -T db pg_restore --list < $FILE"
