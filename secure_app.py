import os
import re
import sqlite3
import time
from flask import Flask, request, render_template, session, redirect
from werkzeug.security import check_password_hash

app = Flask(__name__)

# For production, set APP_SECRET in the environment.
app.secret_key = os.environ.get("APP_SECRET", "local-development-only-change-me")
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False,  # Set True when served over HTTPS.
    PERMANENT_SESSION_LIFETIME=1800,
)

# Simple in-memory throttling for a local demo.
# A production service should use a shared store/rate-limit mechanism.
failed_attempts = {}
MAX_ATTEMPTS = 5
WINDOW_SECONDS = 300

def get_db():
    return sqlite3.connect("users.db")

def valid_username(value: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9_.-]{3,32}", value))

def is_rate_limited(username: str) -> bool:
    now = time.time()
    attempts = [t for t in failed_attempts.get(username, []) if now - t < WINDOW_SECONDS]
    failed_attempts[username] = attempts
    return len(attempts) >= MAX_ATTEMPTS

def record_failure(username: str):
    failed_attempts.setdefault(username, []).append(time.time())

@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; style-src 'self'; form-action 'self'; frame-ancestors 'none'"
    )
    return response

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not valid_username(username) or not (8 <= len(password) <= 128):
            message = "Invalid username or password."
            return render_template("login.html", message=message), 400

        if is_rate_limited(username):
            message = "Too many unsuccessful attempts. Please try again later."
            return render_template("login.html", message=message), 429

        # FIX: parameterized query prevents SQL injection.
        conn = get_db()
        row = conn.execute(
            "SELECT id, username, password FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        conn.close()

        # FIX: password is verified against a salted password hash.
        if row and check_password_hash(row[2], password):
            session.clear()
            session["user_id"] = row[0]
            session["username"] = row[1]
            session.permanent = True
            return redirect("/dashboard")

        # FIX: generic authentication response.
        record_failure(username)
        message = "Invalid username or password."

    return render_template("login.html", message=message)

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    return render_template("dashboard.html", username=session.get("username"))

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=False)
