from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import scrape, analyze, crawl, crawl_analyze

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
app.include_router(crawl.router)
app.include_router(crawl_analyze.router)


