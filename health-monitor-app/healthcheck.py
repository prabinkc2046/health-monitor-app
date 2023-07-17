import psutil
import time
import mysql.connector
import os
# MySQL database configuration
db_config = {
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'database': os.environ.get('DB_NAME')
}

def get_system_health():
    cpu_percent = psutil.cpu_percent()
    mem_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    return time.strftime('%Y-%m-%d %H:%M:%S'), cpu_percent, mem_usage, disk_usage

def insert_system_health(cursor, timestamp, cpu_usage, memory_usage, disk_usage):
    query = "INSERT INTO usage_data (timestamp, cpu_usage_percent, memory_usage_percent, disk_usage_percent) VALUES (%s, %s, %s, %s)"
    values = (timestamp, cpu_usage, memory_usage, disk_usage)
    cursor.execute(query, values)

def main():
    # Connect to the MySQL database
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        print("Connected to MySQL database")
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL database: {err}")
        return

    # Continuously retrieve system health information and insert into the database
    while True:
        timestamp, cpu_percent, mem_usage, disk_usage = get_system_health()
        insert_system_health(cursor, timestamp, cpu_percent, mem_usage, disk_usage)
        conn.commit()
        print(f"Inserted system health data at {timestamp}")
        time.sleep(1)

    # Close the database connection
    cursor.close()
    conn.close()
    print("MySQL connection closed")

if __name__ == "__main__":
    main()
