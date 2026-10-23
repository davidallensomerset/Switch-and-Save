#!/usr/bin/env python3
"""Zero-token static HTML + sitemap generator for Switch & Save Alternatives."""
import json, html, pathlib

ROOT = pathlib.Path(__file__).parent
PAGES_FILE = ROOT / "pages" / "pages.json"
DIST = ROOT / "dist"
DIST.mkdir(exist_ok=True)

STYLE = """
:root { --bg:#f8fafc; --card:#ffffff; --text:#0f172a; --muted:#475569; --accent:#0284c7; --border:#e2e8f0; --good:#16a34a; }
* { box-sizing:border-box; }
body { font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; background:var(--bg); color:var(--text); margin:0; line-height:1.6; }
header { background:#0f172a; color:#fff; padding:1.5rem 1rem; }
.wrap { max-width:880px; margin:0 auto; padding:0 1rem; }
header a { color:#38bdf8; text-decoration:none; font-weight:600; }
h1 { margin:0.4rem 0; font-size:1.75rem; }
.badge { display:inline-block; background:#e0f2fe; color:#0369a1; font-size:0.8rem; font-weight:600; padding:0.2rem 0.6rem; border-radius:999px; }
.card { background:var(--card); border:1px solid var(--border); border-radius:10px; padding:1.25rem; margin:1.25rem 0; box-shadow:0 1px 2px rgba(0,0,0,0.03); }
table { width:100%; border-collapse:collapse; margin:1rem 0; background:var(--card); border-radius:8px; overflow:hidden; border:1px solid var(--border); }
th, td { text-align:left; padding:0.75rem; border-bottom:1px solid var(--border); font-size:0.95rem; }
th { background:#f1f5f9; font-weight:600; }
.btn { display:inline-block; background:var(--accent); color:#fff; padding:0.45rem 0.85rem; border-radius:6px; text-decoration:none; font-weight:600; font-size:0.9rem; }
footer { margin-top:3rem; padding:1.5rem 0; border-top:1px solid var(--border); color:var(--muted); font-size:0.85rem; }
"""

pages = json.loads(PAGES_FILE.read_text())

for p in pages:
    rows = ""
    cards = ""
    for opt in p["options"]:
        rows += f"""
        <tr>
          <td><strong>{html.escape(opt['name'])}</strong></td>
          <td>{html.escape(opt['price_uk'])}</td>
          <td>{html.escape(opt['price_us'])}</td>
          <td>{html.escape(opt['best_for'])}</td>
          <td><a class="btn" href="{html.escape(opt['url'])}" rel="nofollow sponsored">Check Price</a></td>
        </tr>"""
        cards += f"""
        <div class="card">
          <h3>{html.escape(opt['name'])} — <span style="color:var(--good)">{html.escape(opt['price_uk'])} / {html.escape(opt['price_us'])}</span></h3>
          <p><strong>Billing model:</strong> {html.escape(opt['billing'])}</p>
          <p><strong>Best for:</strong> {html.escape(opt['best_for'])}</p>
          <p><strong>Why switch:</strong> {html.escape(opt['verdict'])}</p>
          <p><a class="btn" href="{html.escape(opt['url'])}" rel="nofollow sponsored">Visit {html.escape(opt['name'])} →</a></p>
        </div>"""

    page_html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{html.escape(p['title'])} | Switch &amp; Save</title>
  <meta name="description" content="{html.escape(p['summary'])}">
  <style>{STYLE}</style>
</head>
<body>
  <header>
    <div class="wrap">
      <a href="index.html">← Switch &amp; Save Directory (UK &amp; US)</a>
      <h1>{html.escape(p['title'])}</h1>
      <p style="margin:0;color:#cbd5e1;">Replacing: {html.escape(p['target_tool'])} · Last verified: {html.escape(p['updated'])}</p>
    </div>
  </header>
  <main class="wrap">
    <div class="card">
      <span class="badge">Buyer Question Answered</span>
      <p style="margin:0.5rem 0 0;font-weight:600;">"{html.escape(p['buyer_question'])}"</p>
      <p style="margin:0.5rem 0 0;color:var(--muted);">{html.escape(p['summary'])}</p>
    </div>
    <h2>Quick Price &amp; Feature Comparison (UK £ / US $)</h2>
    <table>
      <thead>
        <tr><th>Alternative</th><th>UK Price</th><th>US Price</th><th>Best For</th><th>Link</th></tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
    <h2>Detailed Breakdown</h2>
    {cards}
  </main>
  <footer>
    <div class="wrap">
      <p><strong>Disclosure:</strong> Some links on this page may become affiliate links (marked Ad/Sponsored), meaning we may earn a small commission at no extra cost to you. Prices verified {html.escape(p['updated'])}.</p>
    </div>
  </footer>
</body>
</html>"""
    (DIST / f"{p['slug']}.html").write_text(page_html)

index_items = ""
for p in pages:
    index_items += f"""
    <div class="card">
      <span class="badge">Replacing: {html.escape(p['target_tool'])}</span>
      <h2 style="margin:0.5rem 0;"><a href="{html.escape(p['slug'])}.html" style="color:var(--text);text-decoration:none;">{html.escape(p['title'])} →</a></h2>
      <p style="color:var(--muted);margin:0.25rem 0 0.75rem;">{html.escape(p['summary'])}</p>
      <a class="btn" href="{html.escape(p['slug'])}.html">Compare Alternatives</a>
    </div>"""

index_html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Switch &amp; Save — Practical Software &amp; Subscription Alternatives (UK &amp; US)</title>
  <meta name="description" content="Side-by-side UK &amp; US price comparisons for switching away from overpriced software and subscriptions.">
  <style>{STYLE}</style>
</head>
<body>
  <header>
    <div class="wrap">
      <h1>Switch &amp; Save (UK &amp; US)</h1>
      <p style="margin:0;color:#cbd5e1;">No-fluff side-by-side comparisons of cheaper, one-off, and open-source alternatives to overpriced subscriptions.</p>
    </div>
  </header>
  <main class="wrap">
    {index_items}
  </main>
  <footer>
    <div class="wrap">
      <p>Updated weekly · UK (£) and US ($) pricing side-by-side.</p>
    </div>
  </footer>
</body>
</html>"""
(DIST / "index.html").write_text(index_html)
print("Built", len(pages), "comparison pages + index.html in", DIST)

# Write .nojekyll and sitemap.xml
(DIST / ".nojekyll").write_text("", encoding="utf-8")
urls = ["https://davidallensomerset.github.io/Switch-and-Save/"] + [
    f"https://davidallensomerset.github.io/Switch-and-Save/{p['slug']}.html" for p in pages
]
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in urls:
    sitemap += f"  <url><loc>{u}</loc><lastmod>2026-10-23</lastmod></url>\n"
sitemap += "</urlset>\n"
(DIST / "sitemap.xml").write_text(sitemap, encoding="utf-8")
print("Added .nojekyll and sitemap.xml")
