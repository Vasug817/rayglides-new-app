from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/auth/send-otp', methods=['POST'])
@app.route('/auth/send-otp', methods=['POST'])
def send_otp():
    try:
        import sqlite3
        conn = sqlite3.connect(":memory:")
        conn.close()
        return jsonify({"success": True, "message": "sqlite3 imported and run successfully!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
