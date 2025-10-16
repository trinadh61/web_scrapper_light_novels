from playwright.async_api import async_playwright

async def export_page_to_pdf(url, output_pdf):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, wait_until='networkidle')
        await page.pdf(path=output_pdf, format="A4", print_background=True)
        await browser.close()