import os
import sqlite3

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

# ---------------- APP INIT ----------------
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

# ---------------- DATABASE ----------------
def get_db():
    # Add timeout to prevent "database is locked" error
    conn = sqlite3.connect("interview.db", timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS interviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            role TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            final_score INTEGER
        )""")
        conn.commit()

init_db()

# ---------------- QUESTIONS ----------------
role_questions = {
    "software": [
        "Explain a coding project you worked on.",
        "How do you debug complex errors?",
        "What programming languages are you strongest in?"
    ],
    "data": [
        "How do you clean messy datasets?",
        "Explain a time you used SQL.",
        "What visualization tools do you prefer?"
    ],
    "marketing": [
        "How would you launch a new product?",
        "Describe a successful campaign you worked on.",
        "How do you measure marketing success?"
    ]
}

# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return render_template("home.html")

# ---------------- AUTH ----------------
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        try:
            with get_db() as conn:
                conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
        except:
            return "Username already exists!"
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        with get_db() as conn:
            user = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("role_select"))
        else:
            return "Invalid credentials!"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---------------- INTERVIEW ----------------
@app.route("/role")
def role_select():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("role.html")

@app.route("/start", methods=["POST"])
def start():
    role = request.form["role"]
    session["role"] = role
    session["questions"] = role_questions[role]
    session["score"] = 0
    session["index"] = 0

    progress = 1
    total = len(session["questions"])
    progress_percent = (progress / total) * 100

    return render_template(
        "index.html",
        question=session["questions"][0],
        score=0,
        progress=progress,
        total=total,
        progress_percent=progress_percent
    )

@app.route("/submit", methods=["POST"])
def submit():
    answer = request.form["answer"]
    index = session.get("index", 0)
    question = session["questions"][index]
    score = session.get("score", 0)

    # Scoring logic
    if "teamwork" in answer.lower():
        feedback = "✅ Great! You mentioned teamwork — employers love that."
        score += 2
    elif "skills" in answer.lower():
        feedback = "💡 Good point! Highlighting your skills makes your answer stronger."
        score += 2
    elif "learning" in answer.lower():
        feedback = "📘 Showing willingness to learn is excellent."
        score += 2
    else:
        feedback = "📝 Nice start! Try adding teamwork, skills, or learning to make it stronger."
        score += 1

    session["score"] = score
    return render_template(
        "result.html",
        question=question,
        answer=answer,
        feedback=feedback,
        score=score,
        index=index,
        total=len(session["questions"])
    )

@app.route("/next")
def next_question():
    index = session.get("index", 0) + 1
    session["index"] = index

    if index < len(session["questions"]):
        progress = index + 1
        total = len(session["questions"])
        progress_percent = (progress / total) * 100

        return render_template(
            "index.html",
            question=session["questions"][index],
            score=session["score"],
            progress=progress,
            total=total,
            progress_percent=progress_percent
        )
    else:
        # Save interview results safely
        with get_db() as conn:
            conn.execute(
                "INSERT INTO interviews (user_id, role, final_score) VALUES (?, ?, ?)",
                (session["user_id"], session["role"], session["score"])
            )
            conn.commit()
        return render_template(
            "final.html",
            score=session["score"],
            total=len(session["questions"]),
            role=session["role"]
        )

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    with get_db() as conn:
        interviews = conn.execute("SELECT * FROM interviews WHERE user_id=?", (session["user_id"],)).fetchall()
    return render_template("dashboard.html", interviews=interviews)

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
