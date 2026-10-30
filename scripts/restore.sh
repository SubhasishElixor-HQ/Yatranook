#!/usr/bin/env sh
set -eu
if [ "${1:-}" = "" ] || [ ! -f "$1" ]; then
  echo "Usage: $0 path/to/backup.dump" >&2
  exit 2
fi
printf 'WARNING: this will replace objects in the configured Yatranook database. Continue? [y/N] '
read -r ANSWER
[ "$ANSWER" = "y" ] || [ "$ANSWER" = "Y" ] || exit 1
docker compose exec -T db sh -c 'pg_restore --clean --if-exists --no-owner -U "$POSTGRES_USER" -d "$POSTGRES_DB"' < "$1"
echo "Restore command completed. Verify application data and run smoke tests."
