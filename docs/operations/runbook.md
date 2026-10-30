# Operations Runbook

## Startup

```bash
cp .env.example .env
docker compose up --build -d
docker compose ps
docker compose logs -f api
```

## Health checks

- Web: `http://localhost:8080/healthz`
- API via web proxy: `http://localhost:8080/api/v1/health`
- Liveness: `http://localhost:8080/healthz` and API container `/healthz`

## Backup

```bash
./scripts/backup.sh
```

PowerShell users can run the equivalent Docker command:

```powershell
docker compose exec -T db pg_dump -U $env:POSTGRES_USER -d $env:POSTGRES_DB -Fc | Set-Content -Encoding Byte .\backups\yatranook.dump
```

For reliable Windows backups, use `cmd /c` redirection or a PowerShell byte-safe stream; validate the dump with `pg_restore --list`.

## Restore warning

Restoring overwrites data in the target database. Restore only into an isolated or deliberately selected database after verifying the backup. Use the provided shell script on Linux/macOS or a controlled PowerShell command on Windows.

## Logs

```bash
docker compose logs --tail=200 api
docker compose logs --tail=200 web
docker compose logs --tail=200 db
```

## Migration lifecycle

Single replica: the API entrypoint applies Alembic migrations before startup. Multi-replica production: run `alembic upgrade head` once as a release job, then deploy API replicas with migrations disabled in their entrypoint.

## Incident basics

1. Check container health and recent logs.
2. Check database connection and storage availability.
3. Check provider availability and rate-limit headers.
4. Disable an unhealthy external integration through configuration.
5. Avoid manually changing production records without a documented migration or recovery procedure.
6. Record the incident, impact, mitigation, and follow-up actions.
