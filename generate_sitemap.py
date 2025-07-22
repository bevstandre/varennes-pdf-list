import json
from datetime import datetime
from pathlib import Path

# Charger les données du JSON
with open("pdf_links.json", "r", encoding="utf-8") as f:
    links = json.load(f)

# Générer le contenu du sitemap
sitemap_entries = []
for item in links:
    url = item.get("url")
    date = item.get("date") or datetime.today().strftime("%Y-%m-%d")
    sitemap_entries.append(f"""  <url>
    <loc>{url}</loc>
    <lastmod>{date}</lastmod>
  </url>""")

sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(sitemap_entries)}
</urlset>"""

# Écrire le fichier sitemap.xml
Path("sitemap.xml").write_text(sitemap_content, encoding="utf-8")
print("✅ sitemap.xml généré.")
