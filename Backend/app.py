from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

DB = "database.db"


def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS violations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        score INTEGER,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/violation", methods=["POST"])
def add_violation():

    data = request.json

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO violations(type,score,timestamp) VALUES(?,?,?)",
        (
            data["type"],
            data["score"],
            data["timestamp"]
        )
    )

    conn.commit()
    conn.close()

    return jsonify({"status":"success"})


@app.route("/api/dashboard")
def dashboard():

    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM violations")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM violations WHERE type='HELMET'")
    helmet = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM violations WHERE type='ALCOHOL'")
    alcohol = cur.fetchone()[0]

    score = max(0,100-(helmet*10)-(alcohol*25))

    cur.execute("""
        SELECT type,timestamp
        FROM violations
        ORDER BY id DESC
        LIMIT 10
    """)

    rows = cur.fetchall()

    history=[]

    for row in rows:

        history.append({

            "type":row["type"],

            "timestamp":row["timestamp"]

        })

    conn.close()

    return jsonify({

        "score":score,

        "helmet":helmet,

        "alcohol":alcohol,

        "total":total,

        "history":history

    })


if __name__=="__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )