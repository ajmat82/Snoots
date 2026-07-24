#!/usr/bin/env python3
"""
Rebuild all Google Ads bulk upload CSVs using the exact template format
downloaded from the Google Ads UI (Tools > Bulk actions > Uploads > Templates).
"""

import csv

SRC = "google-ads-editor-upload.csv"

with open(SRC, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

campaigns = [r for r in rows if r["Type"] == "Campaign"]
ad_groups = [r for r in rows if r["Type"] == "Ad group"]
keywords   = [r for r in rows if r["Type"] == "Keyword"]
rsa_ads    = [r for r in rows if r["Type"] == "Responsive search ad"]
neg_kws    = [r for r in rows if r["Type"] == "Campaign negative keyword"]

MATCH_TYPE_MAP = {
    "Exact":  "Exact match",
    "Phrase": "Phrase match",
    "Broad":  "Broad match",
}

# ── 1. Campaigns ──────────────────────────────────────────────────────────────
# No official template provided; keep the format that got past the Budget error.
# Added: Row Type, Action columns to match the pattern of other templates.
with open("gae_campaigns.csv", "w", newline="", encoding="utf-8") as f:
    cols = ["Row Type", "Action", "Campaign", "Budget", "Campaign type",
            "Campaign status", "Bid strategy type", "Networks", "Languages",
            "EU political ads"]
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for r in campaigns:
        w.writerow({
            "Row Type": "Campaign",
            "Action": "Add",
            "Campaign": r["Campaign"],
            "Budget": r["Campaign Daily Budget"],
            "Campaign type": "Search",
            "Campaign status": "Paused",
            "Bid strategy type": "Maximize conversions",
            "Networks": "Google Search",
            "Languages": "English",
            "EU political ads": "No",
        })
print(f"gae_campaigns.csv          → {len(campaigns)} rows")

# ── 2. Ad Groups ──────────────────────────────────────────────────────────────
# Template cols: Row Type, Action, Ad group status, Campaign ID, Campaign,
#                Ad group ID, Ad group, Ad group type, Ad rotation,
#                Default max. CPC, ...
with open("gae_ad_groups.csv", "w", newline="", encoding="utf-8") as f:
    cols = ["Row Type", "Action", "Ad group status", "Campaign", "Ad group",
            "Default max. CPC"]
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for r in ad_groups:
        w.writerow({
            "Row Type": "Ad group",
            "Action": "Add",
            "Ad group status": "Enabled",
            "Campaign": r["Campaign"],
            "Ad group": r["Ad group"],
            "Default max. CPC": r["Max CPC"],
        })
print(f"gae_ad_groups.csv          → {len(ad_groups)} rows")

# ── 3. Keywords ───────────────────────────────────────────────────────────────
# Template cols: Row Type, Action, Keyword status, Campaign ID, Campaign,
#                Ad group ID, Ad group, Keyword ID, Keyword, Type, ...
with open("gae_keywords.csv", "w", newline="", encoding="utf-8") as f:
    cols = ["Row Type", "Action", "Keyword status", "Campaign", "Ad group",
            "Keyword", "Type"]
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for r in keywords:
        w.writerow({
            "Row Type": "Keyword",
            "Action": "Add",
            "Keyword status": "Enabled",
            "Campaign": r["Campaign"],
            "Ad group": r["Ad group"],
            "Keyword": r["Keyword"],
            "Type": MATCH_TYPE_MAP.get(r["Match type"], r["Match type"]),
        })
print(f"gae_keywords.csv           → {len(keywords)} rows")

# ── 4. Responsive Search Ads ──────────────────────────────────────────────────
# Template cols: Row Type, Action, Ad status, Campaign ID, Campaign,
#                Ad group ID, Ad group, Ad ID, Ad type, Label,
#                Headline 1-15, Description 1-4,
#                Headline 1-15 position, Description 1-4 position,
#                Path 1, Path 2, Final URL, ...
hl_cols   = [f"Headline {i}" for i in range(1, 16)]
hl_pos    = [f"Headline {i} position" for i in range(1, 16)]
desc_cols = [f"Description {i}" for i in range(1, 5)]
desc_pos  = [f"Description {i} position" for i in range(1, 5)]

with open("gae_rsa_ads.csv", "w", newline="", encoding="utf-8") as f:
    cols = (["Row Type", "Action", "Ad status", "Campaign", "Ad group",
             "Ad type"]
            + hl_cols + desc_cols + hl_pos + desc_pos
            + ["Path 1", "Path 2", "Final URL"])
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for r in rsa_ads:
        row = {
            "Row Type": "Ad",
            "Action": "Add",
            "Ad status": "Enabled",
            "Campaign": r["Campaign"],
            "Ad group": r["Ad group"],
            "Ad type": "Responsive search ad",
            "Path 1": r.get("Path 1", ""),
            "Path 2": r.get("Path 2", ""),
            "Final URL": r["Final URL"],
        }
        for c in hl_cols + desc_cols + hl_pos + desc_pos:
            row[c] = r.get(c, "")
        w.writerow(row)
print(f"gae_rsa_ads.csv            → {len(rsa_ads)} rows")

# ── 5. Campaign Negative Keywords ─────────────────────────────────────────────
# Template cols: Row Type, Action, Keyword status, Level, Campaign ID,
#                Campaign, Ad group ID, Ad group, Keyword ID,
#                Negative keyword, Type
with open("gae_negative_keywords.csv", "w", newline="", encoding="utf-8") as f:
    cols = ["Row Type", "Action", "Keyword status", "Level", "Campaign",
            "Negative keyword", "Type"]
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for r in neg_kws:
        w.writerow({
            "Row Type": "Negative keyword",
            "Action": "Add",
            "Keyword status": "Enabled",
            "Level": "Campaign",
            "Campaign": r["Campaign"],
            "Negative keyword": r["Keyword"],
            "Type": MATCH_TYPE_MAP.get(r["Match type"], r["Match type"]),
        })
print(f"gae_negative_keywords.csv  → {len(neg_kws)} rows")

print("\nAll files rebuilt using official Google Ads template format.")
print("Import order: campaigns → ad groups → keywords → RSA ads → negative keywords")
