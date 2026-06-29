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

### v1.5.2 — 2026-06-29 ($25B senior notes follow-on)
- **SpaceX raised another $25B** in senior unsecured notes the week after the IPO. Combined with the IPO, that's **~$110.7B in equity + debt in three weeks**. Direct EDGAR check (bot still 403'd from CI) turned up three 8-Ks covering the notes deal:
  - **June 22 — Offering launched** (acc `0001628280-26-044489`). Disclosed ~$100.8B cash on the balance sheet as of June 19.
  - **June 23 — Priced 5 tranches** (acc `0001628280-26-044955`): $7B 5.350% due 2031, $6B 5.650% due 2033, $6B 5.875% due 2036, $2.5B 6.600% due 2046, $3.5B 6.650% due 2056.
  - **June 26 — Closing** (acc `0001628280-26-045763`). Indenture with BNY Mellon Trust; registration rights agreement with same IPO syndicate (BofA, Citi, Goldman, JPM, Morgan Stanley) as initial purchasers. 144A/Reg S placement; commit to register-for-exchange within 540 days.
- **Two consolidated TIMELINE events** added: "Launches $25B senior notes offering" (June 22) and "$25B senior notes closed (5 tranches)" (June 26, folding in the June 23 pricing).
- **Three new FILINGS entries** at the top of the list — one per 8-K so each filing is a clickable destination.
- **Footer disclaimer** updated to note the $25B notes follow-on and the ~$110.7B combined-raise figure.
- Hero / price block / countdown caption / OG image **unchanged** — the bond deal is corporate-finance news adjacent to the IPO, not a change to the IPO story itself.

### v1.5.1 — 2026-06-21 (delete the dead countdown)
- The countdown grid was hidden post-IPO but still in the DOM, plus its CSS, JS, and the `setInterval` that fired every second to do nothing. Removed entirely now that the site has permanently shifted to post-IPO mode.
- Specifically deleted: the four `.cd-cell` HTML elements, `.countdown` / `.cd-cell` / `.cd-num` / `.cd-lbl` CSS rules, `updateCountdown()` function, the `setInterval(updateCountdown, 1000)` call, the `updateCountdown()` boot call, and the now-unused `pad()` helper. The `<div class="live-banner">` no longer needs the `hidden` attribute — it's always visible.
- Kept: `IPO_DATE` constant (still used by the .ics download and Google Calendar template link as a historical-event timestamp), the `.ts` UTC clock in the top bar, and the static countdown caption beneath the banner (which now reads as the post-IPO summary).
- Net change: a leaner page with no dead DOM/CSS/JS that future-me has to scratch his head about.

### v1.5.0 — 2026-06-21 (post-IPO settled)
- **Minor version bump** because the site has shifted from "tracking a live IPO" to "tracking the aftermath" — a different phase.
- **Greenshoe fully exercised — the new headline.** Underwriters took the full 83.33M over-allotment on June 15; total offering 638.9M shares × $135 = **$85.7B raised**, the actual record (vs. the $75B baseline before greenshoe). Hero subtitle, price-block caveat, countdown caption, footer disclaimer, and OG image all updated.
- **First-week trading reality folded in**: day-one close $161 (+19%), hit a $225 intraday high before easing. Site doesn't quote live intraday — that link goes to Nasdaq for that.
- **Lockup schedule rewritten — was wrong.** What we had as a single Dec 9 cliff is actually a tiered/staggered unlock:
  - **Late July/Aug** — Q2 earnings + ~20% unlock (+10% extra if SPCX is >30% above $135 IPO into that date)
  - **~November** — Q3 earnings + 28% unlock (biggest single tranche)
  - **December 8** — 180-day full lockup expires (corrected from Dec 9)
  - **June 12, 2027** — Musk's ~6.4B shares unlock (366-day extended lockup, no early release)
- **Four new TIMELINE events** for the post-IPO filing flurry: greenshoe exercise + Series Preferred conversion (June 15), governance/bylaws amendment (June 16), additional governance + first Form 4 insider trade (June 17). The June 12 first-trade event picked up the S-8 employee stock plan registration.
- **Four new FILINGS entries**: three 8-Ks (June 15, 16, 17) + S-8 (June 12). Older entries preserved.
- **OG image regenerated** with the new subtitle: "Priced $135 · Greenshoe exercised · $85.7B raised · Trading on Nasdaq."

### v1.4.2 — 2026-06-12 (privacy scrub)
- **Removed every reference to the maintainer's GitHub handle from the publicly-served site surface.** Three real references existed: `<meta name="author">` in `index.html`, the JSON-LD WebSite `publisher.name` field, and an explicit `Repository:` line in `llms.txt`. All three removed.
- **`llms.txt` rewritten end-to-end** while I was in there — it was still v1.2-era stale (talked about $525–$530 estimate, June 18–30 window, "speculated $SPCX"). Now describes the live, post-IPO state cleanly: $135 fixed, $SPCX trading on Nasdaq, ~$1.77T post-money valuation, full filing trail.
- Generic "GitHub Pages" hosting mentions (describing deployment, not user identity) left in place.
- OG image PNG already had only `spacex.bookhockeys.com` in the footer — no regeneration needed.
- Verified clean: `grep -i "itsavibecode\|github.com"` returns zero hits across `index.html`, `llms.txt`, `robots.txt`, `sitemap.xml`, `CNAME`, `og-image.png`, `apple-touch-icon.png`, and `README.md`.

### v1.4.1 — 2026-06-12 (live banner replaces zero countdown)
- **Countdown replaced with a pulsing "$SPCX trading live on Nasdaq" banner** once the IPO date passes. Showing `00 00 00 00` reads as "broken countdown" rather than "the moment has arrived"; the live banner — green dot, pulsing animation, prominent "$SPCX trading live on Nasdaq" — communicates the actual state. New `.live-banner` element sits where the countdown grid used to be; JS toggles `hidden` on both elements based on `IPO_DATE - new Date()`.

### v1.4.0 — 2026-06-12 (first trade — IT'S LIVE)
- **$SPCX is trading on Nasdaq.** SpaceX priced June 11 at $135 fixed and began trading June 12 — the largest IPO in stock-market history. Opening trade indications walked from $175 → $160 → ~$150–$155 (~11–15% pop above the IPO price). Bell-ringing ceremonies at Nasdaq MarketSite and Starbase.
- **Major version bump (v1.4)** because this is the moment the tracker was built for. The site pivots from "tracking an upcoming IPO" to "tracking a live one."
- **Hero rewritten**:
  - Status pill: "Unconfirmed · target window" → **"Live · Trading on Nasdaq"**
  - Big date: "June 2026" → **"June 12, 2026"**
  - Subtitle: "$SPCX is trading on Nasdaq · Priced at $135 · Opening indications $150–$175 · Largest IPO in stock-market history"
- **Price block** now labeled "IPO Offer Price (final)" with a description that points readers to their broker or Nasdaq for live intraday price (this site doesn't quote intraday).
- **Countdown caption** flipped to "The IPO is live. $SPCX opened trading on Nasdaq today after pricing at $135 last night…"
- **Three new timeline events / event updates**:
  - **June 11** "Pricing day · $135 fixed" → **"Priced at $135 + SEC effective"** — adds the EFFECT notice (accession 9999999995-26-001968) and six Form 3 insider beneficial-ownership filings (accessions 0001628280-26-042631 through 042636)
  - **June 12** "First trade on Nasdaq" → **"First trade on Nasdaq — $SPCX is LIVE"** — adds the 424B4 final prospectus (accession 0001628280-26-042639), the bell-ringing ceremonies, and the opening-trade indication walk
- **Two new top-of-list FILINGS entries**:
  - **424B4** final prospectus (accession `0001628280-26-042639`) — confirms the $135 fixed pricing
  - **EFFECT** SEC notice of effectiveness (accession `9999999995-26-001968`)
- **OG image regenerated** for the new live state — "LIVE · TRADING ON NASDAQ" status pill + "Priced $135 · First trade June 12 · Opening $150-$175 indication" subtitle. Anyone sharing the link sees the right story.
- **Footer disclaimer** rewritten for past-tense IPO — adds the 424B4 confirmation and the $1.77T post-money valuation (slightly above the $1.75T target because of share-class math).

### v1.3.5 — 2026-06-11 (pricing day)
- **It's pricing day.** SpaceX prices today at $135 fixed, $1.75T post-money valuation. First trade tomorrow on Nasdaq as $SPCX — the biggest IPO in stock-market history. Direct EDGAR check turned up a flurry of pre-trade filings the bot's poller missed; hand-pulled and added below.
- **Hero subtitle** rewritten for "it's today" tense: "Pricing today at $135 fixed · First trade tomorrow on Nasdaq as $SPCX · 555.6M shares + 83.33M greenshoe."
- **Countdown caption** now reads "Pricing happens today after market close at the fixed $135 per share. $SPCX opens for trading tomorrow on Nasdaq — the biggest IPO in stock-market history."
- **Footer disclaimer** rewritten — adds greenshoe (83.33M shares = up to $86.2B fully exercised), reported $70B+ retail demand, June 10 Nasdaq listing approval, and removes pre-pricing tense throughout.
- **Three new TIMELINE events** between June 4 roadshow and June 11 pricing:
  - **June 8** — First FWP (Free Writing Prospectus) filed; second FWP June 9. Roadshow marketing materials live on EDGAR.
  - **June 10** — Nasdaq listing approved. Form 8-A12B filed + Nasdaq CERT issued = all pre-trade clearances in place.
  - **June 11 (today)** — Pricing day description expanded with the actual offering specifics (555.6M + 83.33M greenshoe @ $135; ~$75-86B raise; $70B+ retail demand; 1,500-attendee retail event).
- **Two new FILINGS entries** at the top of the list:
  - **8-A12B** (accession 0001628280-26-042107) with the paired Nasdaq CERT noted
  - **FWP** (accession 0001628280-26-041761) with the June 8 FWP noted (0001628280-26-041365)
- **Roadshow event description** updated with the ~125 analysts from 21 banks specifics now that the actual roadshow attendance is reported.

### v1.3.4 — 2026-06-03
- **OG image regenerated.** The 1200×630 share-preview PNG had been stale since v1.2.2 — still showing `~$525-$530`, `LIKELY TICKER`, `UNCONFIRMED · TARGET WINDOW`, and the original "Roadshow week of June 8 · Pricing window June 18-30" subtitle. Anyone who shared the link in iMessage / Discord / Slack / LinkedIn was seeing the old v1.2.x story. Now displays `$135.00`, `CONFIRMED TICKER · $SPCX`, `CONFIRMED · PRICING JUNE 11`, and the current subtitle. `.scripts/build-og-image.py` updated to match. Re-run after every hero/price change.
- **Share count + Fidelity retail access** folded into the disclaimer and the Broker prep section. ~555.6M shares at $135 = $75B raise (the math checks). Fidelity confirmed as SpaceX's named retail-access broker, so it's now elevated to the top of the broker list with a bold note about opting in before June 11. Schwab dropped down; the 5% employee carve-out from v1.3.3 added as a separate line for clarity.
- **June 4 timeline event** updated from generic "IPO roadshow begins" → "IPO roadshow + retail access opens" with the now-known specifics: dedicated SpaceX investor website + roadshow presentation + Fidelity retail opens.

### v1.3.3 — 2026-06-03
- **Fixed $135 IPO price disclosed today.** CNBC reports SpaceX is going to market with a fixed $135 per share — no traditional book-built range — at the targeted $1.75T valuation. This is unusual for an IPO of this size. The price block flipped from "Working estimate ~$105-$110" to **"IPO Offer Price (fixed) $135.00"** with a clear caveat about the atypical structure.
- **Two new S-1 amendments hand-added** (bot's EDGAR poller still blocked from GH Actions IPs):
  - **June 1 — S-1/A #1** (accession `0001628280-26-039276`) disclosed up to 5% of shares reserved for employees / friends-and-family
  - **June 3 — S-1/A #2** (accession `0001628280-26-040364`) reportedly contains the fixed-price offering terms
- **Timeline events** added for both amendments + the fixed-price disclosure. The June 11 event renamed from "Earliest pricing" → "Pricing" since the date is no longer a "as early as" estimate, and the June 12 event description tightened.
- **Hero subtitle** rewritten: "Roadshow starts June 4 · pricing June 11 at $135 fixed · first trade June 12 on Nasdaq as $SPCX."
- **Countdown caption, footer disclaimer, .ics summary, and Google Calendar event description** all updated to reflect the fixed $135 price and the actual amendment-derived dates.

### v1.3.2 — 2026-05-28
- **The public S-1 actually filed on May 20, 2026.** Accession `0001628280-26-036936` under CIK `1181412` (Space Exploration Technologies Corp.). Confirms $SPCX on Nasdaq; underwriters Morgan Stanley (left-lead), Goldman Sachs, BofA, Citi, JPMorgan; price range deliberately blank, to be set during the roadshow.
- **Timeline updated** to reflect what actually happened vs. what was predicted:
  - "Confidential S-1 filed" date corrected from April 1 → **March 30** per SEC records (April 1 was the press-report date)
  - **Added** May 7 "Confidential S-1 amendment (DRS/A) filed" (accession `0001628279-26-000583`)
  - "Public S-1 expected" → **"Public S-1 filed on EDGAR"** with full underwriter list in the description
- **FILINGS** gets three real entries replacing the placeholder "Confidential draft registration": the public S-1 (linking to the actual SEC archive at [sec.gov/Archives/.../spaceexplorationtechnologi.htm](https://www.sec.gov/Archives/edgar/data/1181412/000162828026036936/spaceexplorationtechnologi.htm)), the May 7 DRS/A, and the March 30 original DRS.
- **Ticker ribbon** language tightened from "Expected Ticker / working assumption" → "Confirmed Ticker / Officially confirmed in S-1."
- **Price block** caveat reworded — the S-1 cover left the price range blank, so the ~$105–$110 number is now framed as a working estimate pending the roadshow.
- **Footer disclaimer** rewritten to reflect the S-1 being public, the ticker being official, and the price range being TBD.
- **Bot's EDGAR poller rewritten.** It had been silently 403'ing from GitHub Actions IPs against the `efts.sec.gov/LATEST/search-index` endpoint, which is why the May 20 S-1 wasn't auto-detected. Now polls SpaceX's CIK directly via `https://data.sec.gov/submissions/CIK0001181412.json` (plus the four historical Form D filer CIKs), which is far more reliable. When the 424B prospectus drops at pricing, the bot should now actually catch it and append the "Final prospectus (424B) filed" timeline event automatically.

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
