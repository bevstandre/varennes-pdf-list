import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import json
import time

SITEMAP_URL = "https://www.ville.varennes.qc.ca/sitemap.xml"
OUTPUT_FILE = "pdf_links.json"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_sitemap_urls(sitemap_url):
    resp = requests.get(sitemap_url, headers=HEADERS)
    tree = ET.fromstring(resp.content)
    urls = [url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
            for url in tree.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url')]
    return urls

def find_pdfs_in_page(url):
    pdf_links = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.lower().endswith('.pdf'):
                if href.startswith('/'):
                    href = 'https://www.ville.varennes.qc.ca' + href
                elif not href.startswith('http'):
                    href = url.rsplit('/', 1)[0] + '/' + href
                pdf_links.append(href)
    except Exception as e:
        print(f"Erreur sur {url}: {e}")
    return pdf_links

def is_pdf_link_working(url):
    try:
        resp = requests.head(url, headers=HEADERS, timeout=10, allow_redirects=True)
        return resp.status_code == 200
    except Exception:
        return False

def main():
    urls = get_sitemap_urls(SITEMAP_URL)
    all_pdf_links = set()
    for page_url in urls:
        pdf_links = find_pdfs_in_page(page_url)
        for pdf_url in pdf_links:
            if is_pdf_link_working(pdf_url):
                all_pdf_links.add(pdf_url)
        time.sleep(0.5)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(list(all_pdf_links)), f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
