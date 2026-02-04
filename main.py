from fastapi import FastAPI, Header, HTTPException, Request
import os

app = FastAPI()

# API key expected by the tester
API_KEY = "test_api_key"


@app.get("/")
def home():
    return {"status": "Honeypot API running"}


@app.api_route("/honeypot", methods=["GET", "POST"])
async def honeypot(request: Request, x_api_key: str = Header(None)):
    # Authentication
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    message = ""

    # Safely read request body (tester may send empty or malformed JSON)
    if request.method == "POST":
        try:
            body = await request.json()
            if isinstance(body, dict):
                message = body.get("message", "")
        except:
            message = ""

    # Simple scam detection logic
    scam_type = "phishing" if "otp" in message.lower() else "legitimate"

    return {
        "status": "success",
        "scam_type": scam_type,
        "risk_score": 0.7 if scam_type == "phishing" else 0.2,
        "signals": ["otp_request"] if scam_type == "phishing" else [],
        "honeypot_reply": "Can you please clarify your request?"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )
