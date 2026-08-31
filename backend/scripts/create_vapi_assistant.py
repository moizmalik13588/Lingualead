import json
import os
import sys
import httpx
from dotenv import load_dotenv

# Load .env from project root or backend parent
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.env")))
load_dotenv(os.path.abspath(os.path.join(os.path.dirname(__file__), "../.env")))

VAPI_API_KEY = os.getenv("VAPI_API_KEY")
if not VAPI_API_KEY or VAPI_API_KEY == "your_vapi_api_key_here":
    print("ERROR: VAPI_API_KEY is not set or is still the default placeholder in .env")
    sys.exit(1)

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../vapi_assistant_config.json"))
if not os.path.exists(CONFIG_PATH):
    print(f"ERROR: Configuration file not found at {CONFIG_PATH}")
    sys.exit(1)

try:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        assistant_config = json.load(f)
except Exception as e:
    print(f"ERROR: Failed to load assistant config JSON: {e}")
    sys.exit(1)

url = "https://api.vapi.ai/assistant"
headers = {
    "Authorization": f"Bearer {VAPI_API_KEY}",
    "Content-Type": "application/json",
}

print("Creating Vapi assistant via Vapi API...")

try:
    response = httpx.post(url, json=assistant_config, headers=headers, timeout=30.0)
    if response.status_code in (200, 201):
        data = response.json()
        assistant_id = data.get("id")
        print("\n=== VAPI ASSISTANT CREATED SUCCESSFULLY ===")
        print(f"Assistant ID: {assistant_id}")
        print("\nAdd this to your .env file:")
        print(f"VAPI_ASSISTANT_ID={assistant_id}")
        print("===========================================\n")
    else:
        print(f"ERROR: Failed to create Vapi assistant (Status {response.status_code})")
        print(response.text)
        sys.exit(1)
except Exception as e:
    print(f"ERROR: Exception occurred while calling Vapi API: {e}")
    sys.exit(1)
