from flask import Flask, jsonify
import sqlite3
import os
import random
import hashlib
import time

app = Flask(__name__)

DB_PATH = '/tmp/rayglides_test_full.db'

def hash_password(password):
    salt = b'rayglides_salt_static'
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return dk.hex()

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if cursor.fetchone():
            conn.close()
            return
    except Exception:
        pass

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          email TEXT UNIQUE NOT NULL,
          phone TEXT,
          role TEXT DEFAULT 'driver',
          auth_provider TEXT DEFAULT 'email',
          password_hash TEXT,
          emergency_name TEXT,
          emergency_phone TEXT,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          user_id INTEGER,
          device_id TEXT UNIQUE NOT NULL,
          model_type TEXT NOT NULL,
          license_plate TEXT,
          battery_capacity_ah REAL DEFAULT 20.0,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
          FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telemetry_history (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          device_id TEXT NOT NULL,
          timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
          soc INTEGER,
          soh INTEGER,
          battery_voltage REAL,
          battery_current REAL,
          battery_temp REAL,
          solar_voltage REAL,
          solar_power REAL,
          fan_duty REAL,
          solar_wh REAL,
          charge_wh REAL,
          cost_saved REAL,
          latitude REAL,
          longitude REAL,
          FOREIGN KEY (device_id) REFERENCES vehicles(device_id)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS otp_codes (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          contact_info TEXT NOT NULL,
          code TEXT NOT NULL,
          expires_at REAL NOT NULL,
          verified INTEGER DEFAULT 0
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          order_id TEXT,
          payment_id TEXT,
          status TEXT,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rides (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          rider_name TEXT NOT NULL,
          pickup_location TEXT NOT NULL,
          dropoff_location TEXT NOT NULL,
          fare REAL NOT NULL,
          status TEXT DEFAULT 'available',
          driver_id INTEGER,
          created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
          completed_at DATETIME,
          FOREIGN KEY (driver_id) REFERENCES users(id)
        )
    """)
    
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_telemetry_device ON telemetry_history(device_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_telemetry_time ON telemetry_history(timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_rides_status ON rides(status)")
    
    admin_email = 'admin@rayglides.com'
    admin_pwd = 'admin123'
    driver_email = 'vasu@rayglides.com'
    driver_pwd = 'driver123'
        
    admin_hash = hash_password(admin_pwd)
    cursor.execute("INSERT OR IGNORE INTO users (name, email, role, password_hash) VALUES (?, ?, ?, ?)",
                   ('RayGlides Admin', admin_email, 'admin', admin_hash))
                   
    driver_hash = hash_password(driver_pwd)
    cursor.execute("INSERT OR IGNORE INTO users (name, email, phone, role, password_hash, emergency_name, emergency_phone) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   ('Vasu Gupta', driver_email, '+919876543210', 'driver', driver_hash, 'Emergency Contact', '+911111111111'))
    
    cursor.execute("SELECT id FROM users WHERE email=?", (driver_email,))
    user_row = cursor.fetchone()
    if user_row:
        cursor.execute("""
            INSERT OR IGNORE INTO vehicles (user_id, device_id, model_type, license_plate)
            VALUES (?, 'RayGlides_EMS_9232C8', '3_wheeler', 'DL-3S-EV-1234')
        """, (user_row[0],))
        
    cursor.execute("SELECT count(*) FROM rides WHERE status='available'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO rides (rider_name, pickup_location, dropoff_location, fare) VALUES (?, ?, ?, ?)",
                       ('Delhi Cargo Depot', 'Okhla Phase 3', 'Connaught Place', 350.0))

    conn.commit()
    conn.close()

@app.route('/api/auth/send-otp', methods=['POST'])
@app.route('/auth/send-otp', methods=['POST'])
def send_otp():
    try:
        init_db()
        return jsonify({"success": True, "message": "Full DB init check successful!"})
    except Exception as e:
        import traceback
        return jsonify({"success": False, "error": str(e), "traceback": traceback.format_exc()})
