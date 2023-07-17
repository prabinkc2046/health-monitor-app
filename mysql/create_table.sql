CREATE TABLE usage_data (
  timestamp TIMESTAMP PRIMARY KEY,
  cpu_usage_percent DECIMAL(5, 2),
  memory_usage_percent DECIMAL(5, 2),
  disk_usage_percent DECIMAL(5, 2)
);
