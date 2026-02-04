from fastapi import FastAPI, Request
import os

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "ok"}

@app.post("/honeypot")
async def honeypot(request: Request):

    try:
        body = await request.json()
    except:
        body = {}

    text = ""

    try:
        text = body.get("message", {}).get("text", "")
    except:
        text = ""

    msg = text.lower()

    if "bank" in msg or "blocked" in msg or "verify" in msg:
        reply = "Why is my account being suspended?"
    else:
        reply = "Can you explain what this message is about?"

    return {
        "status": "success",
        "reply": reply
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
