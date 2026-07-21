import sys
import asyncio

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import APIRouter, HTTPException
from models import ScrapedSource, ScrapeRequest, ScrapeResponse
from scraper.fetcher import fetch
from scraper.extractor import extract_content

router = APIRouter()

@router.post("/scrape",response_model=ScrapeResponse)
async def scrape(request: ScrapeRequest):
    html = await fetch(request.url)
    if not html:
        raise HTTPException(status_code=422, detail="Could not extract the HTML.")
    extracted = extract_content(html,request.url)
    if not extracted.text:
        raise HTTPException(status_code=422, detail="Could not extract the content.")
    return ScrapeResponse(url=request.url, **extracted.model_dump())

