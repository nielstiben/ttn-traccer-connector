from fastapi import FastAPI, Request, HTTPException, Depends
import httpx
import os
from dotenv import load_dotenv
import logging
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# Load environment variables
load_dotenv()

# Load required environment variables
TRACCAR_OSMAND_URL = os.getenv("TRACCAR_OSMAND_URL")
TTN_WEBHOOK_USERNAME = os.getenv("TTN_WEBHOOK_USERNAME")
TTN_WEBHOOK_PASSWORD = os.getenv("TTN_WEBHOOK_PASSWORD")

if not TRACCAR_OSMAND_URL or not TTN_WEBHOOK_USERNAME or not TTN_WEBHOOK_PASSWORD:
    raise ValueError("TRACCAR_OSMAND_URL, TTN_WEBHOOK_USERNAME, and TTN_WEBHOOK_PASSWORD must be set in the .env file")

# Load optional environment variables
PAYLOAD_KEY_LONGITUDE = os.getenv("PAYLOAD_KEY_LONGITUDE", "longitude")
PAYLOAD_KEY_LATITUDE = os.getenv("PAYLOAD_KEY_LATITUDE", "latitude")
PAYLOAD_KEY_BATTERY = os.getenv("PAYLOAD_KEY_BATTERY", "battery")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != TTN_WEBHOOK_USERNAME or credentials.password != TTN_WEBHOOK_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return credentials

@app.post("/webhook")
async def webhook(request: Request, credentials: HTTPBasicCredentials = Depends(authenticate)):
    try:
        data = await request.json()
        logger.info(f"Received data from TTN: {data}")

        # Extract required fields
        device_id = data.get("end_device_ids", {}).get("device_id")
        decoded_payload = data.get("uplink_message", {}).get("decoded_payload", {})

        if not device_id:
            return {"error": "Device ID missing"}

        # Define mapping of payload keys to parameter names
        payload_fields = {
            "lat": PAYLOAD_KEY_LATITUDE,
            "lon": PAYLOAD_KEY_LONGITUDE,
            "batt": PAYLOAD_KEY_BATTERY
        }

        # Build position parameters only with present values
        position_params = {"id": device_id}
        missing_fields = []

        for param_key, payload_key in payload_fields.items():
            value = decoded_payload.get(payload_key)
            if value is not None:
                position_params[param_key] = value
            else:
                missing_fields.append(payload_key)

        if missing_fields:
            logger.warning(f"Missing payload fields: {', '.join(missing_fields)}")

        # Make the GET request
        async with httpx.AsyncClient() as client:
            print(f"GET to {TRACCAR_OSMAND_URL}/api/positions. Payload: {position_params}")
            response = await client.get(
                f"{TRACCAR_OSMAND_URL}/api/positions",
                params=position_params
            )
            response.raise_for_status()

        return {"message": "Data forwarded successfully"}

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return {"error": str(e)}
