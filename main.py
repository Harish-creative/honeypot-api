from fastapi import FastAPI, Request, Header, HTTPException
import os

app = FastAPI()

API_KEY = "test_api_key"

# Root health check
@app.api_route("/", methods=["GET", "OPTIONS"])
async def root():
    return {"status": "success", "reply": "ok"}

# Honeypot endpoint
@app.api_route("/honeypot", methods=["GET", "POST", "OPTIONS"])
async def honeypot(request: Request, x_api_key: str = Header(None)):

    # OPTIONS preflight
    if request.method == "OPTIONS":
        return {"status": "success", "reply": "ok"}

    # API Key validation
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    text = ""

    # Try JSON body
    try:
        body = await request.json()
        if isinstance(body, dict):
            # Hackathon nested format
            if "message" in body and isinstance(body["message"], dict):
                text = body["message"].get("text", "")
            else:
                text = body.get("text", "")
    except:
        pass

    # Fallback raw body
    if not text:
        try:
            raw = await request.body()
            text = raw.decode("utf-8", errors="ignore")
        except:
            pass

    msg = str(text).lower()

    # Honeypot logic
    scam_words = ["bank", "blocked", "verify", "otp", "account", "urgent", "suspended"]

    if any(word in msg for word in scam_words):
        reply = "Why is my account being suspended?"
    else:
        reply = "Can you explain what this message is about?"

    # EXACT response schema expected by tester
    return {
        "status": "success",
        "reply": reply
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
