import os
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_HOST = os.environ.get("DB_HOST", "postgresql")
DB_NAME = os.environ.get("DB_NAME", "preptrackdb")
DB_USER = os.environ.get("DB_USER", "prepuser")
DB_PASS = os.environ.get("DB_PASS", "SuperSecret123")

def get_db_connection():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)

# --- NEW: Kubernetes Health Probe Endpoint ---
@app.route('/health', methods=['GET'])
def health_check():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "database": "disconnected", "error": str(e)}), 500

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, topic, description, status FROM study_tasks ORDER BY id DESC;')
        tasks = cur.fetchall()
        cur.close()
        conn.close()
        
        task_list = [{"id": t[0], "topic": t[1], "description": t[2], "status": t[3]} for t in tasks]
        return jsonify(task_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- NEW: Create Task ---
@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO study_tasks (topic, description, status) VALUES (%s, %s, %s) RETURNING id;',
            (data['topic'], data['description'], data.get('status', 'Pending'))
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Task created", "id": new_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- NEW: Delete Task ---
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM study_tasks WHERE id = %s;', (task_id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Task deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
