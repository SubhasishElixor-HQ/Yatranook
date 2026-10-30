$ErrorActionPreference = 'Stop'
$container = 'yatranook-db'
$backupDir = Join-Path (Get-Location) 'backups'
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$containerFile = "/tmp/yatranook-$stamp.dump"
$localFile = Join-Path $backupDir "yatranook-$stamp.dump"
docker exec $container sh -c "pg_dump -U \`$POSTGRES_USER -d \`$POSTGRES_DB -Fc -f $containerFile"
docker cp "${container}:$containerFile" $localFile
docker exec $container rm -f $containerFile
Write-Host "Backup created: $localFile"
Write-Host 'Verify with: docker exec yatranook-db pg_restore --list /tmp/<copied-backup>.dump'
