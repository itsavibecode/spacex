# SpaceX IPO Tracker

Live single-page tracker for the upcoming SpaceX IPO. Built so I (and anyone else watching) don't miss the date and aren't scrambling on pricing day.

**Live:** [spacex.bookhockeys.com](https://spacex.bookhockeys.com/)

## What it shows

- **Big date hero** — current best estimate for the listing window (June 18–30, 2026); countdown targets **June 18** (the earliest of the window) so you're prepared on the front edge instead of caught off-guard
- **IPO price benchmark** — ~$525–$530/share at the targeted $1.75T–$2T valuation, alongside the current secondary-market mark from Hiive
- **Likely ticker** — $SPCX (freed up by Tuttle Capital in April 2026), with $SPCE as a secondary speculation
- **Live countdown** to the estimated pricing date, recomputed every second
- **Latest coverage** — 5 most recent of the 25 newest articles from Google News, refreshed daily by a GitHub Action; sorted by publish date
- **Timeline** — past milestones and upcoming events, rendered newest-first; "→ Next up" badge auto-flips to whichever future event is most imminent
- **Filings & primary sources** — direct links to SEC EDGAR searches, Form D CIKs, draft S-1 filter, and secondary-market data (Hiive, Forge, Yahoo)
- **Reminders that actually work** — pickable alarm offsets baked into a downloadable .ics file (native phone/desktop alarms), browser notifications while a tab/PWA is open, and a Google Calendar template link
- **PNG snapshots** — hover any article or timeline event, click the camera in the corner, and a PNG of just that card downloads

## What it deliberately doesn't do

This site is static GitHub Pages — no backend, no database, no scheduler. It will never email or text you, because any form that took your email or phone would be a dead end. The honest delivery channels are:

1. The .ics download (native VALARM blocks, fires on your device)
2. Browser notifications (fires while the tab or installed PWA is alive)
3. Bookmarks to SEC EDGAR, Google Alerts, Kalshi, and @SpaceX on X for the moment official news drops

## Editing the data

Open [`index.html`](index.html) and look near the top of the `<script>` block. Everything that changes when news lands is in plain JS arrays/constants:

- `IPO_DATE` and `IPO_DATE_LABEL` — the countdown target (manual)
- `ARTICLE_POOL` — `{ title, source, date, url }` entries. **Auto-refreshed daily by [.github/workflows/refresh-news.yml](.github/workflows/refresh-news.yml)** between the `// AUTO:ARTICLES:START` / `:END` markers — hand edits inside will be overwritten on the next cron run.
- `TIMELINE` — `{ date, title, desc }` entries (chronological in source, rendered newest-first). Hand-curated; the workflow only *appends* events when a new public S-1 or 424B is detected on EDGAR.
- `FILINGS` — `{ type, title, meta, url, date, dateKind }` entries. The workflow bumps `Updated` dates daily and appends EDGAR-detected SpaceX filings (deduped by accession number). Hand-curated entries are preserved.

When SpaceX confirms a hard pricing date, ticker, or offer price, edit the constants and the hero copy in the HTML, bump the version badge, and add a changelog entry below.

## Auto-refresh workflow

A GitHub Action ([`.github/workflows/refresh-news.yml`](.github/workflows/refresh-news.yml)) runs daily at 14:00 UTC and on demand from the **Actions** tab. It calls [`.scripts/refresh-news.py`](.scripts/refresh-news.py), which:

1. Pulls SpaceX IPO articles from the Google News RSS feed (no API key)
2. Bumps every "Updated" date in `FILINGS` and the Hiive subtitle date to today
3. Queries SEC EDGAR for SpaceX-from filings and appends new ones
4. Updates `<lastmod>` in `sitemap.xml`

The workflow only commits when content actually changed. Bot commits are authored as `github-actions[bot]` so they're visually distinct from human commits in the log.

To run it manually: GitHub → **Actions** tab → **Refresh news + filings** → **Run workflow**.

## Changelog

### v1.3.1 — 2026-05-19
- **Major news refresh** for the manual-only fields the auto-refresh deliberately doesn't touch. Reuters reported May 15 that the IPO timeline has been substantially accelerated and shareholders approved a 5-for-1 forward stock split.
- **Countdown pivoted from June 18 → June 11** (earliest of the new June 11–12 pricing window). Footer disclaimer and countdown caption updated to match.
- **Hero subtitle** now reads "Roadshow June 4 · pricing as early as June 11 · first trade as early as June 12 · Nasdaq."
- **Price benchmark switched to post-split** (~$105–$110), with a clear note explaining the 5-for-1 split so anyone who saw the pre-split $525–$530 understands the math. Pre-split number and the $1.75T valuation still shown for context.
- **Ticker ribbon** tightened: $SPCX on Nasdaq is now Reuters' and Bloomberg's working assumption rather than pure speculation; final confirmation still gated on the public S-1. Dropped the $SPCE alternative mention.
- **Timeline events** (newest at top):
  - **Added** May 15 "5-for-1 forward stock split approved"
  - **Added** May 17 "BlackRock anchor talks reported ($5–10B)"
  - **Updated** May 15 "Public S-1 expected" → May 20 (Reuters' target date)
  - **Updated** June 8 "IPO roadshow begins" → June 4
  - **Replaced** June 18 "Earliest pricing & first trade" with two events: June 11 "Earliest pricing" + June 12 "First trade on Nasdaq"
  - **Removed** June 11 "Retail investor day" (conflicted with the new June 11 pricing date; will re-add if a separate retail event is reconfirmed for the compressed timeline)
  - **Updated** Dec 15 "Insider lockup expires" → Dec 9 (180 days from a June 12 first trade)
- **.ics and Google Calendar event descriptions** rewritten to match the new timeline, price, and ticker.

### v1.3.0 — 2026-05-13
- **Daily auto-refresh via GitHub Actions.** A new `.github/workflows/refresh-news.yml` runs at 14:00 UTC every day (and on demand from the Actions tab) and pushes a commit only when content actually changed. The accompanying `.scripts/refresh-news.py`:
  - Fully replaces `ARTICLE_POOL` from the [Google News RSS feed](https://news.google.com/rss/search?q=%22SpaceX%22+IPO) (no API key needed; aggregates Bloomberg, CNBC, Reuters, WSJ, Motley Fool, Yahoo, etc.) — keeps the 25 newest, dedupes by title+source, drops anything older than 60 days.
  - Bumps every `dateKind: "Updated"` entry in `FILINGS` to today's date, and the "Hiive MM/DD" date in the price subtitle.
  - Polls the SEC EDGAR full-text search API for SpaceX-from filings (`S-1`, `S-1/A`, `F-1`, `DRS`, `424B1-4`, `8-A12B`) and appends new entries to `FILINGS` (deduped by accession number — bulletproof) plus a `TIMELINE` event the first time an `S-1` or `424B` is detected.
  - Updates `<lastmod>` in `sitemap.xml`.
  - Idempotent: workflow only commits when `git diff` is non-empty.
- **Camera button on every article and timeline event.** Hover (or focus) a card and a small camera icon fades in at top-right — click it to download a PNG snapshot of just that card. Powered by [html2canvas](https://html2canvas.hertzen.com/) lazy-loaded on first use (zero cold-load cost). Filenames are descriptive like `spacex-ipo-article-motley-fool-2026-05-13.png` and `spacex-ipo-timeline-2026-06-18-earliest-pricing-first-trade.png`. Camera button hides itself during capture so it doesn't appear in the screenshot. Click stops propagation so the article link doesn't open.
- **Array markers.** `ARTICLE_POOL`, `TIMELINE`, and `FILINGS` are now wrapped in `// AUTO:*:START/END` comments so the refresh script has clean replacement boundaries and human edits stay readable.

### v1.2.3 — 2026-05-08
- **Lighthouse mobile: 90/90/100/100 → 100/100/100/100.** All four categories now max out. FCP and LCP both dropped from 2.9s → 1.1s; Speed Index 3.1s → 1.1s; TTI 2.9s → 1.2s; CLS stayed comfortably under 0.05.
- **Killed the only render-blocking resource** by switching the Google Fonts `<link>` from a synchronous stylesheet to the `rel="preload" as="style" onload="this.rel='stylesheet'"` async pattern with a `<noscript>` fallback. The fonts now load in parallel with the document instead of blocking ~1.9s of first paint.
- **Fixed all WCAG AA color-contrast failures** (`#now-ts`, `.price-range`, `#countdown-caption`, every article date). Bumped `--ink-faint` from `#6b7385` (4.08:1 on `--bg`, 3.73:1 on `--panel`) to `#8b93a7` which clears 5.8:1 on both surfaces.
- **Fixed heading order** by promoting the four section titles from `<div class="sec-title">` to `<h2 class="sec-title">`. The h1 → h2 → h3 hierarchy is now sequential; screen readers and SEO crawlers no longer trip over an out-of-order h3 in the reminders section.
- **Added `<meta name="color-scheme" content="dark">`** so the browser paints a dark background before CSS parses, eliminating the flash of light on cold loads.
- **Added `.scripts/compare-lh.py`** helper for printing before/after Lighthouse diffs and `.gitignore` for the regenerable `.lh-*.json` reports.

### v1.2.2 — 2026-04-28
- **Real share previews.** Generated a 1200×630 `og-image.png` (the size every link unfurler expects) and a 180×180 `apple-touch-icon.png`. Added the missing pieces of the Open Graph / Twitter Card spec: `og:image` (+ width / height / type / alt / secure_url), `og:locale`, `twitter:image`, `twitter:image:alt`, and flipped `twitter:card` from `summary` to `summary_large_image` so the Twitter/X preview uses the hero card instead of a tiny thumbnail. Added the `apple-touch-icon` link so iOS home-screen and iMessage rich previews show the rocket icon.
- **OG image build script** lives at `.scripts/build-og-image.py` — uses Pillow + Windows-bundled fonts (Arial Black, Inter, Consolas Bold). Re-run it whenever the hero numbers change.
- **Verify share previews** with [opengraph.xyz](https://www.opengraph.xyz/url/https%3A%2F%2Fspacex.bookhockeys.com%2F), [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/?q=https%3A%2F%2Fspacex.bookhockeys.com%2F), [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/inspect/https%3A%2F%2Fspacex.bookhockeys.com%2F), and (signed in) the [X Cards Validator](https://cards-dev.twitter.com/validator). LinkedIn and X cache aggressively — re-fetch from those tools after each image change.

### v1.2.1 — 2026-04-28
- **Latest coverage now sorted by publish date** instead of randomly shuffled — the 5 newest articles always rise to the top. Removed the Reshuffle button (it was randomizing what should have been a recency feed) and the on-load shuffle helper.
- **Every filing now shows a date.** Form D entries display the actual SEC filing date pulled from EDGAR (CIK 2047425 → 2024-12-05, 1992247 → 2023-09-07, 1819923 → 2020-10-07, 1826165 → 2020-09-28); the confidential draft S-1 shows 2026-04-01; live search/secondary-market links show the most recent "Updated" timestamp. Filings reordered newest-first.
- **Countdown pivoted from the June 22 midpoint to the June 18 earliest.** Better to be ready early than caught late if SpaceX prices on the front edge of the window. Timeline event renamed to "Earliest pricing & first trade"; insider lockup expiry pushed from Dec 22 → Dec 15 (still 180 days out from the new first-trade date); .ics summary, Google Calendar event title, and footer disclaimer all reworded to match.
- **Filing card layout** gets a small `filing-head` flex row so the type badge and date sit side-by-side without breaking the existing grid.

### v1.2.0 — 2026-04-27
- **Refreshed all data** for the post-confidential-S-1 news cycle: IPO window narrowed to June 18–30, pricing benchmark updated to ~$525–$530 (the actual IPO target), Hiive secondary mark separated out, ticker note expanded to mention $SPCE alongside $SPCX, and 9 newer articles added to the rotation pool (Motley Fool, TechStackIPO, ARK, Augustus Wealth, The Next Web, etc.)
- **Added** Apr 21 closed-door analyst meetings to the timeline; expanded May 15 Public S-1 entry into a May 15–22 window; updated estimated first trade from Jun 16 → Jun 22; added Dec 22 insider lockup expiry as a downside catalyst marker
- **Reversed timeline render order** so the most recent / most imminent events are at the top — easier to scan when checking back in
- **Reworked the reminders section** — removed the email and phone fields entirely (they were a placebo since this is a static site with no backend), reframed the section around the delivery mechanisms that actually work, and added a "How you'll actually hear about official news" panel pointing at SEC EDGAR, Google Alerts, Kalshi, and @SpaceX
- **Added 30-min-before-pricing alarm** option for both .ics and browser notifications
- **Wired alarm checkboxes** to auto-persist their state to localStorage on change (no more "Save preferences" button)
- **Added SEO + share metadata** — `<meta description>`, Open Graph tags, Twitter card, canonical URL, and a JSON-LD WebSite schema block; created [`robots.txt`](robots.txt), [`sitemap.xml`](sitemap.xml), and [`llms.txt`](llms.txt)
- **Fixed stale price text** in the .ics and Google Calendar event descriptions (was still saying "~$600–700"; now matches the $525–530 benchmark)
- **Updated** the bottom disclaimer to reflect the latest filing status and date estimate

### v1.1.0 — 2026-04-19
- Inline SVG favicon (rocket silhouette, data URI — no external file needed)
- Version badge in the footer
- Predicted ticker ribbon ($SPCX based on Tuttle Capital ETF swap)
- New Timeline section with auto-detecting done / next / future status

### v1.0.0 — 2026-04-18
- Initial single-file build: hero date, price block, countdown, articles pool, filings grid, reminder section
- Clean typography pass: dropped italic serif and excessive monospace; switched to Inter throughout with monospace only on countdown digits and timestamps

## Stack

- One static `index.html`, no build step, no dependencies beyond Google Fonts (Inter + JetBrains Mono)
- Hosted on GitHub Pages at the apex CNAME `spacex.bookhockeys.com`

## Disclaimer

Not investment advice. All figures are publicly reported estimates from secondary markets (Hiive, Forge) and the financial press. SpaceX has not officially confirmed an IPO date, offer price, or ticker symbol as of this README.
