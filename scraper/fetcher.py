from playwright.async_api import async_playwright
import httpx
from core.config import FETCH_TIMEOUT, RENDER_TIMEOUT, USER_AGENT, STATIC_LENGTH_THRESHOLD

async def fetch_static(url: str) -> str:
    async with httpx.AsyncClient(timeout=FETCH_TIMEOUT,headers={"User-Agent": USER_AGENT}) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
        except httpx.RequestError as e:
            print(f"An error occurred while requesting {url}: {e}")
            return ""
        except httpx.HTTPStatusError as e:
            print(f"Error response {e.response.status_code} while requesting {url}: {e}")
            return ""
        
async def fetch_rendered(url: str) -> str:
    async with async_playwright() as client:
        browser = await client.chromium.launch(headless = True)
        page = await browser.new_page()
        try:
            await page.goto(url, timeout = RENDER_TIMEOUT)
            await page.wait_for_load_state("networkidle")
            html = await page.content()
            return html
        except Exception as e:
            print(f"An error occurred while requesting {url}: {e}") 
            return ""
        finally:
            await browser.close()

async def fetch(url: str) -> str:
    html = await fetch_static(url)
    if(len(html)<STATIC_LENGTH_THRESHOLD):
        print("Static failed, using rendered")
        html = await fetch_rendered(url)
    return html
