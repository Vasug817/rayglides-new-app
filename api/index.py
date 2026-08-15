from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

@app.route('/api/auth/send-otp', methods=['POST'])
@app.route('/auth/send-otp', methods=['POST'])
def send_otp():
    try:
        db_path = '/tmp/rayglides_test.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, val TEXT)")
        cursor.execute("INSERT INTO test (val) VALUES ('hello')")
        conn.commit()
        cursor.execute("SELECT val FROM test")
        val = cursor.fetchone()[0]
        conn.close()
        return jsonify({"success": True, "message": f"SQLite write successful! Read value: {val}"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
