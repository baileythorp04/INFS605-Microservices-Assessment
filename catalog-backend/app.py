
from flask import Flask, jsonify, request
from flask_cors import CORS            
import psycopg2                        
import os
import json
import time

app = Flask(__name__)
CORS(app)  

DATABASE_URL = os.getenv(
    #the second link typed here is the default value.
    "DATABASE_URL",
    "postgresql://catalog:password@catalog-db:5432/catalog"
)


max_retries = 20
for i in range(max_retries):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("Connected to DB!")
        conn.close()
        break
    except psycopg2.OperationalError:
        # If the connection failed, wait and try again.
        print(f"DB connection failed ({i+1}/{max_retries}), retrying in 2s...")
        time.sleep(2)
else:
    # If we've retried max_retries times, raise an error and stop the service.
    raise Exception(f"Could not connect to the database after {max_retries} retries")

def get_connection():
    """
    Create and return a new psycopg2 database connection.

    Note:
    - Each call returns a *new* connection. Handlers must close connections and cursors.
    - For production, use a connection pool (psycopg2.pool or SQLAlchemy engine).
    """
    return psycopg2.connect(DATABASE_URL)


@app.route("/")
def home():
    """
    Health check and human-readable message.
    Frontend or a human tester can hit this endpoint to confirm the service is running.
    """
    return (
        "Hello from **Brand new** catalog-db service (with Postgres DB)! "
        "This is a line of text to let you know that the API service is running smoothly and doesn't yet have CRUD capability"
    )

@app.route("/courses", methods=["GET"])
def get_courses():
    """
    Query the courses table and return a JSON list of course objects.

    Each course object:
      { "id": int, "name": str, "code": str, "year": int, "description": str }

    Notes:
    - We ORDER BY id to provide predictable results for students learning/testing.
    - attendance is stored in the DB as JSON (JSONB). We default to [] if null.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Execute a SELECT query to retrieve the relevant columns.
    cur.execute("SELECT id, name, code, year, description FROM courses ORDER BY id ASC")
    rows = cur.fetchall()

    # Close DB resources to avoid leaking connections.
    cur.close()
    conn.close()

    # Transform DB rows (tuples) into dictionaries for JSON serialization.
    courses = [
        {"id": r[0], "name": r[1], "code": r[2], "year": r[3], "description": r[4]}
        for r in rows
    ]
    return jsonify(courses), 200

@app.route("/courses", methods=["POST"])
def add_course():

    data = request.get_json() or {}

    # Basic validation for required fields.
    if "name" not in data or "code" not in data or "year" not in data or "description" not in data:
        return jsonify({"error": "name, code, year, and description are required"}), 400

    conn = get_connection()
    cur = conn.cursor()

    # Use parameterized INSERT to safely add the row; attendance starts as an empty JSON array.
    cur.execute(
        "INSERT INTO courses (name, code, year, description) VALUES (%s, %s, %s, %s) RETURNING id",
        (data["name"], data["code"], data["year"], data["description"])
    )
    new_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()

    # Return the new resource with HTTP 201 "Created"
    return jsonify({
        "id": new_id,
        "name": data["name"],
        "code": data["code"],
        "year": data["year"],
        "description": data["description"],
    }), 201


# -----------------------------
# Run the Flask dev server
# -----------------------------
if __name__ == "__main__":
    """
    For local development we run the Flask built-in server.
    In production (inside Docker), use a real WSGI server like gunicorn for stability:
      gunicorn -w 4 -b 0.0.0.0:5001 app:app
    """
    app.run(host="0.0.0.0", port=5002, debug=True)
