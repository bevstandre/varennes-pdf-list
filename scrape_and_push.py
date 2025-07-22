import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import time

BASE_URL = "https://www.ville.varennes.qc.ca"

def scrape_pdfs(base_url):
    visited = set()
    pdf_links = set()
    from collections import deque
    queue = deque([base_url])

    while queue:
        url = queue.popleft()
        if url in visited:
            continue
        visited.add(url)
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, "html.parser")
            for link in soup.find_all("a", href=True):
                href = link['href']
                href = urljoin(url, href)
                parsed = urlparse(href)
                if parsed.netloc != urlparse(base_url).netloc:
                    continue
                if href.lower().endswith(".pdf"):
                    pdf_links.add(href)
                elif href.startswith(base_url) and href not in visited and not href.lower().endswith((".pdf", ".jpg", ".png", ".gif")):
                    queue.append(href)
        except Exception as e:
            print(f"Erreur sur {url}: {e}")

    return sorted(pdf_links)

def filter_valid_pdfs(pdf_links):
    valid_pdfs = []
    headers = {"User-Agent": "Mozilla/5.0"}
    for link in pdf_links:
        try:
            r = requests.head(link, headers=headers, allow_redirects=True, timeout=10)
            if r.status_code == 200:
                valid_pdfs.append(link)
            else:
                print(f"Invalid PDF (status {r.status_code}): {link}")
            time.sleep(0.5)
        except Exception as e:
            print(f"Erreur lors de la vérification de {link}: {e}")
    return valid_pdfs

def main():
    pdf_links = scrape_pdfs(BASE_URL)
    valid_pdfs = filter_valid_pdfs(pdf_links)
    with open("pdf_links.json", "w", encoding="utf-8") as f:
        json.dump(valid_pdfs, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
