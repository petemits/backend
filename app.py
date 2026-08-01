from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# ---------------- DATABASE ---------------- #
def db():
    conn = sqlite3.connect("condoliving.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- INIT SYSTEM ---------------- #
@app.route("/init")
def init():
    conn = db()
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        email TEXT,
        password TEXT,
        role TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS contracts (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        role TEXT,
        type TEXT,
        content TEXT,
        status TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS work_orders (
        id INTEGER PRIMARY KEY,
        unit TEXT,
        issue_type TEXT,
        description TEXT,
        status TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS contractors (
        id INTEGER PRIMARY KEY,
        name TEXT,
        trade TEXT,
        rating REAL,
        approved INTEGER
    )""")

    conn.commit()
    conn.close()
    return "CONDOLIVING SAAS DATABASE READY"

# ---------------- USERS ---------------- #
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    conn = db()
    c = conn.cursor()

    c.execute("INSERT INTO users VALUES (NULL,?,?,?)",
              (data["email"], data["password"], data["role"]))

    conn.commit()
    conn.close()
    return {"msg": "user created"}

@app.route("/users")
def users():
    conn = db()
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    rows = c.fetchall()
    return jsonify([dict(r) for r in rows])

# ---------------- WORK ORDERS ---------------- #
@app.route("/workorder", methods=["POST"])
def create_work():
    d = request.json
    conn = db()
    c = conn.cursor()

    c.execute("INSERT INTO work_orders VALUES (NULL,?,?,?,?)",
              (d["unit"], d["issue_type"], d["description"], "open"))

    conn.commit()
    conn.close()
    return {"msg": "work order created"}

@app.route("/workorders")
def workorders():
    conn = db()
    c = conn.cursor()
    c.execute("SELECT * FROM work_orders")
    return jsonify([dict(r) for r in c.fetchall()])

# ---------------- CONTRACTORS ---------------- #
@app.route("/contractor", methods=["POST"])
def add_contractor():
    d = request.json
    conn = db()
    c = conn.cursor()

    c.execute("INSERT INTO contractors VALUES (NULL,?,?,?,1)",
              (d["name"], d["trade"], d["rating"]))

    conn.commit()
    conn.close()
    return {"msg": "contractor added"}

@app.route("/contractors")
def contractors():
    conn = db()
    c = conn.cursor()
    c.execute("SELECT * FROM contractors WHERE approved=1")
    return jsonify([dict(r) for r in c.fetchall()])

# ---------------- CONTRACTS ---------------- #
@app.route("/contract", methods=["POST"])
def contract():
    d = request.json
    conn = db()
    c = conn.cursor()

    c.execute("INSERT INTO contracts VALUES (NULL,?,?,?,?,?)",
              (d["user_id"], d["role"], d["type"], d["content"], "pending"))

    conn.commit()
    conn.close()
    return {"msg": "contract created"}

@app.route("/contracts")
def contracts():
    conn = db()
    c = conn.cursor()
    c.execute("SELECT * FROM contracts")
    return jsonify([dict(r) for r in c.fetchall()])

# ---------------- RUN ---------------- #
if __name__ == "__main__":
    app.run(debug=True)