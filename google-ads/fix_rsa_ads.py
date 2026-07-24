#!/usr/bin/env python3
"""
Rebuild gae_rsa_ads.csv with corrected headlines (≤30 chars, no em/en dash or ★)
and rewritten descriptions (≤90 chars each). Path values ≤15 chars.
"""

import csv

# Mapping: original headline → corrected headline (max 30 chars, no —/–/★)
HL_FIXES = {
    # em/en dash only (replace with hyphen)
    "Snoots Vet — Official Site":           "Snoots Vet - Official Site",
    "Clifton, NJ — Book Today":             "Clifton, NJ - Book Today",
    "Vet Membership — No Copays":           "Vet Membership - No Copays",
    "All Vet Care — One Monthly Fee":       "All Vet Care - One Monthly Fee",
    "Flat-Fee Vet — No Copays":             "Flat-Fee Vet - No Copays",
    "Join Snoots Vet — Book Today":         "Join Snoots Vet - Book Today",
    "Concierge Vet Membership — NJ":        "Concierge Vet Membership - NJ",
    "Pet Health Plan — from $55/Mo":        "Pet Health Plan from $55/Mo",
    "Dogs & Cats — No Exclusions":          "Dogs & Cats - No Exclusions",
    "Monthly or Annual — You Choose":       "Monthly or Annual - You Choose",
    "Lemonade Alternative — NJ":            "Lemonade Alternative - NJ",
    "Covered From Day One — No Wait":       "Covered From Day One - No Wait",
    "One Monthly Fee — No Surprises":       "One Monthly Fee - No Surprises",
    "Book Online — Same-Week Visits":       "Book Online - Same-Week Visits",
    "Clifton Clinic — Easy to Reach":       "Clifton Clinic - Easy to Reach",
    "Join Snoots — Book Online":            "Join Snoots - Book Online",
    "Kitten Vet Membership — NJ":           "Kitten Vet Membership - NJ",
    "Senior Dog Vet Care — NJ":             "Senior Dog Vet Care - NJ",
    "Puppy Wellness Plan — Flat Fee":       "Puppy Wellness Plan, Flat Fee",
    "No Copays — Ever":                     "No Copays - Ever",
    "Book Online — Same-Week Visit":        "Book Online - Same-Week Visit",
    "Dog Dental Cleaning — Included":       "Dog Dental Cleaning - Included",
    "Cat & Dog Spay/Neuter — NJ":           "Cat & Dog Spay/Neuter - NJ",
    "No Copays — Every Visit":              "No Copays - Every Visit",
    # too long (and fix dash if needed)
    "All Vaccines & Diagnostics Included":  "All Vaccines & Diagnostics",
    "Flat-Fee Vet Care in New Jersey":      "Flat-Fee Vet in New Jersey",
    "Telehealth + In-Clinic Included":      "Telehealth + In-Clinic",
    "No Pre-Existing Condition Limits":     "No Pre-Existing Conditions",
    "Official Snoots Membership Page":      "Official Snoots Membership",
    "Unlimited Vet Care — from $55/Mo":     "Unlimited Vet Care from $55/Mo",
    "All Vaccines & Bloodwork Included":    "All Vaccines & Bloodwork",
    "Skip Pet Insurance — Join Snoots":     "Skip Insurance. Join Snoots.",
    "Unlimited Telehealth + In-Clinic":     "Telehealth + In-Clinic",
    "4.9★ Rated — 8,000+ Pets Served":     "4.9-Star Rated. 8,000+ Pets",
    "Join Snoots — Book Online Today":      "Join Snoots. Book Online Now.",
    "Affordable Vet Care — from $55/Mo":    "Affordable Vet from $55/Mo",
    "One Flat Fee. No Surprise Bills.":     "No Surprise Bills. Flat Fee",
    "Vaccines, Bloodwork & More Included":  "Vaccines, Bloodwork & More",
    "The Smarter Way to Pay for Vet Care":  "Smart Way to Pay for Vet Care",
    "4.9★ Vet — 8,000+ Happy Pets":        "Top Rated Vet. 8,000+ Pets",
    "Serving Dogs & Cats Near Clifton, NJ": "Serving Dogs & Cats in Clifton",
    "Founding Member Discount — 25% Off":   "Founding Members Save 25% Off",
    "Monthly or Annual Plans Available":    "Monthly or Annual Options",
    "from $55/Mo. Everything Included.":    "$55/Mo. Everything Included.",
    "Unlimited Visits for One Low Price":   "Unlimited Visits, Low Price",
    "No Invoice. No Copay. No Surprise.":   "No Invoices. No Copays. Ever.",
    "Cancel Anytime — No Lock-In":          "Cancel Anytime - No Lock-In",
    "Affordable Vet Care — from $55/Mo":    "Affordable Vet from $55/Mo",
    "Subscription Vet Care — from $55/Mo":  "Subscription Vet from $55/Mo",
    "Membership-Based Vet in Clifton":      "Membership Vet in Clifton, NJ",
    "Direct Primary Care for Your Pet":     "Direct Primary Care for Pets",
    "Unlimited Visits. One Monthly Fee.":   "Unlimited Visits. One Low Fee.",
    "4.9★ Rated Concierge Vet — NJ":        "4.9-Star Concierge Vet in NJ",
    "Same-Week Appointments Available":     "Same-Week Appointments",
    "NJ's First Unlimited Vet Membership":  "NJ's First Unlimited Vet Plan",
    "A Better Alternative to Pet Insurance":"A Better Alt. to Pet Insurance",
    "No Copays. No Deductibles. No Claims.":"No Copays or Deductibles. Ever",
    "Unlimited Vet Care — from $55/Mo":     "Unlimited Vet Care from $55/Mo",
    "Skip Pet Insurance. Join Snoots.":     "Skip Pet Insurance. Try Snoots",
    "Unlimited Visits. One Simple Fee.":    "Unlimited Visits, Simple Fee",
    "Pet Wellness Plan — Clifton, NJ":      "Pet Wellness Plan - Clifton NJ",
    "4.9★ Vet Membership in NJ":            "4.9-Star Vet Membership in NJ",
    "Telehealth + In-Clinic — Included":    "Telehealth + In-Clinic",
    "Founding Members Save 25% Today":      "Founding Members Save 25% Off",
    "Join Snoots — New Jersey's Vet":       "Join Snoots - New Jersey's Vet",
    "Better Than Pet Insurance — from $55/Mo": "Better Than Pet Insurance",
    "No Waiting Periods. No Exclusions.":   "No Wait Periods, No Exclusions",
    "No Deductibles. No Reimbursements.":   "No Deductibles or Repayments",
    "Trupanion Alternative — from $55/Mo":  "Trupanion Alternative - $55/Mo",
    "Pet Insurance vs. Snoots Membership":  "Pet Insurance vs. Snoots",
    "4.9★ Vet in Clifton, NJ":              "4.9-Star Vet in Clifton, NJ",
    "Compare Snoots vs. Pet Insurance":     "Compare Snoots vs. Insurance",
    "Unlimited Vet Membership — from $55/Mo": "Vet Membership from $55/Month",
    "Serving Dogs & Cats Near Clifton":     "Serving Dogs & Cats in Clifton",
    "4.9★ Vet Near Paterson & Passaic":     "4.9-Star Vet Near Paterson NJ",
    "Serving Pets Across 15 NJ Towns":      "Serving Pets Across NJ Towns",
    "Flat-Fee Vet — Minutes Away in NJ":    "Flat-Fee Vet. Minutes Away.",
    "Book a Same-Week Vet Appointment":     "Same-Week Vet Appointment",
    "Unlimited Dog Vet Care — from $55/Mo": "Unlimited Dog Vet from $55/Mo",
    "Dog Vet Membership in New Jersey":     "Dog Vet Membership in NJ",
    "Dog Wellness Plan — Flat Monthly Fee": "Dog Wellness Plan, Flat Fee",
    "Bloodwork & Diagnostics Included":     "Bloodwork & Diagnostics",
    "4.9★ Rated Vet — Near Clifton, NJ":    "4.9-Star Vet Near Clifton, NJ",
    "Skip Pet Insurance for Your Dog":      "Skip Pet Insurance for Dogs",
    "Unlimited Cat Vet Care — from $55/Mo": "Unlimited Cat Vet from $55/Mo",
    "Cat Vet Membership in New Jersey":     "Cat Vet Membership in NJ",
    "Cat Wellness Plan — Flat Monthly Fee": "Cat Wellness Plan, Flat Fee",
    "Bloodwork & Diagnostics for Cats":     "Cat Bloodwork & Diagnostics",
    "Skip Pet Insurance for Your Cat":      "Skip Pet Insurance for Cats",
    "Puppy's First Vet Visit — from $55/Mo": "Puppy's First Vet from $55/Mo",
    "Unlimited Vet Care for Your New Pet":  "Unlimited Vet for Your New Pet",
    "4.9★ Vet Near Clifton, NJ":            "4.9-Star Vet Near Clifton, NJ",
    "One Membership — Every Life Stage":    "One Plan for Every Life Stage",
    "Join Snoots — Dogs & Cats Welcome":    "Join Snoots - Dogs & Cats",
    "Dog & Cat Vaccines — from $55/Mo":     "Dog & Cat Vaccines from $55/Mo",
    "All Vaccines Included in Membership":  "All Vaccines in Membership",
    "Puppy & Kitten Vaccines Included":     "Puppy & Kitten Vaccines",
    "Pet Vaccinations Near Clifton, NJ":    "Pet Vaccinations - Clifton, NJ",
    "Core & Non-Core Vaccines Covered":     "Core & Non-Core Vaccines",
    "Vaccines + Unlimited Visits — from $55/Mo": "Vaccines + Unlimited Visits",
    "4.9★ Vet — Clifton, NJ":              "4.9-Star Vet in Clifton, NJ",
    "Annual Vet Exam — Included from $55/Mo": "Annual Vet Exam from $55/Mo",
    "Pet Wellness Exam Near Clifton, NJ":   "Pet Wellness Exam - Clifton NJ",
    "Heartworm & Flea Testing Included":    "Heartworm & Flea Testing",
    "Dog & Cat Annual Exams — Flat Fee":    "Annual Exams, Flat Fee",
    "No Extra Fee for Wellness Visits":     "No Fee for Wellness Visits",
    "Unlimited Wellness Exams Included":    "Unlimited Wellness Exams",
    "4.9★ Vet — Passaic County, NJ":        "4.9-Star Vet - Passaic County",
    "Same-Week Wellness Appointments":      "Same-Week Wellness Visits",
    "Bloodwork & Diagnostics Included":     "Bloodwork & Diagnostics",
    "Spay & Neuter Included — from $55/Mo": "Spay & Neuter from $55/Mo",
    "Bloodwork Included in Membership":     "Bloodwork in Your Membership",
    "All Diagnostics Included — from $55/Mo": "All Diagnostics from $55/Mo",
    "Imaging & Bloodwork — No Extra Cost":  "Imaging & Bloodwork Included",
    "All Routine Care — One Monthly Fee":   "All Routine Care, One Fee",

    # ── punctuation fixes: periods used as sentence separators in headlines ──
    # Google policy prohibits periods/full-stops as sentence terminators in headlines.
    "No Copays. No Surprise Bills.":        "No Copays, No Surprise Bills",
    "Unlimited Visits. One Low Fee.":       "Unlimited Visits, One Low Fee",
    "One Flat Fee. Unlimited Visits":       "One Flat Fee, Unlimited Visits",
    "No Surprise Vet Bills. Ever.":         "No Surprise Vet Bills - Ever",
    "Skip Insurance. Join Snoots.":         "Skip Insurance, Join Snoots",
    "4.9-Star Rated. 8,000+ Pets":          "4.9-Star Rated, 8,000+ Pets",
    "Cancel Anytime. No Lock-In.":          "Cancel Anytime, No Lock-In",
    "Join Snoots. Book Online Now.":        "Join Snoots - Book Online Now",
    "No Surprise Bills. One Flat Fe":       "No Surprise Bills, Flat Fee",
    "Top Rated Vet. 8,000+ Pets":           "Top Rated Vet, 8,000+ Pets",
    "$55/Mo. Everything Included.":         "$55/Mo - Everything Included",
    "No Invoices. No Copays. Ever.":        "No Invoices, No Copays, Ever",
    "Pay Once. Come in Any Time.":          "Pay Once, Come in Any Time",
    "No Per-Visit Fees. Ever.":             "No Per-Visit Fees - Ever",
    "Cancel Anytime. No Commitment.":       "Cancel Anytime, No Commitment",
    "Skip the Claims. Join Snoots.":        "Skip the Claims, Join Snoots",
    "No Copays. Unlimited Visits.":         "No Copays, Unlimited Visits",
    "Flat-Fee Vet. Minutes Away.":          "Flat-Fee Vet, Minutes Away",
    "No Copays for Your Dog. Ever.":        "No Copays for Your Dog - Ever",
    "No Copays for Your Cat. Ever.":        "No Copays for Your Cat - Ever",
    "Unlimited Procedures. One Fee.":       "Unlimited Procedures, One Fee",
    "A Better Alt. to Pet Insurance":       "A Better Alt to Pet Insurance",
    "No Copays or Deductibles. Ever":       "No Copays or Deductibles Ever",
    "Skip Pet Insurance. Try Snoots":       "Skip Pet Insurance, Try Snoots",
    "Pet Insurance vs. Snoots":             "Pet Insurance vs Snoots",
    "Compare Snoots vs. Insurance":         "Compare Snoots vs Insurance",
    "New Puppy? Start with Snoots.":        "New Puppy? Start with Snoots",
}

# Per-ad corrected descriptions (≤90 chars each)
AD_DESCRIPTIONS = {
    "Search_Brand_SnootesBrand_MaxConv": [
        "Unlimited vet visits, vaccines & telehealth from $55/mo. No copays or surprise bills.",
        "Snoots is NJ's flat-fee vet membership - no copays, deductibles or claim forms ever.",
        "4.9-star rated. 8,000+ pets. Founding members save 25% on first 12 months in Clifton.",
        "Dogs & cats welcome. Unlimited consultations, vaccines, bloodwork & telehealth from $55.",
    ],
    "Search_NB_UnlimitedVetCare_MaxConv": [
        "Snoots covers unlimited consultations, vaccines, bloodwork & telehealth from $55/month.",
        "Unlike pet insurance - no copays, deductibles or claim forms. Unlimited care from $55.",
        "NJ's first unlimited vet membership. Founding members get 25% off. Dogs & cats welcome.",
        "Unlimited visits, telehealth, bloodwork, imaging & dental. One flat monthly fee.",
    ],
    "Search_NB_AffordableVet_MaxConv": [
        "Tired of unpredictable vet bills? Snoots members pay from $55/mo - no extra charges.",
        "NJ's flat-fee vet membership. No copays, no deductibles, no surprise invoices. Ever.",
        "Unlimited consultations, diagnostics, vaccines & dental for dogs and cats from $55/mo.",
        "8,000+ pet owners switched to Snoots. Founding members get 25% off for 12 months.",
    ],
    "Search_NB_CostAnxiety_MaxConv": [
        "Vet bills adding up? Snoots members pay from $55/month - no extra charges, ever.",
        "Forget per-visit fees and surprise bills. One flat monthly fee covers everything.",
        "NJ pet owners save thousands switching to Snoots. No copays, no claims, no surprises.",
        "8,000+ pets on Snoots. Founding members lock in 25% off for 12 months in NJ.",
    ],
    "Search_NB_Concierge_MaxConv": [
        "Like DPC for humans - Snoots is a flat-fee vet membership from $55/mo. No per-visit fees.",
        "NJ's concierge vet membership. Same-week appointments, unlimited telehealth. No invoices.",
        "Unlimited consultations, telehealth, vaccines, diagnostics & dental from $55/month.",
        "8,000+ pets on Snoots. Founding members save 25% for 12 months. Passaic County, NJ.",
    ],
    "Search_NB_PetInsuranceAlt_MaxConv": [
        "Skip copays, deductibles and claim forms. Snoots is a vet membership from $55/month.",
        "Unlike pet insurance, Snoots covers preventive care with no pre-existing limits.",
        "Snoots members pay $0 out-of-pocket for all routine vet visits, vaccines & more.",
        "NJ's flat-fee vet membership. 4.9 stars, 8,000+ pets. Founding members save 25%.",
    ],
    "Search_NB_InsuranceResearch_MaxConv": [
        "Pet insurance has waiting periods and exclusions. Snoots doesn't - covered from day one.",
        "Most pet insurance reimburses 70-90% after deductibles. Snoots members pay $0 extra.",
        "Unlike Lemonade or Trupanion, Snoots covers 100% of preventive care. No claim forms.",
        "8,000+ NJ pet owners chose Snoots over pet insurance. Founding members save 25%.",
    ],
    "Search_NB_VetNearMe_MaxConv": [
        "Top-rated vet membership near you - unlimited visits, vaccines & telehealth from $55/mo.",
        "4.9-star rated vet in Clifton, NJ. Unlimited primary care for one flat monthly fee.",
        "Stop paying per visit. Unlimited consults, vaccines, bloodwork & dental from $55/mo.",
        "8,000+ pets at Snoots. Founding members lock in 25% off. Book online this week.",
    ],
    "Search_NB_VetCliftonNJ_MaxConv": [
        "Top-rated vet membership in Clifton, NJ - unlimited visits & vaccines from $55/month.",
        "4.9-star vet in Clifton, NJ. Dogs & cats get unlimited primary care. One flat fee.",
        "Stop paying per visit. Unlimited consults, vaccines, bloodwork & dental from $55/mo.",
        "8,000+ pets at Snoots. Founding members lock in 25% off. Book online this week.",
    ],
    "Search_NB_HyperLocal_MaxConv": [
        "4.9-star vet in Clifton, NJ - near Passaic, Paterson & Wayne. From $55/month.",
        "Serving pets across Passaic & Bergen County. Unlimited vet care for one flat monthly fee.",
        "Snoots is in Clifton, NJ - serving dogs & cats from Paterson to Montclair. From $55/mo.",
        "8,000+ local pets on Snoots. Founding members save 25%. Book online this week.",
    ],
    "Search_NB_DogVet_MaxConv": [
        "Give your dog unlimited vet care from $55/month - vaccines, bloodwork & telehealth.",
        "No copays or surprise vet bills for your dog. All routine care covered from $55/mo.",
        "NJ's top-rated dog vet membership. 4.9 stars. Founding members save 25%. Clifton, NJ.",
        "8,000+ pets on Snoots. Unlimited consults, vaccines & bloodwork for dogs from $55/mo.",
    ],
    "Search_NB_CatVet_MaxConv": [
        "Give your cat unlimited vet care from $55/month - vaccines, bloodwork & telehealth.",
        "No copays or surprise vet bills for your cat. All routine care covered from $55/mo.",
        "NJ's top-rated cat vet membership. 4.9 stars. Founding members save 25%. Clifton, NJ.",
        "8,000+ pets on Snoots. Unlimited consults, vaccines & bloodwork for cats from $55/mo.",
    ],
    "Search_NB_LifeStage_MaxConv": [
        "Just got a puppy or kitten? Snoots covers all vaccines & unlimited visits from $55/mo.",
        "New pets need frequent vet visits. Snoots makes it easy - unlimited care from $55/mo.",
        "From first puppy visit to senior exams, Snoots covers every stage from $55/month.",
        "8,000+ pets on Snoots. Founding members save 25%. Book and bring your pet in this week.",
    ],
    "Search_NB_Vaccinations_MaxConv": [
        "All dog & cat vaccinations included in Snoots membership. No extra charges, ever.",
        "Stop paying $50-$100 per vaccine visit. All vaccines included from $55/month.",
        "Snoots covers every vaccination - puppy series, boosters, rabies & more from $55/mo.",
        "8,000+ pets on Snoots. Founding members save 25%. Same-week vaccine appointments.",
    ],
    "Search_NB_WellnessExam_MaxConv": [
        "Annual exams, heartworm tests & wellness visits included in Snoots from $55/month.",
        "Stop paying $75-$150 for wellness exams. Snoots members get unlimited visits from $55.",
        "Full wellness care - annual exams, vaccines, parasite testing & diagnostics from $55/mo.",
        "8,000+ pets on Snoots. Founding members save 25%. Book a wellness exam this week.",
    ],
    "Search_NB_Procedures_MaxConv": [
        "Dog dental cleaning, spay/neuter, bloodwork & imaging included from $55/month.",
        "Stop getting surprised by vet costs. All diagnostics, procedures & care from $55/mo.",
        "Snoots covers spay/neuter, dental, bloodwork & imaging near Clifton, NJ from $55/mo.",
        "8,000+ pets on Snoots. Founding members save 25%. No surprise invoices, ever.",
    ],
}

# Per-ad path overrides (max 15 chars each).
# Path 1 / Path 2 are display-only suffixes appended to the auto-detected domain.
# Do NOT include the domain here — Google pulls that from Final URL automatically.
PATH_FIXES = {
    "Search_Brand_SnootesBrand_MaxConv":    ("Vet-Membership", "Join"),
    "Search_NB_UnlimitedVetCare_MaxConv":   ("Unlimited-Vet",  "Members"),
    "Search_NB_AffordableVet_MaxConv":      ("Affordable-Vet", "Members"),
    "Search_NB_CostAnxiety_MaxConv":        ("Affordable-Vet", "Members"),
    "Search_NB_Concierge_MaxConv":          ("Vet-Membership", "Members"),
    "Search_NB_PetInsuranceAlt_MaxConv":    ("No-Insurance",   "Members"),
    "Search_NB_InsuranceResearch_MaxConv":  ("vs-Insurance",   "Members"),
    "Search_NB_VetNearMe_MaxConv":          ("Vet-Near-Me",    "NJ"),
    "Search_NB_VetCliftonNJ_MaxConv":       ("Clifton-NJ",     "Vet"),
    "Search_NB_HyperLocal_MaxConv":         ("Near-You",       "NJ"),
    "Search_NB_DogVet_MaxConv":             ("Dog-Vet",        "Members"),
    "Search_NB_CatVet_MaxConv":             ("Cat-Vet",        "Members"),
    "Search_NB_LifeStage_MaxConv":          ("New-Pet",        "Members"),
    "Search_NB_Vaccinations_MaxConv":       ("Vaccines",       "Members"),
    "Search_NB_WellnessExam_MaxConv":       ("Wellness",       "Members"),
    "Search_NB_Procedures_MaxConv":         ("Whats-Included", "Members"),
}

def fix_headline(h):
    if not h:
        return h
    if h in HL_FIXES:
        return HL_FIXES[h]
    # Generic fallback: replace illegal chars
    h = h.replace("—", "-").replace("–", "-").replace("★", "")
    return h[:30]

with open("gae_rsa_ads.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

hl_cols   = [f"Headline {i}" for i in range(1, 16)]
hl_pos    = [f"Headline {i} position" for i in range(1, 16)]
desc_cols = [f"Description {i}" for i in range(1, 5)]
desc_pos  = [f"Description {i} position" for i in range(1, 5)]

out_cols = (["Row Type", "Action", "Ad status", "Campaign", "Ad group", "Ad type"]
            + hl_cols + desc_cols + hl_pos + desc_pos
            + ["Path 1", "Path 2", "Final URL"])

errors = []
with open("gae_rsa_ads.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=out_cols)
    w.writeheader()
    for r in rows:
        ad_group = r["Ad group"]
        descs = AD_DESCRIPTIONS.get(ad_group, [])
        p1, p2 = r.get("Path 1", ""), r.get("Path 2", "")
        if ad_group in PATH_FIXES:
            p1, p2 = PATH_FIXES[ad_group]

        row = {
            "Row Type": "Ad",
            "Action": "Add",
            "Ad status": "Enabled",
            "Campaign": r["Campaign"],
            "Ad group": ad_group,
            "Ad type": "Responsive search ad",
            "Path 1": p1,
            "Path 2": p2,
            "Final URL": "https://joinsnoots.com",
        }
        for c in hl_cols + hl_pos + desc_pos:
            row[c] = r.get(c, "")
        for i, c in enumerate(hl_cols):
            row[c] = fix_headline(r.get(c, ""))
        for i, c in enumerate(desc_cols):
            row[c] = descs[i] if i < len(descs) else ""

        # Validate
        for c in hl_cols:
            v = row[c]
            if v and len(v) > 30:
                errors.append(f"STILL TOO LONG [{c}] {ad_group}: {repr(v)} ({len(v)})")
        for c in desc_cols:
            v = row[c]
            if v and len(v) > 90:
                errors.append(f"STILL TOO LONG [{c}] {ad_group}: {repr(v)} ({len(v)})")
        for c in ["Path 1", "Path 2"]:
            v = row[c]
            if v and len(v) > 15:
                errors.append(f"STILL TOO LONG [{c}] {ad_group}: {repr(v)} ({len(v)})")

        w.writerow(row)

if errors:
    print("REMAINING VIOLATIONS:")
    for e in errors:
        print(" ", e)
else:
    print(f"All {len(rows)} RSA ads fixed. No remaining violations.")
