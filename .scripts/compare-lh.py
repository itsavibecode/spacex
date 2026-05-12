"""One-off: compare before/after Lighthouse reports for the perf pass."""
import json, sys
sys.stdout.reconfigure(encoding="utf-8")

b = json.load(open(r"T:/ClaudeCodeRepo/spacex/.lh-mobile.json", encoding="utf-8"))
a = json.load(open(r"T:/ClaudeCodeRepo/spacex/.lh-mobile-after.json", encoding="utf-8"))

def s(d, k):
    sc = d.get("categories", {}).get(k, {}).get("score")
    return int(sc * 100) if sc is not None else None

print("=== MOBILE: BEFORE (live) vs AFTER (local v1.2.3) ===")
print(f'{"category":20s}  before -> after')
for cat in ("performance", "accessibility", "best-practices", "seo"):
    print(f"  {cat:20s}  {s(b,cat):>3} -> {s(a,cat):>3}")

print()
print("Core metrics:")
for m in ("first-contentful-paint", "largest-contentful-paint",
         "total-blocking-time", "cumulative-layout-shift",
         "speed-index", "interactive"):
    bv = b["audits"].get(m, {}).get("displayValue", "--")
    av = a["audits"].get(m, {}).get("displayValue", "--")
    bs = b["audits"].get(m, {}).get("score")
    asc = a["audits"].get(m, {}).get("score")
    print(f"  {m:35s} {bv:>14} -> {av:>14}  (score {bs} -> {asc})")

print()
print("=== Audits that were failing before — verify fixed ===")
for k in ("color-contrast", "heading-order", "render-blocking-resources",
          "render-blocking-insight", "largest-contentful-paint-element",
          "network-dependency-tree-insight"):
    bsc = b["audits"].get(k, {}).get("score")
    asc = a["audits"].get(k, {}).get("score")
    bdv = b["audits"].get(k, {}).get("displayValue", "")
    adv = a["audits"].get(k, {}).get("displayValue", "")
    print(f"  {k:40s}  before={bsc} {bdv}  | after={asc} {adv}")
