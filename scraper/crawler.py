import asyncio
from dataclasses import dataclass, field
from collections import deque

from scraper.links import extract_links, is_same_domain, normalise_url
from scraper.fetcher import fetch

@dataclass
class CrawlConfig:
    max_pages: int = 10
    max_depth: int = 2
    delay_seconds: float = 1.0

@dataclass
class CrawlResult:
    url: str
    depth: int
    html: str
    success: bool

class Crawler:
    def __init__(self,start_url,config):
        self.base_url = start_url
        self.config = config
        self.frontier = deque()
        self.visited = set()
        self.frontier.append((start_url,0))
        self.results = []

    async def run(self):
        while self.frontier and len(self.visited) < self.config.max_pages:
            url,depth = self.frontier.popleft()
            if url in self.visited:
                continue
            self.visited.add(url)
            html = await fetch(url)
            success = True if html != "" else False
            crawl_result = CrawlResult(
                url = url,
                depth = depth,
                html = html,
                success = success
            )
            self.results.append(crawl_result)
            if depth >= self.config.max_depth or success == False:
                continue
            link_set = extract_links(html,url)
            for link in link_set:
                if link in self.visited:
                    continue
                if is_same_domain(link,self.base_url):
                    self.frontier.append((link,depth+1))
        return self.results
        
