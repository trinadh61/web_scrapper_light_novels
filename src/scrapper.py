import os
from urllib import request
from urllib.parse import urlparse
from playwright.async_api import async_playwright

async def fetch_page_content(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, wait_until='networkidle')
        content = await page.content()
        await browser.close()
        return content
    

async def fetch_image_urls(url, xpath):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, wait_until='networkidle')
        # Locate all img elements under the given XPath and extract their src attributes
        img_elements = await page.locator(f'xpath={xpath}//img').all()
        img_urls = []
        for img in img_elements:
            src = await img.get_attribute('src')
            if src:
                img_urls.append(src)
        await browser.close()
        return img_urls
    
def is_trusted_domain(url, allowed_domains):
    domain = urlparse(url).netloc
    return any(domain.endswith(allowed) for allowed in allowed_domains)

def is_safe_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https")

def has_safe_extension(url, allowed_exts=None):
    if allowed_exts is None:
        allowed_exts = [".jpg", ".jpeg", ".png", ".webp"]
    ext = os.path.splitext(urlparse(url).path)[1].lower()
    return ext in allowed_exts

def download_images(img_urls, output_dir, allowed_domains=None, max_size_mb=5):
    os.makedirs(output_dir, exist_ok=True)
    for idx, url in enumerate(img_urls):
        if not is_safe_url(url):
            print(f"Skipping unsafe URL scheme: {url}")
            continue
        if allowed_domains and not is_trusted_domain(url, allowed_domains):
            print(f"Skipping untrusted domain: {url}")
            continue
        if not has_safe_extension(url):
            print(f"Skipping suspicious extension: {url}")
            continue
        try:
            response = request.get(url, timeout=10, stream=True)
            response.raise_for_status()
            content_length = int(response.headers.get("content-length", 0))
            if content_length > max_size_mb * 1024 * 1024:
                print(f"Skipping large file ({content_length} bytes): {url}")
                continue
            ext = os.path.splitext(urlparse(url).path)[1] or ".jpg"
            filename = f"image_{idx+1}{ext}"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded: {filepath}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")