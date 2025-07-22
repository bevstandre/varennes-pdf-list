import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import json
import time
import sys

SITEMAP_URL = "https://www.ville.varennes.qc.ca/sitemap.xml"
OUTPUT_FILE = "pdf_links.json"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_sitemap_urls(sitemap_url):
    try:
        resp = requests.get(sitemap_url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        print(f"Erreur lors du chargement du sitemap : {e}")
        sys.exit(1)
    try:
        tree = ET.fromstring(resp.content)
        urls = [url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
                for url in tree.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url')]
        return urls
    except Exception as e:
        print(f"Erreur de parsing XML : {e}")
        sys.exit(1)

def find_pdfs_in_page(url):
    pdf_links = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.lower().endswith('.pdf'):
                if href.startswith('/'):
                    href = 'https:/
