from flask import Flask, request, jsonify, render_template
import sqlite3
import re

app = Flask(__name__)
DB_NAME = "lottery.db"

def get_db():
    return sqlite3.connect(DB_NAME)

# Create table if not exists
with get_db() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS numbers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT NOT NULL
        )
    """)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/frequency", methods=["POST"])
def frequency():
    num = request.json["number"]

    db = get_db()
    cursor = db.execute(
        "SELECT COUNT(*) FROM numbers WHERE number = ?",
        (num,)
    )
    count = cursor.fetchone()[0]
    db.close()

    return jsonify({
        "number": num,
        "frequency": count
    })

@app.route("/add", methods=["POST"])
def add_number():
    num = request.json["number"]

    if len(num) != 4 or not num.isdigit():
        return jsonify({"message": "Enter a valid 4-digit number"}), 400

    db = get_db()
    db.execute(
        "INSERT INTO numbers (number) VALUES (?)",
        (num,)
    )
    db.commit()
    db.close()

    return jsonify({"message": "Number added successfully"})

@app.route("/bulk_add", methods=["POST"])
def bulk_add_numbers():
    text = request.json["text"]
    numbers = re.findall(r"\b\d{4}\b", text)
    
    if not numbers:
        return jsonify({"message": "No 4-digit numbers found"}), 400
    
    db = get_db()
    for num in numbers:
        db.execute("INSERT INTO numbers (number) VALUES (?)", (num,))
    db.commit()
    db.close()
    
    return jsonify({"message": f"Added {len(numbers)} numbers successfully"})

if __name__ == "__main__":
    app.run(debug=True)
