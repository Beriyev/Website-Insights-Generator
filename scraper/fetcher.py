import asyncio
from playwright.async_api import async_playwright
import httpx

async def fetch_static(url: str) -> str:
    async with httpx.AsyncClient(timeout=10.0,headers={"User-Agent": "Mozilla/5.0"}) as client:
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
            await page.goto(url, timeout = 15000)
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
    if(len(html)<3000):
        print("Static failed, using rendered")
        html = await fetch_rendered(url)
    return html


if __name__ == "__main__":
    import asyncio

    async def main():
        html = await fetch("https://react-shopping-cart-67954.firebaseapp.com/")
        print(len(html))

    asyncio.run(main())