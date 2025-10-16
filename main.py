import asyncio
from src.pdf_exporter import export_page_to_pdf

def main():
    url = "https://example-lightnovel-website.com/chapter-1"  # Replace with your target URL
    output_pdf = "lightnovel-chapter-1.pdf"
    asyncio.run(export_page_to_pdf(url, output_pdf))

if __name__ == "__main__":
    main()