from fastapi import FastAPI
import threading
import bot  # this imports bot.py and starts polling

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "bot": "running"}

def start():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

threading.Thread(target=start).start()
