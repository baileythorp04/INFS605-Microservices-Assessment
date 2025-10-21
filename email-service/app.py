"""
student-profile microservice (Flask + psycopg2)

Purpose
-------
This file implements a small HTTP API that exposes CRUD operations for a
"students" resource and an endpoint for recording attendance.

How it fits into a microservice architecture
--------------------------------------------
- This application is a *backend microservice* that owns student data.
- It runs in its own Docker container and talks to a Postgres database
  running in a different container (service name: student-db).
- A separate frontend microservice (React) communicates with this API over HTTP.
- Containers are composed with docker-compose so services can reach each other
  by service name (e.g. student-db).

Important notes for students
----------------------------
- DATABASE_URL is read from the environment so the same code runs locally and
  in Docker. Example value used in docker-compose:
    postgresql://studentuser:studentpass@student-db:5432/studentsdb

- This is a teaching example: it uses direct psycopg2 connections (no pooling).
  For production you would use a connection pool or an ORM like SQLAlchemy.

- The Postgres database must be seeded (init.sql) with a `students` table that
  has at least columns: id (serial primary key), name (text), email (text),
  attendance (JSONB or text storing JSON array).
"""

from string import Template
from flask import Flask, jsonify, request
from flask_cors import CORS            # allows the React frontend to call this API
import psycopg2                        # PostgreSQL client library
import os
import json
import time
import datetime

app = Flask(__name__)
CORS(app)  # permit Cross-Origin requests from the frontend during development

OUT_DIR = os.getenv("EMAIL_OUT_DIR", "/out")

# -----------------------------
# Simple health endpoint
# -----------------------------
@app.route("/")
def home():
    """
    Health check and human-readable message.
    Frontend or a human tester can hit this endpoint to confirm the service is running.
    """
    return (
        "Hello from email-service! Theres no database this time."
        "This is a line of text to let you know that the API service is running."
    )


@app.route("/email/feedback", methods=["POST"])
def send_feedback_email():
    
    data = request.get_json() or {}

    if "sender" not in data or "feedback" not in data:
        return jsonify({"error": "sender and feedback are required"}), 400
    
    recipient = "schooladmin@email.com"
    sender = data['sender']
    feedback = data['feedback']


    template = Template(
        'To: $recipient\n' \
        'You have recieved feedback on your website from $sender\n' \
        '\n' \
        '$feedback\n' \
        '\n' \
        'To reply to this feedback or to view other feedback, go to http://localhost:3000/'
    )

    email = template.substitute({'recipient': recipient, 'sender': sender, 'feedback': feedback})
        



    return "Email sent", 200



@app.route("/email/reply", methods=["POST"])
def send_reply_email():
    data = request.get_json() or {}

    if "recipient" not in data or "reply" not in data or "feedback" not in data:
        return jsonify({"error": "recipient, reply and feedback are required"}), 400
    
    recipient = data['recipient']
    sender = "schooladmin@email.com"
    feedback = data['feedback']
    reply = data['reply']


    template = Template(
        'To: $recipient\n' \
        'You have recieved a reply to your feedback from $sender\n' \
        '\n' \
        '$reply\n' \
        '\n' \
        '\n' \
        'This was in response to your original feedback:\n' \
        '\n' \
        '$feedback'
    )

    email = template.substitute({'recipient': recipient, 'sender': sender, 'reply': reply, 'feedback': feedback})
        
    print("Reply email successfully created. Sending...")
    print(email)

    currenttime = datetime.datetime.now()
    
    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, f"reply-{currenttime}.txt")
    try:
        with open(out_path, "a", encoding="utf-8") as fh:
                fh.write(email)
    except:
         return jsonify({"error": "Failed to send email to file"}), 400

    return jsonify({"email":email, "message": "Email sent to file"}), 200



# -----------------------------
# Run the Flask dev server
# -----------------------------
if __name__ == "__main__":
    """
    For local development we run the Flask built-in server.
    In production (inside Docker), use a real WSGI server like gunicorn for stability:
      gunicorn -w 4 -b 0.0.0.0:5001 app:app
    """
    app.run(host="0.0.0.0", port=5004, debug=True)
