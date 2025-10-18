
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
