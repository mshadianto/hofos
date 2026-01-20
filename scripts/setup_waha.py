#!/usr/bin/env python3
"""
WAHA Setup & Test Script
Automatically configures webhook and tests the connection
"""
import os
import sys
import time
import httpx
from dotenv import load_dotenv

load_dotenv()

WAHA_URL = os.getenv("WAHA_URL", "").rstrip("/")
WAHA_API_KEY = os.getenv("WAHA_API_KEY", "")
WEBHOOK_URL = "https://hofos.up.railway.app/webhook"
SESSION_NAME = "hofos"

def log(msg):
    print(f"[SETUP] {msg}")

def api_call(method, endpoint, json_data=None):
    """Make API call to WAHA"""
    url = f"{WAHA_URL}{endpoint}"
    headers = {"X-Api-Key": WAHA_API_KEY, "Content-Type": "application/json"}

    with httpx.Client(timeout=30) as client:
        if method == "GET":
            resp = client.get(url, headers=headers)
        elif method == "POST":
            resp = client.post(url, headers=headers, json=json_data or {})
        elif method == "PUT":
            resp = client.put(url, headers=headers, json=json_data or {})
        else:
            raise ValueError(f"Unknown method: {method}")

        return resp.status_code, resp.json() if resp.text else {}

def check_config():
    """Check environment configuration"""
    log("Checking configuration...")

    if not WAHA_URL:
        log("ERROR: WAHA_URL not set in .env")
        return False
    if not WAHA_API_KEY:
        log("ERROR: WAHA_API_KEY not set in .env")
        return False

    log(f"WAHA_URL: {WAHA_URL}")
    log(f"WAHA_API_KEY: {'*' * 10}...{WAHA_API_KEY[-4:]}")
    log(f"SESSION: {SESSION_NAME}")
    log(f"WEBHOOK: {WEBHOOK_URL}")
    return True

def get_session_status():
    """Get current session status"""
    log(f"Checking session '{SESSION_NAME}'...")

    status_code, data = api_call("GET", f"/api/sessions/{SESSION_NAME}")

    if status_code == 404:
        log(f"Session '{SESSION_NAME}' not found")
        return None
    elif status_code != 200:
        log(f"Error getting session: {data}")
        return None

    log(f"Session status: {data.get('status')}")
    log(f"Connected as: {data.get('me')}")
    log(f"Webhooks: {data.get('config', {}).get('webhooks', [])}")

    return data

def setup_webhook():
    """Configure webhook on session"""
    log("Setting up webhook...")

    config = {
        "config": {
            "webhooks": [{
                "url": WEBHOOK_URL,
                "events": ["message"]
            }]
        }
    }

    status_code, data = api_call("PUT", f"/api/sessions/{SESSION_NAME}", config)

    if status_code == 200:
        log("Webhook configured successfully!")
        return True
    else:
        log(f"Error setting webhook: {data}")
        return False

def restart_session():
    """Stop and start session"""
    log("Restarting session...")

    # Stop
    log("Stopping session...")
    api_call("POST", f"/api/sessions/{SESSION_NAME}/stop")
    time.sleep(2)

    # Start
    log("Starting session...")
    status_code, data = api_call("POST", f"/api/sessions/{SESSION_NAME}/start")

    if status_code == 200:
        log("Session start requested")
        return True
    else:
        log(f"Error starting session: {data}")
        return False

def wait_for_working(max_wait=60):
    """Wait for session to become WORKING"""
    log(f"Waiting for session to be WORKING (max {max_wait}s)...")

    start = time.time()
    while time.time() - start < max_wait:
        status_code, data = api_call("GET", f"/api/sessions/{SESSION_NAME}")
        status = data.get("status", "UNKNOWN")
        me = data.get("me")

        log(f"Status: {status}, Me: {me}")

        if status == "WORKING" and me:
            log("Session is WORKING!")
            return True
        elif status == "SCAN_QR_CODE":
            log(">>> SCAN QR CODE di WAHA Dashboard! <<<")
        elif status == "FAILED":
            log("Session FAILED. Check WAHA logs.")
            return False

        time.sleep(3)

    log("Timeout waiting for session")
    return False

def test_webhook():
    """Send test message to webhook"""
    log("Testing webhook endpoint...")

    test_payload = {
        "event": "message",
        "session": SESSION_NAME,
        "payload": {
            "from": "6281234567890@c.us",
            "body": "halo test",
            "fromMe": False
        }
    }

    with httpx.Client(timeout=30) as client:
        resp = client.post(WEBHOOK_URL, json=test_payload)
        log(f"Webhook response: {resp.status_code} - {resp.text}")
        return resp.status_code == 200

def main():
    print("=" * 50)
    print("WAHA Setup & Test Script")
    print("=" * 50)

    # Check config
    if not check_config():
        sys.exit(1)

    print()

    # Get current status
    session = get_session_status()

    print()

    # Setup webhook
    setup_webhook()

    print()

    # Check if session needs restart
    if not session or session.get("status") != "WORKING":
        restart = input("Session not WORKING. Restart? (y/n): ").lower()
        if restart == 'y':
            restart_session()
            print()
            wait_for_working()

    print()

    # Test webhook
    test = input("Test webhook endpoint? (y/n): ").lower()
    if test == 'y':
        test_webhook()

    print()
    print("=" * 50)
    print("Setup complete!")
    print("Kirim pesan 'halo' ke nomor WAHA untuk test")
    print("=" * 50)

if __name__ == "__main__":
    main()
