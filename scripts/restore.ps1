param([Parameter(Mandatory=$true)][string]$BackupFile)
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $BackupFile -PathType Leaf)) { throw "Backup file not found: $BackupFile" }
$confirm = Read-Host 'WARNING: this overwrites objects in the configured Yatranook database. Type RESTORE to continue'
if ($confirm -cne 'RESTORE') { Write-Host 'Restore cancelled.'; exit 1 }
$container = 'yatranook-db'
$containerFile = '/tmp/yatranook-restore.dump'
docker cp (Resolve-Path -LiteralPath $BackupFile).Path "${container}:$containerFile"
docker exec $container sh -c "pg_restore --clean --if-exists --no-owner -U \`$POSTGRES_USER -d \`$POSTGRES_DB $containerFile"
docker exec $container rm -f $containerFile
Write-Host 'Restore command completed. Verify records and run application smoke tests.'
