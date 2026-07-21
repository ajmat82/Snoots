# Tracking Template & Conversion Setup — Snoots Vet

---

## 1. Account-Level Tracking Template

Apply at the **account level** in Google Ads → Settings → Account settings → Tracking template.

```
{lpurl}?utm_source=google&utm_medium=cpc&utm_campaign={_campaign_name}&utm_content={adgroupid}&utm_term={keyword}&matchtype={matchtype}&device={device}&network={network}&placement={placement}&loc_interest_ms={loc_interest_ms}&loc_physical_ms={loc_physical_ms}
```

### Parameter breakdown

| Parameter | Populates with | Why it matters |
|---|---|---|
| `{lpurl}` | The ad's final URL | Required — do not remove |
| `utm_source=google` | Hardcoded | Source attribution |
| `utm_medium=cpc` | Hardcoded | Medium attribution |
| `utm_campaign={_campaign_name}` | Custom parameter (see below) | Human-readable campaign name in GA4 |
| `utm_content={adgroupid}` | Google auto-inserts ad group ID | Segment by ad group in GA4 |
| `utm_term={keyword}` | The matched keyword | Keyword-level attribution |
| `matchtype={matchtype}` | e, p, or b (exact/phrase/broad) | Diagnose match type performance |
| `device={device}` | m, t, or c (mobile/tablet/computer) | Device bid analysis |
| `network={network}` | g, s, or d (Google/Search Partners/Display) | Network performance breakdown |
| `placement={placement}` | Placement URL (Display/PMax) | Placement exclusion decisions |
| `loc_interest_ms={loc_interest_ms}` | Location of interest ID | Geo-targeting insight |
| `loc_physical_ms={loc_physical_ms}` | Physical location ID | Actual searcher location |

---

## 2. Custom Parameters for Campaign Names

Google's `{campaign}` ValueTrack parameter returns a numeric ID, not a name. Use custom parameters instead.

In each campaign's settings → Additional settings → Custom parameters, add:

| Campaign | Custom parameter key | Value |
|---|---|---|
| Brand — Snoots Vet | `_campaign_name` | `brand-snoots` |
| NB — Unlimited Vet Membership | `_campaign_name` | `nb-unlimited-vet` |
| NB — Pet Insurance Alternative | `_campaign_name` | `nb-pet-insurance-alt` |
| NB — Local NJ Vet | `_campaign_name` | `nb-local-nj` |
| NB — Pet-Specific | `_campaign_name` | `nb-pet-specific` |

This means GA4 will show `nb-unlimited-vet` as the campaign name — readable without a lookup table.

---

## 3. Final URL Suffix (Alternative / Supplement)

If the tracking template causes issues with any landing pages, add a Final URL suffix as a fallback:

```
utm_source=google&utm_medium=cpc&utm_campaign={_campaign_name}&utm_term={keyword}&device={device}
```

Apply at account level: Google Ads → Settings → Account settings → Final URL suffix.

---

## 4. UTM Naming Convention

Maintain consistency so GA4 reports are clean:

| Dimension | Format | Examples |
|---|---|---|
| utm_source | always `google` | `google` |
| utm_medium | always `cpc` | `cpc` |
| utm_campaign | `[brand/nb]-[theme]` | `brand-snoots`, `nb-unlimited-vet` |
| utm_content | Ad group ID (auto) | `1234567890` |
| utm_term | Keyword (auto) | `unlimited+vet+care` |

---

## 5. Conversion Actions to Configure

### Primary conversions (used by smart bidding)

| Conversion name | Type | Counting | Value |
|---|---|---|---|
| Membership signup | Website action (thank-you page or form submission) | One per click | $55 (monthly MRR) or LTV if known |
| Lead form submission | Website form / Lead form asset | One per click | — (use if no direct signup) |
| Phone call — 60s+ | Phone call from ad | One per click | — |

### Secondary conversions (observation only — do NOT include in smart bidding target)

| Conversion name | Type | Purpose |
|---|---|---|
| Session start | GA4 import | Funnel visibility only |
| Pricing page view | GA4 import | Engagement signal |
| Book appointment click | Click tracking | Intent signal |

> **Critical:** In Google Ads → Tools → Conversions, mark secondary conversions as "Secondary action" not "Primary action." Smart bidding will over-optimize for easy micro-conversions if these are set as primary.

---

## 6. Google Tag Setup (gtag.js)

Add to the `<head>` of every page on joinsnoots.com:

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'AW-XXXXXXXXXX');  // Replace with your Google Ads conversion ID
</script>
```

> Replace `AW-XXXXXXXXXX` with your actual Google Ads conversion ID from Tools → Conversions → [Conversion action] → Tag setup.

---

## 7. Conversion Tag — Membership Signup (Thank-You Page)

Fire on the post-signup confirmation page:

```html
<!-- Google Ads Conversion — Membership Signup -->
<script>
  gtag('event', 'conversion', {
    'send_to': 'AW-XXXXXXXXXX/YYYYYYYYYYYY',  // Conversion ID / Label
    'value': 55.00,
    'currency': 'USD',
    'transaction_id': ''  // Optional: pass a unique order/signup ID to prevent duplicate counting
  });
</script>
```

---

## 8. Enhanced Conversions

Enable Enhanced Conversions to send hashed first-party data (email, name, phone) alongside conversion events. This improves smart bidding signal quality, especially for users on browsers that block cookies.

Setup path: Google Ads → Tools → Conversions → Settings → Enhanced conversions

On the thank-you/confirmation page, push user data before the conversion tag fires:

```html
<script>
  gtag('set', 'user_data', {
    'email': '[hashed or raw — gtag handles hashing]',
    'phone_number': '',
    'address': {
      'first_name': '',
      'last_name': '',
      'country': 'US',
      'postal_code': ''
    }
  });
</script>
```

---

## 9. GA4 ↔ Google Ads Linking

1. Google Ads → Tools → Linked accounts → Google Analytics → Link GA4 property
2. In GA4: Admin → Google Ads Links → verify link is active
3. Import GA4 key events into Google Ads as secondary conversions (for funnel visibility only)
4. Enable **auto-tagging** in Google Ads (Settings → Account settings → Auto-tagging: Yes)

> Auto-tagging appends `gclid` to URLs. This is required for GA4 session attribution to work correctly alongside UTM parameters.

---

## 10. Attribution Model

Set in Google Ads → Tools → Conversions → Attribution:

| Setting | Recommendation |
|---|---|
| Attribution model | **Data-driven** (default for accounts with sufficient data) |
| Fallback | Linear (if data-driven not yet available due to low volume) |
| View-through window | 1 day |
| Click-through window | 30 days |

> Do not use Last click — it undervalues upper-funnel keywords (informational queries, awareness terms) and will cause smart bidding to abandon them prematurely.
