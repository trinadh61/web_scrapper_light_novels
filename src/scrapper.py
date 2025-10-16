from playwright.async_api import async_playwright

async def fetch_page_content(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, wait_until='networkidle')
        content = await page.content()
        await browser.close()
        return content