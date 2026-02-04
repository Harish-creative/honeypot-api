from fastapi import FastAPI, Header, HTTPException, Request
import os

app = FastAPI()

API_KEY = "test_api_key"


@app.get("/")
def home():
    return {"status": "Honeypot API running"}


@app.post("/honeypot")
async def honeypot(request: Request, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Safely read body (tester-friendly)
    try:
        body = await request.json()
    except:
        body = {}

    message = body.get("message", "")

    scam_type = "phishing" if "otp" in message.lower() else "legitimate"

    return {
        "scam_type": scam_type,
        "risk_score": 0.7 if scam_type == "phishing" else 0.2,
        "signals": ["otp_request"] if scam_type == "phishing" else [],
        "honeypot_reply": "Can you please clarify your request?"
    }
