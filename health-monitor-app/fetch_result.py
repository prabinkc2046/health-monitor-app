from flask import Flask, render_template
import mysql.connector
from threading import Thread
from healthcheck import main as healthcheck_main
import matplotlib.pyplot as plt
import io
import base64
import os

# MySQL database configuration
db_config = {
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'database': os.environ.get('DB_NAME')
}

app = Flask(__name__)

def fetch_system_health(cursor):
    query = "SELECT * FROM usage_data ORDER BY timestamp ASC"
    cursor.execute(query)
    return cursor.fetchall()

def generate_bar_graph(system_health_entries):
    timestamps = []
    cpu_usage = []
    memory_usage = []
    disk_usage = []

    for entry in system_health_entries:
        timestamp, cpu, memory, disk = entry
        timestamps.append(timestamp)
        cpu_usage.append(cpu)
        memory_usage.append(memory)
        disk_usage.append(disk)

    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 8))
    
    axes[0].bar(timestamps, cpu_usage, color='red')
    axes[0].set_ylabel('CPU Usage (%)')
    axes[0].set_ylim(0, 100)
    axes[0].set_title('CPU Usage Over Time')

    axes[1].bar(timestamps, memory_usage, color='green')
    axes[1].set_ylabel('Memory Usage (%)')
    axes[1].set_ylim(0, 100)
    axes[1].set_title('Memory Usage Over Time')

    axes[2].bar(timestamps, disk_usage, color='blue')
    axes[2].set_xlabel('Timestamp')
    axes[2].set_ylabel('Disk Usage (%)')
    axes[2].set_ylim(0, 100)
    axes[2].set_title('Disk Usage Over Time')

    plt.tight_layout()

    # Convert the plot to an image
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    plot_image = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    return plot_image

@app.route('/monitor')
def monitor():
    # Connect to the MySQL database
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        print("Connected to MySQL database")
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL database: {err}")
        return "Error connecting to MySQL database"

    # Fetch all entries from the system_health table
    system_health_entries = fetch_system_health(cursor)

    # Generate the bar graphs
    plot_image = generate_bar_graph(system_health_entries)

    # Close the database connection
    cursor.close()
    conn.close()
    print("MySQL connection closed")

    return render_template('monitor.html', plot_image=plot_image)

if __name__ == "__main__":
    # Start the healthcheck.py script in a separate thread
    healthcheck_thread = Thread(target=healthcheck_main)
    healthcheck_thread.start()

    app.run(host="0.0.0.0")
