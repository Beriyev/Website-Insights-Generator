from ollama import AsyncClient
from scraper.fetcher import fetch_static, fetch_rendered, fetch
from models import ExtractedContent, Insights
from scraper.extractor import extract_content
from core.config import OLLAMA_LLM_MODEL, OLLAMA_HOST
import httpx

async def analyze(url: str) -> Insights:
    html = await fetch(url)
    extracted_content = extract_content(html=html, url=url)
    client = AsyncClient(host=OLLAMA_HOST,timeout=httpx.Timeout(180.0))
    MAX_CONTENT_SIZE = 6000

    prompt = f"""Summarize the following webpage in 2-3 concise sentences and extract exactly 4-5 key points. Do not comment on the metadata itself (dates, authors, etc.), focus only on what the content is actually about.
            Each key point must be a single complete sentence, with no leading punctuation, bullet characters, or markdown formatting.
            Title: {extracted_content.title}
            Content:
            {extracted_content.text[:MAX_CONTENT_SIZE]}"""

    insights = await client.chat(
        model = OLLAMA_LLM_MODEL,
        messages=[
            {
                "role":"system",
                "content": "You are a content analysis assistant. Analyze only the webpage content given by the user. Never mention dates, timestamps, your knowledge cutoff, or metadata anomalies, focus purely on summarizing the substance of the content."
            },
            {
                "role":"user",
                "content": prompt
            }
        ],
        format=Insights.model_json_schema(),
        options={"num_predict":4000,"temperature":0}
    )

    content = insights.message.content
    if content is None:
        raise ValueError("Ollama did not return any content")
    final_insights = Insights.model_validate_json(content)
    return final_insights

async def analyze_text(title: str, text: str) -> Insights:
    client = AsyncClient(host=OLLAMA_HOST, timeout=httpx.Timeout(180.0))
    MAX_CONTENT_SIZE = 6000

    prompt = f"""Summarize the following webpage in 2-3 concise sentences and extract exactly 4-5 key points. Do not comment on the metadata itself (dates, authors, etc.), focus only on what the content is actually about.
            Each key point must be a single complete sentence, with no leading punctuation, bullet characters, or markdown formatting.
            Title: {title}
            Content:
            {text[:MAX_CONTENT_SIZE]}"""

    response = await client.chat(
        model=OLLAMA_LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a content analysis assistant. Analyze only the webpage content given by the user. Never mention dates, timestamps, your knowledge cutoff, or metadata anomalies, focus purely on summarizing the substance of the content."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        format=Insights.model_json_schema(),
        options={"num_predict": 4000, "temperature": 0}
    )

    content = response.message.content
    if content is None:
        raise ValueError("Ollama did not return any content")
    return Insights.model_validate_json(content)