from fastapi import FastAPI, Request
import os

app = FastAPI()

@app.api_route("/", methods=["GET", "POST", "OPTIONS"])
async def root(request: Request):
    return {"status": "success", "reply": "ok"}

@app.api_route("/honeypot", methods=["GET", "POST", "OPTIONS"])
async def honeypot(request: Request):

    # Handle OPTIONS (preflight)
    if request.method == "OPTIONS":
        return {"status": "success", "reply": "ok"}

    text = ""

    # Try JSON safely
    try:
        body = await request.json()
        if isinstance(body, dict):
            text = body.get("message", {}).get("text", "")
    except:
        pass

    # Try raw body
    if not text:
        try:
            raw = await request.body()
            text = raw.decode("utf-8", errors="ignore")
        except:
            pass

    msg = str(text).lower()

    # Honeypot logic
    if any(k in msg for k in ["bank", "blocked", "verify", "otp", "account", "urgent"]):
        reply = "Why is my account being suspended?"
    else:
        reply = "Can you explain what this message is about?"

    # EXACT schema expected
    return {
        "status": "success",
        "reply": reply
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
