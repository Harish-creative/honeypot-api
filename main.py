from fastapi import FastAPI, Request
import os
import re

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "ok"}

@app.api_route("/honeypot", methods=["GET", "POST"])
async def honeypot(request: Request):

    message = ""

    if request.method == "POST":
        try:
            data = await request.json()
            if isinstance(data, dict):
                message = str(data.get("message", ""))
        except:
            try:
                raw = await request.body()
                message = raw.decode("utf-8", errors="ignore")
            except:
                message = ""

    msg = message.lower()

    scam_type = "phishing" if "otp" in msg else "legitimate"
    risk_score = 0.7 if scam_type == "phishing" else 0.2
    signals = ["otp_request"] if scam_type == "phishing" else []

    phones = re.findall(r"\b\d{10}\b", message)
    urls = re.findall(r"https?://\S+", message)
    amounts = re.findall(r"\₹?\$?\d+", message)

    extracted_entities = {
        "phone_numbers": phones,
        "urls": urls,
        "amounts": amounts
    }

    return {
        "status": "success",
        "scam_type": scam_type,
        "risk_score": risk_score,
        "signals": signals,
        "extracted_entities": extracted_entities,
        "honeypot_reply": "Please clarify your request."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
