import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, Field
from supabase import Client, create_client

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
# Use a server-side Supabase secret/service-role key here, never the publishable/anon key.
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "Set SUPABASE_URL and SUPABASE_SECRET_KEY in the project root .env file. "
        "Use a Supabase secret key (sb_secret_...) or legacy service_role key."
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="NEXOVERSE API")
app.mount("/css", StaticFiles(directory=ROOT_DIR / "css"), name="css")
app.mount("/js", StaticFiles(directory=ROOT_DIR / "js"), name="js")
app.mount("/demos", StaticFiles(directory=ROOT_DIR / "demos", html=True), name="demos")


class Enquiry(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    email: EmailStr
    service: str = Field(min_length=1, max_length=100)
    message: str = Field(min_length=1, max_length=2000)


@app.get("/")
def home():
    return FileResponse(ROOT_DIR / "index.html")


@app.post("/api/enquiries", status_code=201)
def create_enquiry(enquiry: Enquiry):
    data = {
        "name": enquiry.name.strip(),
        "email": str(enquiry.email),
        "service": enquiry.service.strip(),
        "message": enquiry.message.strip(),
    }

    try:
        result = supabase.table("enquiries").insert(data).execute()
        return {"message": "Enquiry submitted successfully", "data": result.data}
    except Exception as exc:
        # Details stay in the backend terminal; never expose database internals to visitors.
        print("SUPABASE INSERT ERROR:", repr(exc))
        raise HTTPException(
            status_code=502,
            detail="We could not save your enquiry. Please try again shortly.",
        )
