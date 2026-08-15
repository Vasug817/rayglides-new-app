from flask import Flask, jsonify
import sqlite3
import hashlib
import hmac
import time
import os
import random
import threading
import json
import base64
import traceback

app = Flask(__name__)

@app.route('/api/auth/send-otp', methods=['POST'])
@app.route('/auth/send-otp', methods=['POST'])
def send_otp():
    return jsonify({"success": True, "message": "All imports loaded successfully!"})
