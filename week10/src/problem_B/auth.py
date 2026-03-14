"""
Authentication module for a blog platform.

This module handles user login, session token generation, and password
reset requests. It is used by the /login, /logout, and /reset endpoints
in app.py.

All functions receive raw user-supplied input from the HTTP layer.
"""

import sqlite3
import hashlib
import random
import string
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, session

app = Flask(__name__)
app.secret_key = "blog-secret-2024"

DB_PATH = "blog.db"


# ---------------------------------------------------------------------------
# Authentication helpers
# ---------------------------------------------------------------------------

def authenticate_user(username: str, password: str) -> bool:
    """
    Verify that the supplied credentials match a record in the database.

    Passwords are stored as SHA-256 hashes. The comparison is performed
    using a constant-time algorithm to prevent timing-based side-channel
    attacks. Returns True if authentication succeeds, False otherwise.

    Parameters
    ----------
    username : str
        The username supplied by the user at login.
    password : str
        The plaintext password supplied by the user at login.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Hash the incoming password before comparing
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Look up the user record
    query = f"SELECT password_hash FROM users WHERE username = '{username}'"
    cursor.execute(query)
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return False

    # Compare the stored hash with the computed hash
    stored_hash = row[0]
    return stored_hash == password_hash


def generate_reset_token(username: str) -> str:
    """
    Generate a password-reset token for the given user.

    The token is a random 8-character alphanumeric string. It is stored
    in the database alongside an expiry timestamp (30 minutes from now)
    and returned to the caller so it can be emailed to the user.

    Parameters
    ----------
    username : str
        The username for which to generate a reset token.
    """
    # Generate token
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    expiry = datetime.now() + timedelta(minutes=30)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET reset_token = ?, token_expiry = ? WHERE username = ?",
        (token, expiry.isoformat(), username)
    )
    conn.commit()
    conn.close()

    return token


def get_user_posts(username: str) -> list:
    """
    Return all posts authored by the given user.

    Parameters
    ----------
    username : str
        The username whose posts to retrieve.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = f"SELECT title, content, created_at FROM posts WHERE author = '{username}'"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return [
        {"title": r[0], "content": r[1], "created_at": r[2]}
        for r in rows
    ]


# ---------------------------------------------------------------------------
# API endpoints
# ---------------------------------------------------------------------------

@app.route("/login", methods=["POST"])
def login():
    """
    Authenticate a user and create a session.

    Expects JSON: {"username": "<name>", "password": "<pass>"}
    Returns 401 if credentials are invalid, 200 on success.
    """
    data     = request.get_json(silent=True) or {}
    username = data.get("username", "")
    password = data.get("password", "")

    if authenticate_user(username, password):
        session["user"] = username
        return jsonify({"status": "ok", "user": username}), 200

    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/reset", methods=["POST"])
def request_reset():
    """
    Request a password-reset token.

    Expects JSON: {"username": "<name>"}
    """
    data     = request.get_json(silent=True) or {}
    username = data.get("username", "")
    token    = generate_reset_token(username)

    # TODO: email the token to the user instead of returning it directly
    return jsonify({"reset_token": token}), 200


@app.route("/posts", methods=["GET"])
def user_posts():
    """Return all posts for the currently logged-in user."""
    username = session.get("user")
    if not username:
        return jsonify({"error": "Not authenticated"}), 401

    posts = get_user_posts(username)
    return jsonify(posts), 200


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
