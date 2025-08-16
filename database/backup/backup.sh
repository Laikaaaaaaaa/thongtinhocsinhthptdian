# Backup script
#!/bin/bash
echo "Starting backup process..."
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="backup_$DATE.sql"

# Create database backup
pg_dump -h localhost -U postgres myapp > $BACKUP_FILE
echo "Backup completed: $BACKUP_FILE"

# Compress backup
gzip $BACKUP_FILE
echo "Backup compressed: $BACKUP_FILE.gz"
