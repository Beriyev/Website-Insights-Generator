from pydantic import BaseModel

class ExtractedContent(BaseModel):
    title: str | None = None 
    author: str | None = None
    date: str | None = None
    text: str

class ScrapedSource(BaseModel):
    source_type: str
    url: str
    title: str | None = None
    content: str
    metadata: dict = {}

class ScrapeRequest(BaseModel):
    url: str

class ScrapeResponse(BaseModel):
    url: str
    title: str | None = None
    text: str
    author: str | None = None
    date: str | None = None

class AnalyzeRequest(BaseModel):
    url: str

class AnalyzeResponse(BaseModel):
    url: str
    title: str | None = None
    summary: str
    key_points: list[str]

class CrawlRequest(BaseModel):
    url: str
    max_pages: int = 10

class CrawlResponse(BaseModel):
    pages_visited: int
    results: list[ScrapeResponse]
    failed_pages: list[str]
    success_count: int 

class Insights(BaseModel):
    summary: str
    key_points: list[str]

class AnalyzedPage(BaseModel):
    url: str
    title: str | None = None
    summary: str
    key_points: list[str]

class CrawledAnalyzedResponse(BaseModel):
    pages_visited: int
    results: list[AnalyzedPage]
    failed_pages: list[str]
    success_count: int