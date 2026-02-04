from fastapi import FastAPI, Request
import os

app = FastAPI()


@app.get("/")
def home():
    return {"status": "Honeypot API running"}


@app.api_route("/honeypot", methods=["GET", "POST"])
async def honeypot(request: Request):
    message = ""

    if request.method == "POST":
        # 1️⃣ Try JSON
        try:
            body = await request.json()
            if isinstance(body, dict):
                message = body.get("message", "")
        except:
            pass

        # 2️⃣ Try form data
        if not message:
            try:
                form = await request.form()
                message = form.get("message", "")
            except:
                pass

        # 3️⃣ Try raw text
        if not message:
            try:
                raw = await request.body()
                message = raw.decode("utf-8")
            except:
                pass

    scam_type = "phishing" if "otp" in message.lower() else "legitimate"

    return {
        "status": "success",
        "scam_type": scam_type,
        "risk_score": 0.7 if scam_type == "phishing" else 0.2,
        "signals": ["otp_request"] if scam_type == "phishing" else [],
        "extracted_message": message,
        "honeypot_reply": "Please clarify your request."
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
