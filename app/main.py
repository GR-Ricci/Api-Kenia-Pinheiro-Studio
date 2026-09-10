from fastapi import FastAPI

app = FastAPI(title="Kenia Studio")

@app.get("/")
def home():
    return {"message" : "Hello World"}
