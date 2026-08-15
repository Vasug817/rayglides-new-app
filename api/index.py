from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/auth/send-otp', methods=['POST'])
@app.route('/auth/send-otp', methods=['POST'])
def send_otp():
    return jsonify({"success": True, "message": "Simplest Flask app works!"})
