from fastapi import FastAPI, Header, HTTPException, Request
import re, random, os

app = FastAPI()
API_KEY = "test_api_key"


def analyze_message(message: str):
    signals = []
    risk = 0.1
    msg = message.lower()

    if re.search(r"\botp\b|\bcode\b", msg):
        signals.append("otp_request")
        risk += 0.3

    if re.search(r"urgent|immediately|today|now", msg):
        signals.append("urgency")
        risk += 0.2

    if re.search(r"account|bank|wallet|suspended|blocked", msg):
        signals.append("account_threat")
        risk += 0.2

    if re.search(r"http|www\.|\.com", msg):
        signals.append("link_present")
        risk += 0.2

    scam_type = "legitimate"
    if risk >= 0.6:
        scam_type = "phishing"

    return scam_type, min(risk, 0.99), signals


def extract_entities(message: str):
    return {
        "phone_numbers": re.findall(r"\b\d{10}\b", message),
        "urls": re.findall(r"https?://\S+", message),
        "amounts": re.findall(r"\₹?\$?\d+", message),
    }


def generate_reply(scam_type):
    phishing = [
        "Can you explain what this is about?",
        "Which account are you referring to?",
        "I didn’t understand, can you clarify?",
    ]
    safe = ["Okay, noted.", "Thanks for the information."]

    return random.choice(phishing if scam_type == "phishing" else safe)


@app.get("/")
def home():
    return {"message": "Honeypot API is running"}


@app.post("/honeypot")
async def honeypot_endpoint(
    request: Request,
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    body = await request.json()

    # 🔑 Accept multiple possible keys
    message = (
        body.get("message")
        or body.get("text")
        or body.get("content")
    )

    if not message or not isinstance(message, str):
        raise HTTPException(status_code=400, detail="Invalid request body")

    scam_type, risk_score, signals = analyze_message(message)

    return {
        "status": "success",
        "scam_type": scam_type,
        "risk_score": risk_score,
        "signals": signals,
        "extracted_entities": extract_entities(message),
        "honeypot_reply": generate_reply(scam_type),
        "confidence": "high" if risk_score > 0.5 else "medium",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
