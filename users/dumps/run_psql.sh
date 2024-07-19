PGPASSWORD="$POSTGRES_PASSWORD" psql -U "$POSTGRES_USER" -h "$PGHOST" -p "$PGPORT" -d "$POSTGRES_DB" -f dumps/users.sql > /dev/null 2>&1

# Проверяем код завершения последней команды
if [ $? -eq 0 ]; then
  exit 0
else
  exit 1
fi
