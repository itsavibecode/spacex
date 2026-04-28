# SpaceX IPO Tracker

Live single-page tracker for the upcoming SpaceX IPO. Built so I (and anyone else watching) don't miss the date and aren't scrambling on pricing day.

**Live:** [spacex.bookhockeys.com](https://spacex.bookhockeys.com/)

## What it shows

- **Big date hero** — current best estimate for the listing window (June 18–30, 2026, midpoint June 22)
- **IPO price benchmark** — ~$525–$530/share at the targeted $1.75T–$2T valuation, alongside the current secondary-market mark from Hiive
- **Likely ticker** — $SPCX (freed up by Tuttle Capital in April 2026), with $SPCE as a secondary speculation
- **Live countdown** to the estimated pricing date, recomputed every second
- **Latest coverage** — pool of 15 recent articles, 5 picked at random on each load (with a Reshuffle button)
- **Timeline** — past milestones and upcoming events, rendered newest-first; "→ Next up" badge auto-flips to whichever future event is most imminent
- **Filings & primary sources** — direct links to SEC EDGAR searches, Form D CIKs, draft S-1 filter, and secondary-market data (Hiive, Forge, Yahoo)
- **Reminders that actually work** — pickable alarm offsets baked into a downloadable .ics file (native phone/desktop alarms), browser notifications while a tab/PWA is open, and a Google Calendar template link

## What it deliberately doesn't do

This site is static GitHub Pages — no backend, no database, no scheduler. It will never email or text you, because any form that took your email or phone would be a dead end. The honest delivery channels are:

1. The .ics download (native VALARM blocks, fires on your device)
2. Browser notifications (fires while the tab or installed PWA is alive)
3. Bookmarks to SEC EDGAR, Google Alerts, Kalshi, and @SpaceX on X for the moment official news drops

## Editing the data

Open [`index.html`](index.html) and look near the top of the `<script>` block. Everything that changes when news lands is in plain JS arrays/constants:

- `IPO_DATE` and `IPO_DATE_LABEL` — the countdown target
- `ARTICLE_POOL` — `{ title, source, date, url }` entries
- `TIMELINE` — `{ date, title, desc }` entries (chronological order; rendered newest-first)
- `FILINGS` — `{ type, title, meta, url }` entries

When SpaceX confirms a hard pricing date, ticker, or offer price, edit the constants and the hero copy in the HTML, bump the version badge, and add a changelog entry below.

## Changelog

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
