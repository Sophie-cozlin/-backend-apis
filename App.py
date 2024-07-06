from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Database connection details
db_config = {
    'database': 'testconnection',
    'user': 'postgres',
    'password': 'cozlin',
    'host': 'localhost',
    'port': '5432'
}

@app.route('/')
def index():
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    title = data['title']
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute("INSERT INTO Tasks(title) VALUES (%s)", (title,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Task created successfully', 'title': title}), 201

@app.route('/delete/<task_id>', methods=['DELETE'])
def delete(task_id):
    if not task_id:
        return jsonify({'error': 'Task ID is required'}), 400

    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE task_id = %s", (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'message': 'Task deleted successfully'}), 200



if __name__ == '__main__':
    app.run(debug=True)
