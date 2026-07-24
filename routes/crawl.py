from scraper.crawler import Crawler, CrawlConfig, CrawlResult
from scraper.extractor import extract_content
from models import CrawlRequest, CrawlResponse, ScrapeResponse
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/crawl",response_model=CrawlResponse)
async def crawl(request: CrawlRequest):
    config = CrawlConfig(max_pages=request.max_pages)
    crawler = Crawler(start_url=request.url,config=config)
    crawl_results = await crawler.run()
    results = []
    failed_pages = []
    success_count = 0
    pages_visited = 0

    for result in crawl_results:
        if result.success:
            extracted = extract_content(result.html,result.url)
            results.append(ScrapeResponse(url=result.url,**extracted.model_dump()))
            success_count+=1
        else:
            failed_pages.append(result.url)
        pages_visited+=1

    return CrawlResponse(
        pages_visited=pages_visited,
        results = results,
        failed_pages = failed_pages,
        success_count = success_count
    )


    

