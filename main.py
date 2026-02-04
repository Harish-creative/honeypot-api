from fastapi import FastAPI, Request
import os

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "ok"}

@app.api_route("/honeypot", methods=["GET", "POST"])
async def honeypot(request: Request):

    text = ""

    if request.method == "POST":
        # Try JSON first
        try:
            body = await request.json()
            if isinstance(body, dict):
                text = body.get("message", {}).get("text", "")
        except:
            pass

        # Fallback to raw body
        if not text:
            try:
                raw = await request.body()
                text = raw.decode("utf-8", errors="ignore")
            except:
                pass

    msg = str(text).lower()

    # Honeypot reply logic (agentic)
    if any(word in msg for word in ["bank", "blocked", "verify", "otp", "account"]):
        reply = "Why is my account being suspended?"
    else:
        reply = "Can you explain what this message is about?"

    # EXACT response schema required by hackathon tester
    return {
        "status": "success",
        "reply": reply
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
