import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from supabase import create_client

load_dotenv()

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_KEY"]
)

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

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Registration failed"
        )