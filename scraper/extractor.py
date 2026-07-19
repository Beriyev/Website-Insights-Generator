import trafilatura
from models import ExtractedContent

def extract_content(html: str, url: str) -> ExtractedContent:
    content = trafilatura.extract(html,url=url)
    metadata = trafilatura.extract_metadata(html)
    return ExtractedContent(
        title=metadata.title if metadata else None,
        author=metadata.author if metadata else None,
        date=metadata.date if metadata else None,
        text=content or ""
    )

