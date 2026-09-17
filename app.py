import os
import subprocess
import signal
from threading import Thread, Lock
from queue import Queue
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Response
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = "super_secret_key_change_me"

DETECTION_PROC = None
PROC_LOCK = Lock()


DATABASE = "users.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        phone TEXT,
        address TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# --- Simple pub/sub for SSE ---
subscribers = set()
subs_lock = Lock()

def publish(msg: str):
    with subs_lock:
        dead = []
        for q in list(subscribers):
            try:
                q.put_nowait(msg)
            except Exception:
                dead.append(q)
        for q in dead:
            subscribers.discard(q)



def event_stream():
    q = Queue()
    with subs_lock:
        subscribers.add(q)
    try:
        while True:
            msg = q.get()
            yield f"data: {msg}\n\n"
    except GeneratorExit:
        with subs_lock:
            subscribers.discard(q)

def monitor_output(proc: subprocess.Popen):
    for raw in iter(proc.stdout.readline, ''):
        line = raw.strip()
        if not line:
            continue
        publish(line)
        low = line.lower()
        if "no eyes" in low:
            publish("ALERT_NO_EYES")
        if "eyes!!!" in low or low == "eyes":
            publish("INFO_EYES")
    publish("PROC_EXIT")

def is_running():
    global DETECTION_PROC
    return DETECTION_PROC is not None and DETECTION_PROC.poll() is None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        address = request.form["address"]
        password = generate_password_hash(request.form["password"])

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        try:
            cursor.execute("""
            INSERT INTO users(name,email,password,phone,address)
            VALUES(?,?,?,?,?)
            """, (name, email, password, phone, address))

            conn.commit()

            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            return render_template(
                "register.html",
                error="Email already exists."
            )

        finally:
            conn.close()

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id,name,password FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):

            session["user"] = user[1]
            session["user_id"] = user[0]

            return redirect(url_for("dashboard"))

        else:
            error = "Invalid Email or Password"

    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

@app.route("/dashboard")
def dashboard():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template("dashboard.html")

@app.get("/events")
def sse_events():
    if not session.get("user"):
        return Response("Unauthorized", status=401)
    return Response(event_stream(), mimetype="text/event-stream")

@app.post("/start_detection")
def start_detection():
    if not session.get("user"):
        return jsonify(ok=False, msg="Unauthorized"), 401

    global DETECTION_PROC
    with PROC_LOCK:
        if is_running():
            return jsonify(ok=True, msg="Already running")

        missing = []
        for f in ["SleepDetection.py", "haarcascade_frontalface_default.xml", "haarcascade_eye_tree_eyeglasses.xml"]:
            if not os.path.exists(f):
                missing.append(f)
        if missing:
            return jsonify(ok=False, msg=f"Missing files: {', '.join(missing)}")

        DETECTION_PROC = subprocess.Popen(
            ["python", "-u", "SleepDetection.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        Thread(target=monitor_output, args=(DETECTION_PROC,), daemon=True).start()
    publish("PROC_STARTED")
    return jsonify(ok=True)

@app.post("/stop_detection")
def stop_detection():
    if not session.get("user"):
        return jsonify(ok=False, msg="Unauthorized"), 401

    global DETECTION_PROC
    with PROC_LOCK:
        if not is_running():
            return jsonify(ok=True, msg="Not running")

        try:
            if os.name == "nt":
                try:
                    DETECTION_PROC.send_signal(signal.CTRL_BREAK_EVENT)
                except Exception:
                    DETECTION_PROC.terminate()
            else:
                DETECTION_PROC.terminate()
        finally:
            DETECTION_PROC = None
    publish("PROC_STOPPED")
    return jsonify(ok=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)