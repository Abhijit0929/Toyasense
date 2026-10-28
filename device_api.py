import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from supabase import create_client
from urllib.parse import urlparse
load_dotenv()

# Read environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "").strip()

# Validate configuration
if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL is missing")

if not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_KEY is missing")

parsed_url = urlparse(SUPABASE_URL)

if parsed_url.scheme != "https" or not parsed_url.netloc:
    raise RuntimeError(
        "SUPABASE_URL must be a valid HTTPS project URL"
    )

if parsed_url.path not in ("", "/"):
    raise RuntimeError(
        "SUPABASE_URL must not contain a path such as /rest/v1"
    )

print("Supabase host:", parsed_url.netloc)
print("Supabase path:", repr(parsed_url.path))

# Initialize Supabase client
supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

print("Supabase client initialized successfully")

app = FastAPI(title="ToyaSense Registration API")


class DeviceRegistration(BaseModel):
    device_id: str = Field(min_length=1, max_length=100)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/devices/register")
def register_device(device: DeviceRegistration):
    device_id = device.device_id.strip()

    if not device_id.startswith("TOYASENSE-"):
        raise HTTPException(400, "Invalid device ID")

    now = datetime.now(timezone.utc).isoformat()

    try:
        existing = (
        supabase.table("taps")
        .select("id, device_id")
        .eq("device_id", device_id)
        .limit(1)
        .execute()
    )

        if existing.data:
            supabase.table("taps").update({
                "last_seen_at": now
            }).eq("device_id", device_id).execute()

            is_new = False

        else:
            supabase.table("taps").upsert(
                {
                    "device_id": device_id,
                    "tap_name": device_id,
                    "status": "active",
                    "last_seen_at": now,
                },
                on_conflict="device_id",
            ).execute()

            is_new = True

        return {
            "registered": True,
            "is_new": is_new,
            "device_id": device_id
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail="Registration failed"
        )