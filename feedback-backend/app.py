
from flask import Flask, jsonify, request
from flask_cors import CORS            
import psycopg2                        
import os
import json
import time
import requests

app = Flask(__name__)
CORS(app)  

DATABASE_URL = os.getenv(
    #the second link typed here is the default value.
    "DATABASE_URL",
    "postgresql://feedback:password@feedback-db:5432/feedback"
)
EMAIL_API = 'http://email-service:5004'



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
    print("basic test confirmed")
    return (
        "Hello. Feedback health check is good. "
        "This is a line of text to let you know that the API service is running smoothly"
    )

@app.route("/feedback", methods=["GET"])
def get_feedback():
    """
    Query the courses table and return a JSON list of course objects.

    Each feedback object:
      { "id": int, "student_name": str, "email: str, "text": str, "reply" : str, "feedback_state" : str }

    Notes:
    - We ORDER BY id to provide predictable results for students learning/testing.
    - attendance is stored in the DB as JSON (JSONB). We default to [] if null.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Execute a SELECT query to retrieve the relevant columns.
    cur.execute("SELECT id, student_name, email, text, reply, feedback_status FROM feedback ORDER BY id ASC")
    rows = cur.fetchall()

    # Close DB resources to avoid leaking connections.
    cur.close()
    conn.close()

    # Transform DB rows (tuples) into dictionaries for JSON serialization.
    feedback = [
        {"id": r[0], "student_name": r[1], "email": r[2], "text": r[3], "reply": r[4], "feedback_status": r[5]}
        for r in rows
    ]
    return jsonify(feedback), 200


@app.route("/feedback", methods=["POST"])
def create_feedback():

    data = request.get_json() or {}

    # Basic validation for required fields.
    if "name" not in data or "email" not in data or "text" not in data:
        return jsonify({"error": "name, email and text are required"}), 400

    conn = get_connection()
    cur = conn.cursor()

    # Use parameterized INSERT to safely add the row
    cur.execute(
        "INSERT INTO feedback (student_name, email, text) VALUES (%s, %s, %s) RETURNING id",
        (data["name"], data["email"], data["text"])
    )
    new_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()


    #### calling email-service ####
    sender = data["email"]
    feedback = data["text"]


    url = f"{EMAIL_API}/email/feedback"
    body = { "sender": sender, "feedback": feedback }
    requests.post(url, json=body, timeout=5)


    # Return the new resource with HTTP 201 "Created"
    return jsonify({
        "id": new_id,
        "name": data["name"],
        "email": data["email"],
        "text": data["text"]
    }), 201


@app.route("/feedback/<int:feedback_id>/reply", methods=["POST"])
def reply_feedback(feedback_id):

    data = request.get_json() or {}

    if "reply" not in data :
        return jsonify({"error": "reply is required"}), 400

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT reply, email, text FROM feedback WHERE id=%s", (feedback_id,))
    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return jsonify({"error": "Feedback not found"}), 404

    reply = data["reply"]


    cur.execute("UPDATE feedback SET reply=%s, feedback_status=%s WHERE id=%s", (reply, 'replied', feedback_id))
    conn.commit()

    cur.close()
    conn.close()



    #### calling email-service ####
    recipient = row[1]
    feedback = row[2]


    url = f"{EMAIL_API}/email/reply"
    body = { "reply": reply, "recipient": recipient, "feedback": feedback }
    requests.post(url, json=body, timeout=5)

    return jsonify({"id": feedback_id, "reply": reply}), 200


@app.route("/feedback/<int:feedback_id>", methods=["DELETE"])
def delete_feedback(feedback_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM feedback WHERE id=%s RETURNING id", (feedback_id,))
    deleted = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    if not deleted:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": "Deleted"}), 200

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
