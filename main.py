from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import scrape, analyze

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "running"}

app.include_router(scrape.router)
app.include_router(analyze.router)
