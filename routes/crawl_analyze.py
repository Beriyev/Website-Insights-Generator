from models import CrawledAnalyzedResponse,CrawlRequest,AnalyzedPage,ScrapeResponse
from scraper.crawler import CrawlConfig, Crawler
from scraper.extractor import extract_content
from insights.llm import analyze_text
from fastapi import APIRouter,HTTPException

router = APIRouter()

@router.post("/crawl-analyze",response_model=CrawledAnalyzedResponse)
async def crawl_analyze(request: CrawlRequest):
    config = CrawlConfig(max_pages=request.max_pages)
    crawler = Crawler(start_url=request.url,config=config)
    crawl_results = await crawler.run()
    results = []
    pages_visited = 0
    failed_pages = []
    success_count = 0

    for result in crawl_results:
        if result.success:
            extracted = extract_content(result.html,result.url)
            success_count+=1
            extracted_title = extracted.title if extracted.title!=None else "Untitled"
            insights = await analyze_text(title=extracted_title,text=extracted.text)
            page = AnalyzedPage(url=result.url,title=extracted_title,**insights.model_dump())
            results.append(page)
        else:
            failed_pages.append(result.url)
        pages_visited+=1

    analyzed_response = CrawledAnalyzedResponse(
        pages_visited=pages_visited,
        results=results,
        failed_pages=failed_pages,
        success_count=success_count
    )

    return analyzed_response






