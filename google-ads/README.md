# Snoots Vet — Google Ads Setup

Full account build for joinsnoots.com targeting New Jersey pet owners.

## Campaign Architecture

```
Google Ads Account
├── Brand — Snoots Vet                    ($20–30/day)
│   └── Ad Group: Snoots Brand
│       └── RSA: Official site ad
│
├── NB — Unlimited Vet Membership         ($60/day)
│   ├── Ad Group: Unlimited Vet Care
│   └── Ad Group: Affordable Vet Plan
│
├── NB — Pet Insurance Alternative        ($40/day)
│   └── Ad Group: Pet Insurance Alternative
│
├── NB — Local NJ Vet                     ($50/day)
│   ├── Ad Group: Vet Near Me NJ
│   └── Ad Group: Vet Clifton NJ
│
└── NB — Pet-Specific                     ($30/day)
    ├── Ad Group: Dog Vet Membership
    └── Ad Group: Cat Vet Membership
```

**Total launch budget:** ~$200/day ($6,000/month)

## Files

| File | Contents |
|---|---|
| `brand/brand-campaign.md` | Brand campaign settings, keywords, RSA, negatives |
| `non-brand/non-brand-campaigns.md` | All non-brand campaigns, ad groups, RSAs, keywords |
| `assets/assets.md` | Sitelinks, callouts, structured snippets, call, location, promotion, image assets |
| `tracking-template.md` | Tracking template, UTM convention, conversion setup, Enhanced Conversions, GA4 linking |

## Launch Checklist

- [ ] Google Ads account created and billing configured
- [ ] Google Business Profile linked (location asset)
- [ ] Phone number confirmed for call asset
- [ ] gtag installed on all pages of joinsnoots.com
- [ ] Membership signup conversion tag firing on thank-you page
- [ ] Enhanced Conversions configured
- [ ] GA4 property linked to Google Ads
- [ ] All 5 campaigns created with correct settings
- [ ] Tracking template applied at account level
- [ ] Custom parameters set per campaign (for utm_campaign names)
- [ ] Brand negatives applied to all non-brand campaigns
- [ ] Non-brand negative keyword list applied to all NB campaigns
- [ ] Founding member promotion asset end date confirmed and calendared
- [ ] Initial bids: Maximize Conversions (no tCPA target for first 4 weeks)
- [ ] Schedule 4-week review: switch to tCPA on campaigns with 30+ conversions

## Bidding Progression

| Phase | Timeline | Strategy |
|---|---|---|
| Launch | Weeks 1–4 | Maximize Conversions (no CPA target) |
| Learning complete | Weeks 5–8 | Add tCPA target ~20–30% above actual CPA |
| Optimized | Month 3+ | Tighten tCPA as efficiency improves |

## Key Metrics to Track Weekly

- Impression share (brand should be >90%)
- CTR by campaign (brand typically 10–20%, NB 3–8%)
- CPC by campaign
- Conversion rate (signup / lead form)
- Cost per lead / cost per member acquisition
- Search terms report — add new negatives weekly for first 8 weeks
