import urllib.request
import json
import time
import ssl

API_BASE = "https://rayglides-new-app.vercel.app/api"
TEST_CONTACT = "driver_test_99@rayglides.com"

ssl_context = ssl._create_unverified_context()

def make_request(path, data=None, headers=None):
    url = f"{API_BASE}{path}"
    req_headers = {"Content-Type": "application/json"}
    if headers:
        req_headers.update(headers)
    
    req_data = json.dumps(data).encode('utf-8') if data is not None else None
    req = urllib.request.Request(url, data=req_data, headers=req_headers, method='POST' if data is not None else 'GET')
    
    try:
        with urllib.request.urlopen(req, timeout=8, context=ssl_context) as res:
            return res.status, json.loads(res.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))
    except Exception as e:
        return 500, {"error": str(e)}

def run_tests():
    print("====================================================")
    print("   RAYGLIDES PRODUCTION END-TO-END FLOW VERIFICATION")
    print("====================================================\n")
    
    # 1. Test OTP Generation
    print("[TEST 1/6] Generating OTP for auth...")
    status, payload = make_request("/auth/send-otp", {"contact_info": TEST_CONTACT, "test": True})
    assert status == 200, f"OTP Generation failed with status {status}: {payload}"
    otp_code = payload.get("code")
    print(f"  -> SUCCESS! Received OTP Code: {otp_code}\n")
    
    # 2. Test OTP Verification & Sign-in
    print("[TEST 2/6] Verifying OTP and starting session...")
    status, payload = make_request("/auth/signin-otp", {"contact_info": TEST_CONTACT, "code": otp_code})
    assert status == 200, f"OTP Verification failed with status {status}: {payload}"
    auth_token = payload.get("token")
    user_id = payload.get("user", {}).get("id")
    print(f"  -> SUCCESS! Auth token received: {auth_token[:25]}... (User ID: {user_id})\n")
    
    auth_headers = {"Authorization": f"Bearer {auth_token}"}
    
    # 3. Test EV Cargo Loader Vehicle Selection
    print("[TEST 3/6] Configuring EV Cargo Loader Type (Tata Ace EV)...")
    status, payload = make_request("/driver/select-vehicle", {"model_type": "4_wheeler"}, headers=auth_headers)
    assert status == 200, f"Vehicle selection failed with status {status}: {payload}"
    print("  -> SUCCESS! Vehicle updated to 4_wheeler cargo loader.\n")
    
    # 4. Test Customer Ride Creation
    print("[TEST 4/6] Creating a delivery order request...")
    status, payload = make_request("/rides/create", {
        "rider_name": "Delhi Logistics Hub",
        "pickup_location": "Okhla Phase 1",
        "dropoff_location": "Gurgaon Sector 45",
        "fare": 520.0
    })
    assert status == 200, f"Ride creation failed with status {status}: {payload}"
    ride_id = payload.get("ride_id")
    print(f"  -> SUCCESS! Created Ride ID: {ride_id}\n")
    
    # 5. Test Driver Accepting & Completing Ride Flow
    print("[TEST 5/6] Simulating Driver Ride Flow (Accept -> Start -> Complete)...")
    
    # Accept
    status, payload = make_request("/rides/accept", {"ride_id": ride_id}, headers=auth_headers)
    assert status == 200, f"Ride accept failed with status {status}: {payload}"
    print(f"  -> Accepted Ride ID {ride_id}")
    
    # Start
    status, payload = make_request("/rides/update-status", {"ride_id": ride_id, "status": "started"}, headers=auth_headers)
    assert status == 200, f"Ride start failed: {payload}"
    print(f"  -> Started Ride ID {ride_id}")
    
    # Complete
    status, payload = make_request("/rides/update-status", {"ride_id": ride_id, "status": "completed"}, headers=auth_headers)
    assert status == 200, f"Ride complete failed: {payload}"
    print(f"  -> Completed Ride ID {ride_id}\n")
    
    # 6. Test Admin Panel Dashboards
    print("[TEST 6/6] Verifying Fleet Admin dashboard reports (Requires admin auth)...")
    
    # Login as seeded admin
    status, payload = make_request("/auth/signin-password", {"email": "admin@rayglides.com", "password": "admin123"})
    assert status == 200, f"Admin login failed: {payload}"
    admin_token = payload.get("token")
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Query users
    status, users = make_request("/admin/users", headers=admin_headers)
    assert status == 200, f"Query admin users failed: {users}"
    print(f"  -> SUCCESS! Fleet users queried successfully (Count: {len(users)})")
    
    # Query rides
    status, rides = make_request("/admin/rides", headers=admin_headers)
    assert status == 200, f"Query admin rides failed: {rides}"
    print(f"  -> SUCCESS! Fleet rides queried successfully (Count: {len(rides)})")
    
    print("\n====================================================")
    print("   ALL TESTS PASSED! PRODUCTION URL IS FULLY READY!  ")
    print("====================================================")

if __name__ == '__main__':
    run_tests()
