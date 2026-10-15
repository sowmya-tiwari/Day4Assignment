
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = "task_manager_demo_secret_key"

DATABASE = "tasks.db"


# Connect to the database
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Create the tasks table
def create_table():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending'
        )
    """)

    conn.commit()
    conn.close()


# Login page
@app.route("/", methods=["GET", "POST"])
def home():
    if session.get("logged_in"):
        return redirect(url_for("tasks"))

    message = ""

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == "admin" and password == "1234":
            session["logged_in"] = True
            return redirect(url_for("tasks"))

        message = "Invalid username or password."

    return render_template("login.html", message=message)


# Display tasks (login required)
@app.route("/tasks", methods=["GET"])
def tasks():
    if not session.get("logged_in"):
        return redirect(url_for("home"))

    conn = get_db_connection()
    all_tasks = conn.execute(
        "SELECT id, title, status FROM tasks ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return render_template("tasks.html", tasks=all_tasks)


# Add a task using AJAX
@app.route("/add_task", methods=["POST"])
def add_task():
    if not session.get("logged_in"):
        return jsonify({
            "success": False,
            "message": "Please log in first."
        }), 401

    data = request.get_json(silent=True) or {}
    title = data.get("title", "").strip()

    if not title:
        return jsonify({
            "success": False,
            "message": "Task title cannot be empty."
        }), 400

    conn = get_db_connection()

    cursor = conn.execute(
        "INSERT INTO tasks (title) VALUES (?)",
        (title,)
    )

    task_id = cursor.lastrowid
    conn.commit()

    new_task = conn.execute(
        "SELECT id, title, status FROM tasks WHERE id = ?",
        (task_id,)
    ).fetchone()

    conn.close()

    return jsonify({
        "success": True,
        "task": {
            "id": new_task["id"],
            "title": new_task["title"],
            "status": new_task["status"]
        }
    }), 201


# Logout
@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    create_table()
    app.run(debug=True)
