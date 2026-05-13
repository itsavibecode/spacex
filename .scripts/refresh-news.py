"""
Daily refresh of the SpaceX IPO Tracker data arrays.

Driven by .github/workflows/refresh-news.yml on a daily cron (and via
"Run workflow" in the GitHub UI). Idempotent: only writes when the
content actually changes; the workflow only commits if `git diff` is
non-empty.

What it touches:
  * ARTICLE_POOL  — fully replaced from Google News RSS (no API key needed)
  * FILINGS       — bumps every "Updated" date to today; appends NEW
                     SpaceX-from filings detected on EDGAR (deduped by
                     accession number — bulletproof)
  * TIMELINE      — appends an event when a new public S-1 / 424B is
                     detected (deduped by accession). Hand-curated
                     historical events are preserved untouched.
  * price-range   — bumps the "Hiive MM/DD" date in the hero subtitle
  * sitemap.xml   — bumps <lastmod>

What it deliberately doesn't do:
  * Doesn't try to extract narrative timeline events from news prose
    (too high a hallucination risk for high-stakes facts).
  * Doesn't touch the hand-curated TIMELINE entries.

Run locally with:
    python .scripts/refresh-news.py
"""

import datetime as dt
import html as html_module
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

REPO = Path(__file__).resolve().parents[1]
INDEX = REPO / "index.html"
SITEMAP = REPO / "sitemap.xml"

# SEC requires a real UA; Google News doesn't care but we're polite either way.
UA = ("spacex-tracker-itsavibecode contact@bookhockeys.com "
      "(+https://github.com/itsavibecode/spacex)")


def fetch(url, accept="*/*", retries=2):
    """GET a URL with our UA. Retries once on transient errors (SEC will
    return 403 if our recent rate is too high; a single short sleep
    almost always clears it)."""
    last_err = None
    for attempt in range(retries + 1):
        try:
            req = Request(url, headers={"User-Agent": UA, "Accept": accept})
            with urlopen(req, timeout=30) as r:
                return r.read()
        except Exception as e:
            last_err = e
            if attempt < retries:
                import time
                time.sleep(3 + attempt * 4)  # 3s, 7s
    raise last_err


# === Google News RSS =========================================================
GNEWS_URL = "https://news.google.com/rss/search?q=%22SpaceX%22+IPO&hl=en-US&gl=US&ceid=US:en"

# Friendly source names so the UI doesn't show "Bloomberg.com" next to "Bloomberg".
SOURCE_NORMALIZE = {
    "Bloomberg.com": "Bloomberg",
    "The Wall Street Journal": "WSJ",
    "Wall Street Journal": "WSJ",
    "The Motley Fool": "Motley Fool",
    "Reuters": "Reuters",
    "Yahoo Finance": "Yahoo Finance",
    "Yahoo": "Yahoo Finance",
    "Seeking Alpha": "Seeking Alpha",
    "Bloomberg": "Bloomberg",
    "CNBC": "CNBC",
}


def parse_pubdate(s):
    """Parse RFC 2822 with or without timezone token."""
    for fmt in ("%a, %d %b %Y %H:%M:%S %Z", "%a, %d %b %Y %H:%M:%S %z"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    # Fallback: strip timezone and try without
    try:
        return dt.datetime.strptime(s[:25].strip(), "%a, %d %b %Y %H:%M:%S").date()
    except ValueError:
        return None


def google_news_articles():
    body = fetch(GNEWS_URL, accept="application/rss+xml")
    root = ET.fromstring(body)
    out = []
    for item in root.iter("item"):
        title_raw = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub = (item.findtext("pubDate") or "").strip()
        # Google News titles end with " - Source"
        m = re.match(r"^(.+?)\s+-\s+([^-]+)$", title_raw)
        if m:
            title, source = m.group(1).strip(), m.group(2).strip()
        else:
            title, source = title_raw, "Unknown"
        title = html_module.unescape(title)
        source = SOURCE_NORMALIZE.get(source, source)
        d = parse_pubdate(pub)
        if not d or not link or not title:
            continue
        out.append({
            "title": title,
            "source": source,
            "date": d.isoformat(),
            "url": link,
        })
    return out


def filter_articles(articles, days=60, cap=25):
    cutoff = (dt.date.today() - dt.timedelta(days=days)).isoformat()
    seen = set()
    out = []
    for a in sorted(articles, key=lambda x: x["date"], reverse=True):
        if a["date"] < cutoff:
            continue
        key = (a["title"].lower()[:80], a["source"].lower())
        if key in seen:
            continue
        seen.add(key)
        out.append(a)
        if len(out) >= cap:
            break
    return out


# === SEC EDGAR ===============================================================
EDGAR_SEARCH = "https://efts.sec.gov/LATEST/search-index"
# Only forms that would be material milestones for an IPO. Form D is
# private-placement noise; we keep the hand-curated CIK-specific Form D
# entries already in FILINGS, but the script won't add more.
EDGAR_FORMS = "S-1,S-1/A,F-1,F-1/A,DRS,DRS/A,424B1,424B2,424B3,424B4,8-A12B"


def edgar_filings():
    params = {
        "q": '"Space Exploration Technologies"',
        "dateRange": "custom",
        "startdt": "2026-01-01",
        "enddt": dt.date.today().isoformat(),
        "forms": EDGAR_FORMS,
    }
    url = f"{EDGAR_SEARCH}?{urlencode(params)}"
    body = fetch(url, accept="application/json")
    data = json.loads(body)
    hits = data.get("hits", {}).get("hits", [])
    out = []
    for h in hits:
        src = h.get("_source", {})
        # display_names like "SPACE EXPLORATION TECHNOLOGIES CORP."
        names = " ".join(src.get("display_names", []) or [])
        if "SPACE EXPLORATION TECHNOLOGIES" not in names.upper() \
                and "SPACEX" not in names.upper():
            continue  # Filing mentions SpaceX in the doc but isn't FROM SpaceX
        out.append({
            "form": src.get("form", ""),
            "date": src.get("file_date", ""),
            "ciks": src.get("ciks", []),
            "accession": src.get("adsh", ""),
            "filer": names,
        })
    return out


# === HTML / JS array surgery =================================================

def js_escape(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def render_articles_block(articles):
    """Render the contents BETWEEN the AUTO:ARTICLES:START/END markers.
    The closing `// AUTO:ARTICLES:END` line brings its own indent so we
    end with a bare newline, not a newline-plus-spaces."""
    lines = ["  const ARTICLE_POOL = ["]
    for a in articles:
        lines.append(
            f'    {{ title: "{js_escape(a["title"])}", '
            f'source: "{js_escape(a["source"])}", '
            f'date: "{a["date"]}", '
            f'url: "{js_escape(a["url"])}" }},'
        )
    if articles:
        lines[-1] = lines[-1].rstrip(",")
    lines.append("  ];")
    return "\n" + "\n".join(lines) + "\n"


# The marker pattern preserves the existing END line including its leading
# indent — we just swap out the body between START and END.


def replace_articles(text, articles):
    pattern = re.compile(
        r"(// AUTO:ARTICLES:START[^\n]*\n)(.*?)(\s*// AUTO:ARTICLES:END)",
        re.DOTALL,
    )
    body = render_articles_block(articles)
    # group(3) starts with the leading whitespace of the END line; we keep
    # only the marker text and prepend our own clean indent.
    end_marker = "  // AUTO:ARTICLES:END"
    return pattern.sub(lambda m: m.group(1) + body + end_marker, text, count=1)


def bump_updated_dates(text, today_iso):
    """Bump every entry whose dateKind is 'Updated' to today's date."""
    return re.sub(
        r'date: "\d{4}-\d{2}-\d{2}", dateKind: "Updated"',
        f'date: "{today_iso}", dateKind: "Updated"',
        text,
    )


def bump_hiive_subtitle(text, today_mmdd):
    return re.sub(
        r'Hiive \d{2}/\d{2}',
        f'Hiive {today_mmdd}',
        text,
    )


def insert_edgar_filings(text, edgar):
    """Append new SpaceX-from EDGAR filings to FILINGS (deduped by accession).

    Returns (new_text, num_inserted, inserted_summary). Inserts after the
    `const FILINGS = [` opening so newest sits at the top of the array.
    """
    if not edgar:
        return text, 0, []
    new_entries = []
    for f in edgar:
        if not f["accession"] or f["accession"] in text:
            continue  # already in the file
        cik = (f["ciks"][0] if f["ciks"] else "").lstrip("0") or "0"
        date_display = f["date"]
        # Friendly type label
        form = f["form"]
        type_label = "S-1" if form.startswith("S-1") else \
                     "F-1" if form.startswith("F-1") else \
                     "DRS" if form.startswith("DRS") else \
                     "PROSPECTUS" if form.startswith("424B") else form
        url = (f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany"
               f"&CIK={cik}&type={form}&dateb=&owner=include&count=40")
        entry = (
            f'    {{ type: "{type_label}", '
            f'title: "{js_escape(form)} filing", '
            f'meta: "{js_escape(f["filer"])} · accession {js_escape(f["accession"])}", '
            f'url: "{js_escape(url)}", '
            f'date: "{date_display}", dateKind: "Filed" }},'
        )
        new_entries.append((entry, f))
    if not new_entries:
        return text, 0, []
    insertion = "\n" + "\n".join(e for e, _ in new_entries)
    new_text = re.sub(
        r"(const FILINGS = \[)",
        lambda m: m.group(1) + insertion,
        text, count=1,
    )
    return new_text, len(new_entries), [f for _, f in new_entries]


def insert_edgar_timeline(text, edgar):
    """Append a TIMELINE event for the FIRST occurrence of each milestone form.

    "First public S-1" and "First 424B prospectus" are events worth a
    timeline pin. Deduped by event title — once "Public S-1 filed" exists
    in TIMELINE, we don't add another (even if S-1/A amendments arrive).
    """
    additions = []
    has_s1 = "Public S-1 filed" in text
    has_424b = "Final prospectus (424B) filed" in text
    for f in edgar:
        form = f["form"]
        if form == "S-1" and not has_s1:
            additions.append((f["date"], "Public S-1 filed",
                              f'SpaceX files its first public S-1 (accession {f["accession"]}) on EDGAR. '
                              f'Reveals revenue, margins, defense contracts, governance, and the official ticker.'))
            has_s1 = True
        elif form.startswith("424B") and not has_424b:
            additions.append((f["date"], "Final prospectus (424B) filed",
                              f'SpaceX files its final pricing prospectus ({form}, accession {f["accession"]}) — '
                              f'IPO date and offer price are now official.'))
            has_424b = True
    if not additions:
        return text, 0, []
    block_lines = []
    for date_iso, title, desc in additions:
        block_lines.append(
            f'    {{ date: "{date_iso}", title: "{js_escape(title)}",\n'
            f'      desc: "{js_escape(desc)}" }},'
        )
    insertion = "\n" + "\n".join(block_lines)
    new_text = re.sub(
        r"(const TIMELINE = \[)",
        lambda m: m.group(1) + insertion,
        text, count=1,
    )
    return new_text, len(additions), additions


def update_sitemap(today_iso):
    s = SITEMAP.read_text(encoding="utf-8")
    s2 = re.sub(r"<lastmod>[^<]*</lastmod>",
                f"<lastmod>{today_iso}</lastmod>", s, count=1)
    if s2 != s:
        SITEMAP.write_text(s2, encoding="utf-8")
        return True
    return False


# === main ===================================================================

def main():
    print(f"[refresh-news] starting {dt.datetime.now(dt.timezone.utc).isoformat()}")
    today = dt.date.today()
    today_iso = today.isoformat()
    today_mmdd = today.strftime("%m/%d")

    text = INDEX.read_text(encoding="utf-8")
    orig = text

    # Step 1: articles
    try:
        articles_raw = google_news_articles()
        articles = filter_articles(articles_raw)
        print(f"  Google News: {len(articles_raw)} items -> {len(articles)} kept after dedupe + 60-day cutoff")
        if articles:
            text = replace_articles(text, articles)
        else:
            print("  No fresh articles — leaving ARTICLE_POOL as-is")
    except Exception as e:
        print(f"  WARNING: Google News fetch failed: {e}", file=sys.stderr)

    # Step 2: bump 'Updated' dates and Hiive date
    text = bump_updated_dates(text, today_iso)
    text = bump_hiive_subtitle(text, today_mmdd)

    # Step 3: EDGAR-driven inserts
    edgar = []
    try:
        edgar = edgar_filings()
        print(f"  EDGAR: {len(edgar)} SpaceX-from filings since 2026-01-01")
        for f in edgar:
            print(f"    {f['date']}  {f['form']:10s}  acc={f['accession']}  filer={f['filer'][:60]}")
    except Exception as e:
        print(f"  WARNING: EDGAR fetch failed (continuing): {e}", file=sys.stderr)

    text, n_filings, _ = insert_edgar_filings(text, edgar)
    if n_filings:
        print(f"  Appended {n_filings} new FILINGS entry/ies from EDGAR")
    text, n_tl, additions = insert_edgar_timeline(text, edgar)
    if n_tl:
        print(f"  Appended {n_tl} new TIMELINE event(s):")
        for d, t, _ in additions:
            print(f"    {d}  {t}")

    # Step 4: write only if changed
    sitemap_changed = update_sitemap(today_iso)
    if text != orig:
        INDEX.write_text(text, encoding="utf-8")
        print("  Wrote index.html")
    else:
        print("  index.html unchanged")
    if sitemap_changed:
        print("  Wrote sitemap.xml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
