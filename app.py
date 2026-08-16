from flask import Flask, request, render_template, session, redirect
from werkzeug.security import check_password_hash
import sqlite3

app = Flask(__name__)

# INTENTIONALLY VULNERABLE — LOCAL LAB ONLY.
app.secret_key = "hardcoded-demo-secret"


def get_db():
    return sqlite3.connect("users.db")


@app.route("/", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        query = (
            "SELECT id, username, password "
            "FROM users "
            "WHERE username = ?"
        )

        conn = get_db()
        row = conn.execute(query, (username,)).fetchone()
        conn.close()

        if row and check_password_hash(row[2], password):
            session["user_id"] = row[0]
            session["username"] = row[1]
            return redirect("/dashboard")

        message = "Invalid username or password."

    return render_template("login.html", message=message)


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    return render_template(
        "dashboard.html",
        username=session.get("username")
    )


if __name__ == "__main__":
    app.run(debug=True)