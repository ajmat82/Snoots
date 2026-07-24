#!/usr/bin/env python3
"""
Split the combined Google Ads Editor CSV into separate entity-type files.
Each file follows Google Ads Editor's expected column format for that entity type.
Import each file via: Make multiple changes > Add/update multiple [type]
"""

import csv

SRC = "google-ads-editor-upload.csv"

with open(SRC, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

campaigns   = [r for r in rows if r["Type"] == "Campaign"]
ad_groups   = [r for r in rows if r["Type"] == "Ad group"]
keywords    = [r for r in rows if r["Type"] == "Keyword"]
rsa_ads     = [r for r in rows if r["Type"] == "Responsive search ad"]
neg_kws     = [r for r in rows if r["Type"] == "Campaign negative keyword"]

# ── 1. Campaigns ──────────────────────────────────────────────────────────────
with open("gae_campaigns.csv", "w", newline="", encoding="utf-8") as f:
    cols = ["Campaign", "Campaign Daily Budget", "Campaign Type",
            "Campaign Status", "Bid Strategy Type", "Networks", "Languages"]
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    for r in campaigns:
        w.writerow({
            "Campaign": r["Campaign"],
            "Campaign Daily Budget": r["Campaign Daily Budget"],
            "Campaign Type": r["Campaign Type"],
            "Campaign Status": "Paused",
            "Bid Strategy Type": r["Bid Strategy Type"],
            "Networks": r["Networks"],
            "Languages": r["Languages"],
        })
print(f"gae_campaigns.csv          → {len(campaigns)} rows")

# ── 2. Ad Groups ──────────────────────────────────────────────────────────────
with open("gae_ad_groups.csv", "w", newline="", encoding="utf-8") as f:
    cols = ["Campaign", "Ad Group", "Ad Group Status", "Ad Group Default Max CPC"]
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    for r in ad_groups:
        w.writerow({
            "Campaign": r["Campaign"],
            "Ad Group": r["Ad group"],
            "Ad Group Status": "Enabled",
            "Ad Group Default Max CPC": r["Max CPC"],
        })
print(f"gae_ad_groups.csv          → {len(ad_groups)} rows")

# ── 3. Keywords ───────────────────────────────────────────────────────────────
with open("gae_keywords.csv", "w", newline="", encoding="utf-8") as f:
    cols = ["Campaign", "Ad Group", "Keyword", "Match Type", "Keyword Status"]
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    for r in keywords:
        w.writerow({
            "Campaign": r["Campaign"],
            "Ad Group": r["Ad group"],
            "Keyword": r["Keyword"],
            "Match Type": r["Match type"],
            "Keyword Status": "Enabled",
        })
print(f"gae_keywords.csv           → {len(keywords)} rows")

# ── 4. Responsive Search Ads ──────────────────────────────────────────────────
hl_cols  = [f"Headline {i}" for i in range(1, 16)]
hl_pos   = [f"Headline {i} position" for i in range(1, 16)]
desc_cols = [f"Description {i}" for i in range(1, 5)]

with open("gae_rsa_ads.csv", "w", newline="", encoding="utf-8") as f:
    cols = (["Campaign", "Ad Group", "Ad Type", "Ad Status", "Final URL",
             "Path 1", "Path 2"]
            + hl_cols + hl_pos + desc_cols)
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    for r in rsa_ads:
        row = {
            "Campaign": r["Campaign"],
            "Ad Group": r["Ad group"],
            "Ad Type": "Responsive search ad",
            "Ad Status": "Enabled",
            "Final URL": r["Final URL"],
            "Path 1": r["Path 1"],
            "Path 2": r["Path 2"],
        }
        for c in hl_cols + hl_pos + desc_cols:
            row[c] = r.get(c, "")
        w.writerow(row)
print(f"gae_rsa_ads.csv            → {len(rsa_ads)} rows")

# ── 5. Campaign Negative Keywords ──────────────────────────────────────────────
with open("gae_negative_keywords.csv", "w", newline="", encoding="utf-8") as f:
    cols = ["Campaign", "Keyword", "Match Type"]
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
    w.writeheader()
    for r in neg_kws:
        w.writerow({
            "Campaign": r["Campaign"],
            "Keyword": r["Keyword"],
            "Match Type": r["Match type"],
        })
print(f"gae_negative_keywords.csv  → {len(neg_kws)} rows")

print("\nDone. Import order in Google Ads Editor:")
print("  1. Make multiple changes > Add/update multiple campaigns   → gae_campaigns.csv")
print("  2. Make multiple changes > Add/update multiple ad groups   → gae_ad_groups.csv")
print("  3. Make multiple changes > Add/update multiple keywords    → gae_keywords.csv")
print("  4. Make multiple changes > Add/update multiple ads         → gae_rsa_ads.csv")
print("  5. Make multiple changes > Add/update multiple [keywords]  → gae_negative_keywords.csv")
print("     (for negatives: use the negative keywords section)")
