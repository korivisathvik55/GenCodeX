from fastapi import FastAPI

app = FastAPI(title="GenCodeX API")


@app.get("/")
def home():
    return {
        "message": "Welcome to GenCodeX!",
        "status": "running"
    }