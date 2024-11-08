from flask import Flask, jsonify, request
import psycopg2
from psycopg2 import sql, extras

app = Flask(__name__)

# PostgreSQL database connection
def get_db_connection():
    connection = psycopg2.connect(
        host="localhost",
        database="yourDatabaseName",
        user="yourUsername",
        password="yourPassword"
    )
    return connection

# Route to get all users
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=extras.DictCursor)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify([dict(user) for user in users])

# Route to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    new_user = request.json
    name = new_user.get('name')
    email = new_user.get('email')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING *",
        (name, email)
    )
    created_user = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "User created", "user": dict(created_user)}), 201

# Start the Flask server
if __name__ == '__main__':
    app.run(port=5000)
