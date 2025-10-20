
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
    "postgresql://feedback:password@feedback-db:5432/feedback"
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
        "Hello. Feedback health check is good. "
        "This is a line of text to let you know that the API service is running smoothly"
    )

@app.route("/feedback", methods=["GET"])
def get_feedback():
    """
    Query the courses table and return a JSON list of course objects.

    Each feedback object:
      { "id": int, "student_name": str, "text": str }

    Notes:
    - We ORDER BY id to provide predictable results for students learning/testing.
    - attendance is stored in the DB as JSON (JSONB). We default to [] if null.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Execute a SELECT query to retrieve the relevant columns.
    cur.execute("SELECT id, student_name, text FROM feedback ORDER BY id ASC")
    rows = cur.fetchall()

    # Close DB resources to avoid leaking connections.
    cur.close()
    conn.close()

    # Transform DB rows (tuples) into dictionaries for JSON serialization.
    feedback = [
        {"id": r[0], "student_name": r[1], "text": r[2]}
        for r in rows
    ]
    return jsonify(feedback), 200



# -----------------------------
# Run the Flask dev server
# -----------------------------
if __name__ == "__main__":
    """
    For local development we run the Flask built-in server.
    In production (inside Docker), use a real WSGI server like gunicorn for stability:
      gunicorn -w 4 -b 0.0.0.0:5001 app:app
    """
    app.run(host="0.0.0.0", port=5003, debug=True)
