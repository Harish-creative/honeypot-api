from fastapi import FastAPI, Request
import os

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "ok"}

@app.api_route("/honeypot", methods=["GET", "POST"])
async def honeypot(request: Request):

    message = ""

    if request.method == "POST":
        # Try JSON safely
        try:
            data = await request.json()
            if isinstance(data, dict):
                message = str(data.get("message", ""))
        except:
            pass

        # Try raw body (tester sometimes sends plain text)
        if not message:
            try:
                raw = await request.body()
                message = raw.decode("utf-8", errors="ignore")
            except:
                pass

    scam = "phishing" if "otp" in message.lower() else "legitimate"

    return {
        "status": "success",
        "scam_type": scam,
        "risk_score": 0.7 if scam == "phishing" else 0.2,
        "signals": ["otp_request"] if scam == "phishing" else [],
        "honeypot_reply": "Please clarify your request.",
        "received_message": message
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
