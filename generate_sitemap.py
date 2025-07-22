import json
from datetime import datetime

SITEMAP_FILENAME = "sitemap.xml"
JSON_FILENAME = "pdf_links.json"
BASE_URL = "https://raw.githubusercontent.com/bevstandre/varennes-pdf-list/main/"

def main():
    try:
        with open(JSON_FILENAME, "r", encoding="utf-8") as f:
            pdf_links = json.load(f)
    except Exception as e:
        print(f"Erreur en lisant {JSON_FILENAME} : {e}")
        return

    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    sitemap_entries = []

    for link in pdf_links:
        sitemap_entries.append(f"""  <url>
    <loc>{link}</loc>
    <lastmod>{now}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>""")

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset
  xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
    http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
{chr(10).join(sitemap_entries)}
</urlset>
"""

    try:
        with open(SITEMAP_FILENAME, "w", encoding="utf-8") as f:
            f.write(sitemap_content)
        print(f"Sitemap généré avec succès ({len(pdf_links)} liens).")
    except Exception as e:
        print(f"Erreur lors de l'écriture du sitemap : {e}")

if __name__ == "__main__":
    main()
