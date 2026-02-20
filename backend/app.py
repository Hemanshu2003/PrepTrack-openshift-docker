import os
import psycopg2
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS so our frontend can securely request data
CORS(app)

# Fetch database credentials from OpenShift Secrets/ConfigMaps
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "preptrackdb")
DB_USER = os.environ.get("DB_USER", "prepuser")
DB_PASS = os.environ.get("DB_PASS", "SuperSecret123")

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, topic, description, status FROM study_tasks;')
        tasks = cur.fetchall()
        cur.close()
        conn.close()
        
        # Format the data into JSON
        task_list = []
        for task in tasks:
            task_list.append({
                "id": task[0],
                "topic": task[1],
                "description": task[2],
                "status": task[3]
            })
        return jsonify(task_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the server on port 5000 inside the container
    app.run(host='0.0.0.0', port=5000)