import requests
from bs4 import BeautifulSoup
import os
import re

OUTPUT_DIR = "proceedings_pdfs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_pdf_links(page_url):
    response = requests.get(page_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    pdf_links = []
    for a in soup.find_all("a", href=True, type="application/pdf"):
        href = a["href"]
        if href.startswith("/"):
            href = BASE_URL + href
        pdf_links.append((a.text.strip(), href))
    return pdf_links

def extract_pdf_name(url):
    match = re.search(r'/reports/(.+?\.pdf)', url)
    if match:
        filename = match.group(1)
        filename_clean = filename.replace(' ', '_')
        return filename_clean
    return None

def download_pdf(name, url, output_dir):
    filename = extract_pdf_name(url)
    if filename == None:
        return #TODO: build this error reporting system out
    filepath = os.path.join(output_dir, filename)
    print(f"Downloading: {url} -> {filepath}")
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        #with open(filepath, "wb") as f:
        #    for chunk in r.iter_content(chunk_size=8192):
        #        if chunk:
        #            f.write(chunk)
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def main(pdf_page_url):
    pdf_links = get_pdf_links(pdf_page_url)
    print(len(pdf_links))
    for name, url in pdf_links:
        print(name, url)
        download_pdf(name, url, OUTPUT_DIR)

if __name__ == "__main__":
    #2024 page right now
    page_url = "https://www.chicityclerk.com/legislation-records/journals-and-reports/journals-proceedings?field_year_value=46"
    main(page_url)
