#!/usr/bin/env python3
"""
Snoots Vet — Google Ads Campaign Builder
Creates all 6 campaigns, 16 ad groups, 147 keywords, 16 RSAs, and 125 negative keywords.

Requirements:
    pip install google-ads

Setup:
    Create google-ads.yaml in this directory (or in ~/.config/google-ads.yaml):

        developer_token: YOUR_DEVELOPER_TOKEN
        client_id: YOUR_CLIENT_ID
        client_secret: YOUR_CLIENT_SECRET
        refresh_token: YOUR_REFRESH_TOKEN
        login_customer_id: YOUR_MCC_CUSTOMER_ID   # omit if not using MCC
        use_proto_plus: True

    To get a refresh token, run:
        python -m google.ads.googleads.oauth2 --client_id CLIENT_ID --client_secret CLIENT_SECRET

Usage:
    python create_campaigns.py --customer-id 123-456-7890
    python create_campaigns.py --customer-id 1234567890 --dry-run
"""

import argparse
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# ── CAMPAIGN DATA ─────────────────────────────────────────────────────────────

CAMPAIGNS = [
    ("Search_Brand_Snoots_MaxConv",            25_000_000),   # budget in micros
    ("Search_NB_UnlimitedVet_MaxConv",         60_000_000),
    ("Search_NB_PetInsuranceAlt_MaxConv",      40_000_000),
    ("Search_NB_LocalNJ_MaxConv",              50_000_000),
    ("Search_NB_PetSpecific_MaxConv",          30_000_000),
    ("Search_NB_ProcedureIntent_MaxConv",      40_000_000),
]

AD_GROUPS = [
    # (campaign_name, ad_group_name, max_cpc_micros)
    ("Search_Brand_Snoots_MaxConv",          "Search_Brand_SnootesBrand_MaxConv",    1_000_000),
    ("Search_NB_UnlimitedVet_MaxConv",       "Search_NB_UnlimitedVetCare_MaxConv",  3_000_000),
    ("Search_NB_UnlimitedVet_MaxConv",       "Search_NB_AffordableVet_MaxConv",     3_000_000),
    ("Search_NB_UnlimitedVet_MaxConv",       "Search_NB_CostAnxiety_MaxConv",       3_000_000),
    ("Search_NB_UnlimitedVet_MaxConv",       "Search_NB_Concierge_MaxConv",         3_000_000),
    ("Search_NB_PetInsuranceAlt_MaxConv",    "Search_NB_PetInsuranceAlt_MaxConv",   3_000_000),
    ("Search_NB_PetInsuranceAlt_MaxConv",    "Search_NB_InsuranceResearch_MaxConv", 3_000_000),
    ("Search_NB_LocalNJ_MaxConv",            "Search_NB_VetNearMe_MaxConv",         3_000_000),
    ("Search_NB_LocalNJ_MaxConv",            "Search_NB_VetCliftonNJ_MaxConv",      2_500_000),
    ("Search_NB_LocalNJ_MaxConv",            "Search_NB_HyperLocal_MaxConv",        2_000_000),
    ("Search_NB_PetSpecific_MaxConv",        "Search_NB_DogVet_MaxConv",            2_500_000),
    ("Search_NB_PetSpecific_MaxConv",        "Search_NB_CatVet_MaxConv",            2_500_000),
    ("Search_NB_PetSpecific_MaxConv",        "Search_NB_LifeStage_MaxConv",         2_500_000),
    ("Search_NB_ProcedureIntent_MaxConv",    "Search_NB_Vaccinations_MaxConv",      2_500_000),
    ("Search_NB_ProcedureIntent_MaxConv",    "Search_NB_WellnessExam_MaxConv",      2_500_000),
    ("Search_NB_ProcedureIntent_MaxConv",    "Search_NB_Procedures_MaxConv",        2_500_000),
]

# Match type constants (resolved at runtime from enum)
EXACT = "EXACT"
PHRASE = "PHRASE"
BROAD = "BROAD"

KEYWORDS = [
    # Brand
    ("Search_Brand_SnootesBrand_MaxConv",    "snoots vet",                   EXACT),
    ("Search_Brand_SnootesBrand_MaxConv",    "joinsnoots",                   EXACT),
    ("Search_Brand_SnootesBrand_MaxConv",    "join snoots",                  EXACT),
    ("Search_Brand_SnootesBrand_MaxConv",    "snoots vet nj",                EXACT),
    ("Search_Brand_SnootesBrand_MaxConv",    "snoots vet clifton",           EXACT),
    ("Search_Brand_SnootesBrand_MaxConv",    "snoots membership",            EXACT),
    ("Search_Brand_SnootesBrand_MaxConv",    "snoots vet",                   PHRASE),
    ("Search_Brand_SnootesBrand_MaxConv",    "join snoots",                  PHRASE),
    ("Search_Brand_SnootesBrand_MaxConv",    "snoots membership",            PHRASE),
    # NB UnlimitedVetCare
    ("Search_NB_UnlimitedVetCare_MaxConv",   "unlimited vet care",           PHRASE),
    ("Search_NB_UnlimitedVetCare_MaxConv",   "unlimited vet visits",         PHRASE),
    ("Search_NB_UnlimitedVetCare_MaxConv",   "flat fee vet",                 PHRASE),
    ("Search_NB_UnlimitedVetCare_MaxConv",   "monthly vet plan",             PHRASE),
    ("Search_NB_UnlimitedVetCare_MaxConv",   "vet subscription",             PHRASE),
    ("Search_NB_UnlimitedVetCare_MaxConv",   "vet membership",               PHRASE),
    ("Search_NB_UnlimitedVetCare_MaxConv",   "unlimited veterinary care",    PHRASE),
    ("Search_NB_UnlimitedVetCare_MaxConv",   "vet membership plan",          PHRASE),
    ("Search_NB_UnlimitedVetCare_MaxConv",   "unlimited vet care",           EXACT),
    ("Search_NB_UnlimitedVetCare_MaxConv",   "flat fee vet",                 EXACT),
    ("Search_NB_UnlimitedVetCare_MaxConv",   "vet subscription",             EXACT),
    ("Search_NB_UnlimitedVetCare_MaxConv",   "vet membership",               EXACT),
    # NB AffordableVet
    ("Search_NB_AffordableVet_MaxConv",      "affordable vet care",          PHRASE),
    ("Search_NB_AffordableVet_MaxConv",      "low cost vet care",            PHRASE),
    ("Search_NB_AffordableVet_MaxConv",      "cheap vet care",               PHRASE),
    ("Search_NB_AffordableVet_MaxConv",      "affordable veterinarian",      PHRASE),
    ("Search_NB_AffordableVet_MaxConv",      "budget vet care",              PHRASE),
    ("Search_NB_AffordableVet_MaxConv",      "inexpensive vet",              PHRASE),
    ("Search_NB_AffordableVet_MaxConv",      "affordable vet nj",            PHRASE),
    ("Search_NB_AffordableVet_MaxConv",      "low cost vet nj",              PHRASE),
    ("Search_NB_AffordableVet_MaxConv",      "affordable vet",               EXACT),
    ("Search_NB_AffordableVet_MaxConv",      "low cost vet nj",              EXACT),
    # NB CostAnxiety
    ("Search_NB_CostAnxiety_MaxConv",        "vet bills too expensive",      PHRASE),
    ("Search_NB_CostAnxiety_MaxConv",        "can't afford vet",             PHRASE),
    ("Search_NB_CostAnxiety_MaxConv",        "vet care costs",               PHRASE),
    ("Search_NB_CostAnxiety_MaxConv",        "how to afford vet bills",      PHRASE),
    ("Search_NB_CostAnxiety_MaxConv",        "vet payment plan",             PHRASE),
    ("Search_NB_CostAnxiety_MaxConv",        "vet financing nj",             PHRASE),
    ("Search_NB_CostAnxiety_MaxConv",        "vet bills too expensive",      EXACT),
    ("Search_NB_CostAnxiety_MaxConv",        "vet payment plan",             EXACT),
    # NB Concierge
    ("Search_NB_Concierge_MaxConv",          "concierge vet nj",             PHRASE),
    ("Search_NB_Concierge_MaxConv",          "membership based vet",         PHRASE),
    ("Search_NB_Concierge_MaxConv",          "subscription vet care",        PHRASE),
    ("Search_NB_Concierge_MaxConv",          "preventive vet care plan",     PHRASE),
    ("Search_NB_Concierge_MaxConv",          "pet care membership",          PHRASE),
    ("Search_NB_Concierge_MaxConv",          "direct primary care vet",      PHRASE),
    ("Search_NB_Concierge_MaxConv",          "concierge vet nj",             EXACT),
    ("Search_NB_Concierge_MaxConv",          "pet care membership",          EXACT),
    # NB PetInsuranceAlt
    ("Search_NB_PetInsuranceAlt_MaxConv",    "pet insurance alternative",    PHRASE),
    ("Search_NB_PetInsuranceAlt_MaxConv",    "alternative to pet insurance", PHRASE),
    ("Search_NB_PetInsuranceAlt_MaxConv",    "pet wellness plan",            PHRASE),
    ("Search_NB_PetInsuranceAlt_MaxConv",    "pet health plan",              PHRASE),
    ("Search_NB_PetInsuranceAlt_MaxConv",    "pet care plan",                PHRASE),
    ("Search_NB_PetInsuranceAlt_MaxConv",    "dog health plan",              PHRASE),
    ("Search_NB_PetInsuranceAlt_MaxConv",    "cat health plan",              PHRASE),
    ("Search_NB_PetInsuranceAlt_MaxConv",    "pet subscription vet",         PHRASE),
    ("Search_NB_PetInsuranceAlt_MaxConv",    "is pet insurance worth it",    PHRASE),
    ("Search_NB_PetInsuranceAlt_MaxConv",    "pet insurance alternative",    EXACT),
    ("Search_NB_PetInsuranceAlt_MaxConv",    "pet wellness plan",            EXACT),
    ("Search_NB_PetInsuranceAlt_MaxConv",    "pet health plan",              EXACT),
    # NB InsuranceResearch
    ("Search_NB_InsuranceResearch_MaxConv",  "best pet insurance nj",                    PHRASE),
    ("Search_NB_InsuranceResearch_MaxConv",  "pet insurance vs wellness plan",           PHRASE),
    ("Search_NB_InsuranceResearch_MaxConv",  "is pet insurance worth it for dogs",       PHRASE),
    ("Search_NB_InsuranceResearch_MaxConv",  "pet insurance no waiting period",          PHRASE),
    ("Search_NB_InsuranceResearch_MaxConv",  "pet insurance pre-existing conditions",    PHRASE),
    ("Search_NB_InsuranceResearch_MaxConv",  "lemonade pet insurance alternative",       PHRASE),
    ("Search_NB_InsuranceResearch_MaxConv",  "trupanion alternative",                    PHRASE),
    ("Search_NB_InsuranceResearch_MaxConv",  "best pet insurance nj",                    EXACT),
    ("Search_NB_InsuranceResearch_MaxConv",  "trupanion alternative",                    EXACT),
    # NB VetNearMe
    ("Search_NB_VetNearMe_MaxConv",          "vet near me",                  PHRASE),
    ("Search_NB_VetNearMe_MaxConv",          "veterinarian near me",         PHRASE),
    ("Search_NB_VetNearMe_MaxConv",          "animal hospital near me",      PHRASE),
    ("Search_NB_VetNearMe_MaxConv",          "dog vet near me",              PHRASE),
    ("Search_NB_VetNearMe_MaxConv",          "cat vet near me",              PHRASE),
    ("Search_NB_VetNearMe_MaxConv",          "vet clinic near me",           PHRASE),
    ("Search_NB_VetNearMe_MaxConv",          "vet near me",                  EXACT),
    ("Search_NB_VetNearMe_MaxConv",          "veterinarian near me",         EXACT),
    # NB VetCliftonNJ
    ("Search_NB_VetCliftonNJ_MaxConv",       "vet clifton nj",               PHRASE),
    ("Search_NB_VetCliftonNJ_MaxConv",       "veterinarian clifton nj",      PHRASE),
    ("Search_NB_VetCliftonNJ_MaxConv",       "animal hospital clifton nj",   PHRASE),
    ("Search_NB_VetCliftonNJ_MaxConv",       "vet clifton",                  PHRASE),
    ("Search_NB_VetCliftonNJ_MaxConv",       "vet clifton nj",               EXACT),
    ("Search_NB_VetCliftonNJ_MaxConv",       "veterinarian clifton nj",      EXACT),
    # NB HyperLocal
    ("Search_NB_HyperLocal_MaxConv",         "vet passaic nj",               EXACT),
    ("Search_NB_HyperLocal_MaxConv",         "vet paterson nj",              EXACT),
    ("Search_NB_HyperLocal_MaxConv",         "vet wayne nj",                 EXACT),
    ("Search_NB_HyperLocal_MaxConv",         "vet nutley nj",                EXACT),
    ("Search_NB_HyperLocal_MaxConv",         "vet bloomfield nj",            EXACT),
    ("Search_NB_HyperLocal_MaxConv",         "vet montclair nj",             EXACT),
    ("Search_NB_HyperLocal_MaxConv",         "vet hawthorne nj",             EXACT),
    ("Search_NB_HyperLocal_MaxConv",         "vet garfield nj",              EXACT),
    ("Search_NB_HyperLocal_MaxConv",         "vet rutherford nj",            EXACT),
    ("Search_NB_HyperLocal_MaxConv",         "vet teaneck nj",               EXACT),
    ("Search_NB_HyperLocal_MaxConv",         "vet fair lawn nj",             EXACT),
    ("Search_NB_HyperLocal_MaxConv",         "vet lyndhurst nj",             EXACT),
    ("Search_NB_HyperLocal_MaxConv",         "veterinarian passaic nj",      PHRASE),
    ("Search_NB_HyperLocal_MaxConv",         "veterinarian paterson nj",     PHRASE),
    ("Search_NB_HyperLocal_MaxConv",         "veterinarian wayne nj",        PHRASE),
    ("Search_NB_HyperLocal_MaxConv",         "veterinarian nutley nj",       PHRASE),
    # NB DogVet
    ("Search_NB_DogVet_MaxConv",             "dog vet membership",           PHRASE),
    ("Search_NB_DogVet_MaxConv",             "unlimited dog vet care",       PHRASE),
    ("Search_NB_DogVet_MaxConv",             "dog vet subscription",         PHRASE),
    ("Search_NB_DogVet_MaxConv",             "puppy vet plan",               PHRASE),
    ("Search_NB_DogVet_MaxConv",             "dog health plan nj",           PHRASE),
    ("Search_NB_DogVet_MaxConv",             "dog vet nj",                   PHRASE),
    ("Search_NB_DogVet_MaxConv",             "dog vet membership",           EXACT),
    ("Search_NB_DogVet_MaxConv",             "dog vet nj",                   EXACT),
    # NB CatVet
    ("Search_NB_CatVet_MaxConv",             "cat vet membership",           PHRASE),
    ("Search_NB_CatVet_MaxConv",             "unlimited cat vet care",       PHRASE),
    ("Search_NB_CatVet_MaxConv",             "cat vet subscription",         PHRASE),
    ("Search_NB_CatVet_MaxConv",             "kitten vet plan",              PHRASE),
    ("Search_NB_CatVet_MaxConv",             "cat health plan nj",           PHRASE),
    ("Search_NB_CatVet_MaxConv",             "cat vet nj",                   PHRASE),
    ("Search_NB_CatVet_MaxConv",             "cat vet membership",           EXACT),
    ("Search_NB_CatVet_MaxConv",             "cat vet nj",                   EXACT),
    # NB LifeStage
    ("Search_NB_LifeStage_MaxConv",          "new puppy vet visit",          PHRASE),
    ("Search_NB_LifeStage_MaxConv",          "puppy first vet visit",        PHRASE),
    ("Search_NB_LifeStage_MaxConv",          "puppy vaccine schedule nj",    PHRASE),
    ("Search_NB_LifeStage_MaxConv",          "kitten first vet visit",       PHRASE),
    ("Search_NB_LifeStage_MaxConv",          "dog wellness exam nj",         PHRASE),
    ("Search_NB_LifeStage_MaxConv",          "cat wellness exam nj",         PHRASE),
    ("Search_NB_LifeStage_MaxConv",          "senior dog vet nj",            PHRASE),
    ("Search_NB_LifeStage_MaxConv",          "new puppy vet visit",          EXACT),
    ("Search_NB_LifeStage_MaxConv",          "puppy first vet visit",        EXACT),
    # NB Vaccinations
    ("Search_NB_Vaccinations_MaxConv",       "dog vaccinations nj",          PHRASE),
    ("Search_NB_Vaccinations_MaxConv",       "cat vaccinations nj",          PHRASE),
    ("Search_NB_Vaccinations_MaxConv",       "puppy vaccinations nj",        PHRASE),
    ("Search_NB_Vaccinations_MaxConv",       "kitten vaccinations nj",       PHRASE),
    ("Search_NB_Vaccinations_MaxConv",       "dog vaccines nj",              PHRASE),
    ("Search_NB_Vaccinations_MaxConv",       "cat vaccines nj",              PHRASE),
    ("Search_NB_Vaccinations_MaxConv",       "pet vaccinations near me",     PHRASE),
    ("Search_NB_Vaccinations_MaxConv",       "dog vaccinations nj",          EXACT),
    ("Search_NB_Vaccinations_MaxConv",       "cat vaccinations nj",          EXACT),
    # NB WellnessExam
    ("Search_NB_WellnessExam_MaxConv",       "dog wellness exam nj",         PHRASE),
    ("Search_NB_WellnessExam_MaxConv",       "cat wellness exam nj",         PHRASE),
    ("Search_NB_WellnessExam_MaxConv",       "pet annual exam nj",           PHRASE),
    ("Search_NB_WellnessExam_MaxConv",       "heartworm test nj",            PHRASE),
    ("Search_NB_WellnessExam_MaxConv",       "flea tick prevention vet nj",  PHRASE),
    ("Search_NB_WellnessExam_MaxConv",       "dog annual exam nj",           EXACT),
    ("Search_NB_WellnessExam_MaxConv",       "cat annual exam nj",           EXACT),
    # NB Procedures
    ("Search_NB_Procedures_MaxConv",         "dog bloodwork cost nj",        PHRASE),
    ("Search_NB_Procedures_MaxConv",         "dog spay neuter cost nj",      PHRASE),
    ("Search_NB_Procedures_MaxConv",         "dog dental cleaning cost nj",  PHRASE),
    ("Search_NB_Procedures_MaxConv",         "cat spay neuter nj",           PHRASE),
    ("Search_NB_Procedures_MaxConv",         "dog bloodwork nj",             PHRASE),
    ("Search_NB_Procedures_MaxConv",         "cat dental cleaning nj",       PHRASE),
    ("Search_NB_Procedures_MaxConv",         "dog bloodwork cost nj",        EXACT),
    ("Search_NB_Procedures_MaxConv",         "dog dental cleaning cost nj",  EXACT),
]

BRAND_NEGATIVES = [
    "snoots snack", "snoots candy", "snoots bar", "snoots food",
    "free snoots", "snoots coupon", "snoots promo code",
    "snoots jobs", "snoots careers", "snoots complaints",
]

NB_NEGATIVES = [
    "snoots", "joinsnoots", "snootsvet", "free", "diy", "home vet",
    "jobs", "careers", "salary", "login", "portal",
    "how to become a vet", "vet school", "veterinary school",
    "vet tech", "vet assistant", "vet technician",
    "wildlife vet", "exotic vet", "emergency vet",
    "24 hour vet", "overnight vet", "vet hospital",
]

NB_CAMPAIGNS = [
    "Search_NB_UnlimitedVet_MaxConv",
    "Search_NB_PetInsuranceAlt_MaxConv",
    "Search_NB_LocalNJ_MaxConv",
    "Search_NB_PetSpecific_MaxConv",
    "Search_NB_ProcedureIntent_MaxConv",
]

# ── RSA DATA ──────────────────────────────────────────────────────────────────

def _rsa(ad_group, final_url, path1, path2, headlines, descs, pin_h1=False):
    return {
        "ad_group": ad_group,
        "final_url": final_url,
        "path1": path1,
        "path2": path2,
        "headlines": headlines,
        "descriptions": descs,
        "pin_h1": pin_h1,
    }

LOCAL_HEADLINES = [
    "Vet Near You in New Jersey", "Unlimited Vet Membership — from $55/Mo",
    "4.9★ Vet in Clifton, NJ", "No Copays. Unlimited Visits.",
    "All Vaccines & Bloodwork Included", "Book a Vet Appointment Today",
    "Serving Dogs & Cats Near Clifton", "One Monthly Fee — No Surprises",
    "Telehealth Available Too", "New Jersey's Top-Rated Vet",
    "8,000+ Pets Served", "Founding Members Save 25%",
    "Skip Pet Insurance — Join Snoots", "Book Online — Same-Week Visits",
    "Clifton, NJ Vet Clinic",
]
LOCAL_DESCS = [
    "Snoots is the top-rated vet membership near you — unlimited visits, all vaccines, telehealth and diagnostics from $55/month. No copays, ever.",
    "A 4.9-star rated vet clinic in Clifton, NJ. Our members get unlimited primary care for one flat monthly fee — dogs and cats welcome.",
    "Stop paying per visit. Join Snoots and get unlimited consultations, vaccines, bloodwork, dental & telehealth — all from $55/month near Clifton, NJ.",
    "Join 8,000+ happy pets at Snoots. Founding members lock in 25% off for their first 12 months. Book online and come in as soon as this week.",
]

RSA_DATA = [
    _rsa("Search_Brand_SnootesBrand_MaxConv",
         "https://joinsnoots.com", "joinsnoots.com", "Join",
         ["Snoots Vet — Official Site", "Unlimited Vet Care from $55/Mo", "Join Snoots Today",
          "The Unlimited Vet Membership", "No Copays. No Surprise Bills.",
          "All Vaccines & Diagnostics Included", "Flat-Fee Vet Care in New Jersey",
          "4.9★ Rated Vet in New Jersey", "Founding Members Save 25%",
          "Unlimited Visits. One Low Fee.", "Dogs & Cats Welcome", "Clifton, NJ — Book Today",
          "Telehealth + In-Clinic Included", "No Pre-Existing Condition Limits",
          "Official Snoots Membership Page"],
         ["Skip the surprise vet bills. Snoots members get unlimited consultations, all vaccines, bloodwork & telehealth from $55/month.",
          "Unlike pet insurance, Snoots is a vet membership — no copays, no deductibles, no claim forms. Just bring your pet in, any time.",
          "New Jersey's first unlimited vet membership. Founding members save 25% on their first 12 months. Dogs & cats welcome in Clifton, NJ.",
          "8,000+ pets served. 4.9-star Google rating. Unlimited primary care including vaccines, diagnostics, dental & telehealth — join today."],
         pin_h1=True),

    _rsa("Search_NB_UnlimitedVetCare_MaxConv",
         "https://joinsnoots.com/members", "joinsnoots.com", "Unlimited-Vet",
         ["Unlimited Vet Care — from $55/Mo", "One Flat Fee. Unlimited Visits.",
          "Vet Membership — No Copays", "All Vaccines & Bloodwork Included",
          "No Surprise Vet Bills. Ever.", "The Unlimited Vet from $55/Mo",
          "Skip Pet Insurance — Join Snoots", "Flat-Fee Vet in New Jersey",
          "Unlimited Telehealth + In-Clinic", "4.9★ Rated — 8,000+ Pets Served",
          "New Jersey's Unlimited Vet", "Dogs & Cats Welcome",
          "Founding Members Save 25%", "Cancel Anytime. No Lock-In.",
          "Join Snoots — Book Online Today"],
         ["Snoots is a vet membership that covers unlimited consultations, all vaccines, diagnostics, telehealth and routine care from $55/month — no copays, ever.",
          "Unlike pet insurance, there are no copays, deductibles or claim forms. Pay from $55/month and bring your dog or cat in as often as you need.",
          "New Jersey's first unlimited vet membership. Founding members get 25% off their first 12 months. Serving dogs & cats in Clifton, NJ.",
          "Includes unlimited in-person visits, telehealth, bloodwork, imaging, dental cleaning & all vaccinations. One flat fee — no hidden costs."]),

    _rsa("Search_NB_AffordableVet_MaxConv",
         "https://joinsnoots.com/members", "joinsnoots.com", "Affordable-Vet",
         ["Affordable Vet Care — from $55/Mo", "One Flat Fee. No Surprise Bills.",
          "Low Cost Vet Membership in NJ", "All Vet Care — One Monthly Fee",
          "Unlimited Visits from $55/Mo", "Stop Overpaying for Vet Bills",
          "Vaccines, Bloodwork & More Included", "The Smarter Way to Pay for Vet Care",
          "4.9★ Vet — 8,000+ Happy Pets", "Serving Dogs & Cats Near Clifton, NJ",
          "Flat-Fee Vet — No Copays", "Founding Member Discount — 25% Off",
          "Telehealth + In-Clinic Visits", "Monthly or Annual Plans Available",
          "Join Snoots Vet — Book Today"],
         ["Tired of unpredictable vet bills? Snoots members pay from $55/month and get unlimited vet visits, all vaccines, bloodwork & telehealth — no extra charges.",
          "Snoots is New Jersey's flat-fee vet membership. No copays, no deductibles, no surprise invoices. Just unlimited primary care for your pet.",
          "Dogs and cats get unlimited consultations, diagnostics, vaccinations, dental and telehealth — all covered by from $55/month membership.",
          "Join 8,000+ pet owners who switched to Snoots. Founding members lock in 25% off for 12 months. Serving the greater Clifton, NJ area."]),

    _rsa("Search_NB_CostAnxiety_MaxConv",
         "https://joinsnoots.com/members", "joinsnoots.com", "Affordable-Vet",
         ["Tired of Expensive Vet Bills?", "from $55/Mo. Everything Included.",
          "Stop Paying Per Vet Visit", "No Surprise Vet Bills. Ever.",
          "Flat-Fee Vet Near Clifton, NJ", "Unlimited Visits for One Low Price",
          "Affordable Vet Care — from $55/Mo", "No Invoice. No Copay. No Surprise.",
          "4.9★ Vet — 8,000+ Pets Served", "Dogs & Cats Welcome",
          "Founding Members Save 25%", "Pay Once. Come in Any Time.",
          "Cancel Anytime — No Lock-In", "Telehealth Included Too",
          "Join Snoots — Book Online Today"],
         ["Unpredictable vet bills add up fast. Snoots members pay from $55/month and get unlimited visits, all vaccines, bloodwork and telehealth — no extra charges, ever.",
          "Forget per-visit fees, invoices, and surprise bills. Snoots is a flat monthly membership covering all the vet care your dog or cat will ever need.",
          "New Jersey pet owners save thousands by switching to Snoots. A low monthly fee replaces all routine vet costs — no copays, no claims, no surprises.",
          "Join 8,000+ pets on Snoots. Founding members lock in 25% off for 12 months. Serving Clifton and the surrounding NJ area."]),

    _rsa("Search_NB_Concierge_MaxConv",
         "https://joinsnoots.com/members", "joinsnoots.com", "Membership",
         ["Concierge Vet Membership — NJ", "Subscription Vet Care — from $55/Mo",
          "Membership-Based Vet in Clifton", "Preventive Care Plan for Pets",
          "Direct Primary Care for Your Pet", "Unlimited Visits. One Monthly Fee.",
          "No Per-Visit Fees. Ever.", "4.9★ Rated Concierge Vet — NJ",
          "All Preventive Care Included", "Telehealth + In-Clinic Included",
          "Dogs & Cats Welcome", "Cancel Anytime. No Commitment.",
          "Founding Members Save 25%", "Same-Week Appointments Available",
          "NJ's First Unlimited Vet Membership"],
         ["Like DPC for humans, Snoots is a flat-fee vet membership — pay from $55/month and get unlimited primary and preventive care for your dog or cat. No per-visit fees.",
          "Snoots is New Jersey's concierge vet membership. Members get same-week appointments, unlimited telehealth, and zero surprise invoices for one flat monthly fee.",
          "Unlimited consultations, telehealth, vaccines, diagnostics and dental cleaning — all included in from $55/month membership. No per-visit charges, ever.",
          "Join 8,000+ pets on Snoots. Founding members lock in 25% off for their first 12 months. Clifton, NJ — serving the greater Passaic County area."]),

    _rsa("Search_NB_PetInsuranceAlt_MaxConv",
         "https://joinsnoots.com/members", "joinsnoots.com", "Not-Pet-Insurance",
         ["A Better Alternative to Pet Insurance", "No Copays. No Deductibles. No Claims.",
          "Unlimited Vet Care — from $55/Mo", "Skip Pet Insurance. Join Snoots.",
          "Pet Health Plan — from $55/Mo", "All Vaccines & Diagnostics Included",
          "Unlimited Visits. One Simple Fee.", "No Pre-Existing Condition Limits",
          "Pet Wellness Plan — Clifton, NJ", "4.9★ Vet Membership in NJ",
          "Telehealth + In-Clinic — Included", "Dogs & Cats — No Exclusions",
          "Monthly or Annual — You Choose", "Founding Members Save 25% Today",
          "Join Snoots — New Jersey's Vet"],
         ["Skip the copays, deductibles and claim forms. Snoots is a vet membership — pay from $55/month and get unlimited primary care for your dog or cat.",
          "Unlike pet insurance, Snoots covers preventive care with no pre-existing condition limits. Unlimited consultations, vaccines, bloodwork & more.",
          "Snoots members never pay out-of-pocket for routine vet visits. One flat monthly fee covers everything your pet needs, every time they need it.",
          "New Jersey's first flat-fee vet membership. 4.9 stars, 8,000+ pets served. Founding members get 25% off for 12 months — join today in Clifton, NJ."]),

    _rsa("Search_NB_InsuranceResearch_MaxConv",
         "https://joinsnoots.com/members", "joinsnoots.com", "vs-Insurance",
         ["Better Than Pet Insurance — from $55/Mo", "No Waiting Periods. No Exclusions.",
          "No Deductibles. No Reimbursements.", "No Pre-Existing Condition Limits",
          "Skip the Claims. Join Snoots.", "Lemonade Alternative — NJ",
          "Trupanion Alternative — from $55/Mo", "Pet Insurance vs. Snoots Membership",
          "Covered From Day One — No Wait", "4.9★ Vet in Clifton, NJ",
          "All Vaccines & Diagnostics Included", "Dogs & Cats Welcome",
          "Founding Members Save 25%", "Monthly or Annual — You Choose",
          "Compare Snoots vs. Pet Insurance"],
         ["Pet insurance has waiting periods, deductibles, and pre-existing condition exclusions. Snoots doesn't — pay from $55/month and your pet is covered from day one.",
          "Most pet insurance reimburses 70–90% after your deductible. Snoots members pay $0 out-of-pocket for every routine visit, vaccine, and diagnostic.",
          "Unlike Lemonade or Trupanion, Snoots covers 100% of preventive and primary care — no claim forms, no waiting, no surprises. Just bring your pet in.",
          "Join 8,000+ New Jersey pet owners who chose Snoots over pet insurance. Founding members save 25% for 12 months — sign up today in Clifton, NJ."]),

    _rsa("Search_NB_VetNearMe_MaxConv",
         "https://joinsnoots.com/us", "joinsnoots.com", "Vet-Near-Me",
         LOCAL_HEADLINES, LOCAL_DESCS),

    _rsa("Search_NB_VetCliftonNJ_MaxConv",
         "https://joinsnoots.com/us", "joinsnoots.com", "Clifton-NJ",
         LOCAL_HEADLINES, LOCAL_DESCS),

    _rsa("Search_NB_HyperLocal_MaxConv",
         "https://joinsnoots.com/us", "joinsnoots.com", "Near-You",
         ["Vet Serving Passaic County, NJ", "Unlimited Vet Membership — from $55/Mo",
          "4.9★ Vet Near Paterson & Passaic", "Serving Pets Across 15 NJ Towns",
          "Flat-Fee Vet — Minutes Away in NJ", "No Copays. Unlimited Visits.",
          "All Vaccines & Bloodwork Included", "Near Paterson, Wayne & Nutley",
          "Book a Same-Week Vet Appointment", "Telehealth + In-Clinic — Included",
          "Dogs & Cats Welcome", "Founding Members Save 25%",
          "Skip Pet Insurance — Join Snoots", "Clifton Clinic — Easy to Reach",
          "Join Snoots — Book Online"],
         ["Snoots is a 4.9-star vet membership in Clifton, NJ — just minutes from Passaic, Paterson, Wayne, Nutley, and Bloomfield. from $55/month, unlimited visits.",
          "Serving pets across Passaic and Bergen County. Snoots members get unlimited vet care, all vaccines, telehealth and diagnostics for one flat monthly fee.",
          "Stop driving far for a great vet. Snoots is in Clifton, NJ — serving dogs and cats from Paterson to Montclair and everywhere in between.",
          "Join 8,000+ local pets on Snoots. Founding members lock in 25% off for their first 12 months. Book online and come in as soon as this week."]),

    _rsa("Search_NB_DogVet_MaxConv",
         "https://joinsnoots.com/members", "joinsnoots.com", "Dog-Vet",
         ["Unlimited Dog Vet Care — from $55/Mo", "Dog Vet Membership in New Jersey",
          "All Dog Vaccines Included", "No Copays for Your Dog. Ever.",
          "Unlimited Dog Vet Visits", "Dog Wellness Plan — Flat Monthly Fee",
          "Bloodwork & Diagnostics Included", "4.9★ Rated Vet — Near Clifton, NJ",
          "Telehealth for Dogs Too", "Puppy & Adult Dogs Welcome",
          "Spay & Neuter Included", "Founding Members Save 25%",
          "Skip Pet Insurance for Your Dog", "One Fee Covers Everything",
          "Join Snoots — Book Online"],
         ["Give your dog unlimited vet care from $55/month. Snoots membership includes all vaccinations, bloodwork, diagnostics, telehealth & unlimited visits.",
          "No copays, no surprise vet bills for your dog. Snoots covers all routine and preventive care — spay/neuter, dental, imaging and more included.",
          "New Jersey's top-rated dog vet membership. 4.9 stars. Founding members get 25% off their first 12 months. Puppies and adults welcome near Clifton, NJ.",
          "Join 8,000+ pets on Snoots. Unlimited consultations, all vaccines, bloodwork and telehealth for your dog — one simple from $55/month membership."]),

    _rsa("Search_NB_CatVet_MaxConv",
         "https://joinsnoots.com/members", "joinsnoots.com", "Cat-Vet",
         ["Unlimited Cat Vet Care — from $55/Mo", "Cat Vet Membership in New Jersey",
          "All Cat Vaccines Included", "No Copays for Your Cat. Ever.",
          "Unlimited Cat Vet Visits", "Cat Wellness Plan — Flat Monthly Fee",
          "Bloodwork & Diagnostics for Cats", "4.9★ Rated Vet — Near Clifton, NJ",
          "Telehealth for Cats Too", "Kittens & Adult Cats Welcome",
          "Spay & Neuter Included", "Founding Members Save 25%",
          "Skip Pet Insurance for Your Cat", "One Fee Covers Everything",
          "Join Snoots — Book Online"],
         ["Give your cat unlimited vet care from $55/month. Snoots membership includes all vaccinations, bloodwork, diagnostics, telehealth & unlimited visits.",
          "No copays, no surprise vet bills for your cat. Snoots covers all routine and preventive care — spay/neuter, dental, imaging and more included.",
          "New Jersey's top-rated cat vet membership. 4.9 stars. Founding members get 25% off their first 12 months. Kittens and adults welcome near Clifton, NJ.",
          "Join 8,000+ pets on Snoots. Unlimited consultations, all vaccines, bloodwork and telehealth for your cat — one simple from $55/month membership."]),

    _rsa("Search_NB_LifeStage_MaxConv",
         "https://joinsnoots.com/members", "joinsnoots.com", "New-Pet",
         ["New Puppy? Start with Snoots.", "Puppy's First Vet Visit — from $55/Mo",
          "All Puppy Vaccines Included", "Kitten Vet Membership — NJ",
          "Senior Dog Vet Care — NJ", "Unlimited Vet Care for Your New Pet",
          "Puppy Wellness Plan — Flat Fee", "4.9★ Vet Near Clifton, NJ",
          "One Membership — Every Life Stage", "Telehealth for New Pets Too",
          "Spay & Neuter Included", "Founding Members Save 25%",
          "No Copays — Ever", "Book Online — Same-Week Visit",
          "Join Snoots — Dogs & Cats Welcome"],
         ["Just got a puppy or kitten? Snoots membership covers all your new pet's vaccines, wellness exams, and unlimited visits from $55/month — no per-visit fees.",
          "New pets need frequent vet visits in their first year. Snoots makes it stress-free — unlimited appointments, all vaccinations, and telehealth included.",
          "From first puppy visit to senior wellness exams, Snoots covers every stage of your pet's life for one flat monthly fee. Dogs and cats welcome in Clifton, NJ.",
          "Join 8,000+ pets on Snoots. Founding members lock in 25% off for their first 12 months — sign up today and bring your new pet in this week."]),

    _rsa("Search_NB_Vaccinations_MaxConv",
         "https://joinsnoots.com/members", "joinsnoots.com", "Vaccines",
         ["Dog & Cat Vaccines — from $55/Mo", "All Vaccines Included in Membership",
          "No Extra Charge for Vaccines", "Puppy & Kitten Vaccines Included",
          "Pet Vaccinations Near Clifton, NJ", "Stop Paying Per Vaccine Visit",
          "Core & Non-Core Vaccines Covered", "Vaccines + Unlimited Visits — from $55/Mo",
          "4.9★ Vet — Clifton, NJ", "Same-Week Vaccine Appointments",
          "Dogs & Cats Welcome", "Founding Members Save 25%",
          "Telehealth + In-Clinic Included", "No Copays for Vaccine Visits",
          "Join Snoots — Book Online"],
         ["All dog and cat vaccinations are included in your Snoots membership. Pay from $55/month and bring your pet in for vaccines any time — no extra charges.",
          "Stop paying $50–$100 per vaccine visit. Snoots membership includes all core and non-core vaccines for your dog or cat — unlimited, at no extra cost.",
          "Snoots covers every vaccination your pet needs — puppy series, annual boosters, rabies, Bordetella and more. All included in from $55/month membership.",
          "Join 8,000+ pets on Snoots. Founding members lock in 25% off their first 12 months. Same-week vaccine appointments available in Clifton, NJ."]),

    _rsa("Search_NB_WellnessExam_MaxConv",
         "https://joinsnoots.com/members", "joinsnoots.com", "Wellness",
         ["Annual Vet Exam — Included from $55/Mo", "Pet Wellness Exam Near Clifton, NJ",
          "Heartworm & Flea Testing Included", "Dog & Cat Annual Exams — Flat Fee",
          "No Extra Fee for Wellness Visits", "Unlimited Wellness Exams Included",
          "4.9★ Vet — Passaic County, NJ", "Same-Week Wellness Appointments",
          "Telehealth for Follow-Ups Too", "Bloodwork & Diagnostics Included",
          "Dogs & Cats Welcome", "Founding Members Save 25%",
          "No Copays — Every Visit", "Skip Per-Exam Vet Fees",
          "Join Snoots — Book Online Today"],
         ["Annual exams, heartworm tests, flea/tick prevention consultations, and all wellness visits are included in your Snoots membership — no extra charges.",
          "Stop paying $75–$150 for annual wellness exams. Snoots members get unlimited wellness visits, bloodwork, and diagnostics from $55/month.",
          "Snoots covers your pet's full wellness care — annual exams, vaccine boosters, parasite testing, and diagnostics — all in from $55/month membership.",
          "Join 8,000+ pets on Snoots. Founding members lock in 25% off for their first 12 months. Book a wellness exam this week in Clifton, NJ."]),

    _rsa("Search_NB_Procedures_MaxConv",
         "https://joinsnoots.com/members", "joinsnoots.com", "Whats-Included",
         ["Spay & Neuter Included — from $55/Mo", "Dog Dental Cleaning — Included",
          "Bloodwork Included in Membership", "Stop Paying Per Procedure",
          "All Diagnostics Included — from $55/Mo", "Imaging & Bloodwork — No Extra Cost",
          "4.9★ Vet in Clifton, NJ", "Unlimited Procedures. One Fee.",
          "Cat & Dog Spay/Neuter — NJ", "No Surprise Procedure Bills",
          "Dogs & Cats Welcome", "Founding Members Save 25%",
          "Telehealth + In-Clinic Included", "All Routine Care — One Monthly Fee",
          "Join Snoots — Book Online"],
         ["Dog dental cleaning, spay/neuter, bloodwork, imaging, and all routine procedures are included in your Snoots membership — no per-procedure charges.",
          "Stop getting surprised by vet procedure costs. Snoots members pay from $55/month and get all diagnostics, bloodwork, imaging and routine procedures included.",
          "Snoots covers spay/neuter, dental cleaning, full bloodwork panels, imaging, and more — all included in from $55/month membership near Clifton, NJ.",
          "Join 8,000+ pets on Snoots. Founding members lock in 25% off for their first 12 months. No surprise invoices — ever. Book online today."]),
]

# ── API HELPERS ───────────────────────────────────────────────────────────────

def get_match_type_enum(client, match_type_str):
    return client.enums.KeywordMatchTypeEnum[match_type_str]

def create_budget(client, customer_id, campaign_name, budget_micros, dry_run):
    budget_service = client.get_service("CampaignBudgetService")
    op = client.get_type("CampaignBudgetOperation")
    budget = op.create
    budget.name = f"{campaign_name}_Budget"
    budget.amount_micros = budget_micros
    budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
    if dry_run:
        print(f"  [DRY RUN] Would create budget: {campaign_name}_Budget @ ${budget_micros/1_000_000:.2f}/day")
        return f"customers/{customer_id}/campaignBudgets/DRY_RUN"
    response = budget_service.mutate_campaign_budgets(customer_id=customer_id, operations=[op])
    return response.results[0].resource_name

def create_campaign(client, customer_id, name, budget_resource, dry_run):
    campaign_service = client.get_service("CampaignService")
    op = client.get_type("CampaignOperation")
    campaign = op.create
    campaign.name = name
    campaign.status = client.enums.CampaignStatusEnum.PAUSED
    campaign.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH
    campaign.campaign_budget = budget_resource
    campaign.bidding_strategy_type = client.enums.BiddingStrategyTypeEnum.MAXIMIZE_CONVERSIONS
    campaign.network_settings.target_google_search = True
    campaign.network_settings.target_search_network = False
    campaign.network_settings.target_content_network = False
    if dry_run:
        print(f"  [DRY RUN] Would create campaign: {name}")
        return f"customers/{customer_id}/campaigns/DRY_RUN_{name}"
    response = campaign_service.mutate_campaigns(customer_id=customer_id, operations=[op])
    return response.results[0].resource_name

def create_ad_group(client, customer_id, campaign_resource, ag_name, cpc_micros, dry_run):
    ag_service = client.get_service("AdGroupService")
    op = client.get_type("AdGroupOperation")
    ag = op.create
    ag.name = ag_name
    ag.status = client.enums.AdGroupStatusEnum.ENABLED
    ag.campaign = campaign_resource
    ag.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD
    ag.cpc_bid_micros = cpc_micros
    if dry_run:
        print(f"    [DRY RUN] Would create ad group: {ag_name} (max CPC ${cpc_micros/1_000_000:.2f})")
        return f"customers/{customer_id}/adGroups/DRY_RUN_{ag_name}"
    response = ag_service.mutate_ad_groups(customer_id=customer_id, operations=[op])
    return response.results[0].resource_name

def create_keywords(client, customer_id, ag_resource, keywords, dry_run):
    if not keywords:
        return
    ag_criterion_service = client.get_service("AdGroupCriterionService")
    ops = []
    for text, match_type in keywords:
        op = client.get_type("AdGroupCriterionOperation")
        criterion = op.create
        criterion.ad_group = ag_resource
        criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        criterion.keyword.text = text
        criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum[match_type]
        ops.append(op)
    if dry_run:
        print(f"      [DRY RUN] Would add {len(ops)} keywords")
        return
    ag_criterion_service.mutate_ad_group_criteria(customer_id=customer_id, operations=ops)

def create_negative_keywords(client, customer_id, campaign_resource, keywords, dry_run):
    if not keywords:
        return
    campaign_criterion_service = client.get_service("CampaignCriterionService")
    ops = []
    for text in keywords:
        op = client.get_type("CampaignCriterionOperation")
        criterion = op.create
        criterion.campaign = campaign_resource
        criterion.negative = True
        criterion.keyword.text = text
        criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum.BROAD
        ops.append(op)
    if dry_run:
        print(f"    [DRY RUN] Would add {len(ops)} campaign negative keywords")
        return
    campaign_criterion_service.mutate_campaign_criteria(customer_id=customer_id, operations=ops)

def create_rsa(client, customer_id, ag_resource, rsa_data, dry_run):
    ad_service = client.get_service("AdGroupAdService")
    op = client.get_type("AdGroupAdOperation")
    ad_group_ad = op.create
    ad_group_ad.ad_group = ag_resource
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED

    ad = ad_group_ad.ad
    ad.final_urls.append(rsa_data["final_url"])
    ad.responsive_search_ad.path1 = rsa_data["path1"]
    ad.responsive_search_ad.path2 = rsa_data["path2"]

    for i, text in enumerate(rsa_data["headlines"]):
        asset = client.get_type("AdTextAsset")
        asset.text = text
        if rsa_data.get("pin_h1") and i == 0:
            asset.pinned_field = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1
        ad.responsive_search_ad.headlines.append(asset)

    for text in rsa_data["descriptions"]:
        asset = client.get_type("AdTextAsset")
        asset.text = text
        ad.responsive_search_ad.descriptions.append(asset)

    if dry_run:
        print(f"    [DRY RUN] Would create RSA for {rsa_data['ad_group']}")
        return
    ad_service.mutate_ad_group_ads(customer_id=customer_id, operations=[op])

# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Create Snoots Vet Google Ads campaigns")
    parser.add_argument("--customer-id", required=True,
                        help="Google Ads customer ID (with or without dashes)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would be created without making API calls")
    parser.add_argument("--config", default=None,
                        help="Path to google-ads.yaml (default: ~/.config/google-ads.yaml or ./google-ads.yaml)")
    args = parser.parse_args()

    customer_id = args.customer_id.replace("-", "")
    dry_run = args.dry_run

    if dry_run:
        print("=== DRY RUN MODE — no changes will be made ===\n")
        client = None
    else:
        client = GoogleAdsClient.load_from_storage(args.config)

    # Index ad groups and RSAs by name for lookup
    ag_by_campaign = {}  # campaign_name -> [(ag_name, cpc_micros)]
    for camp, ag, cpc in AD_GROUPS:
        ag_by_campaign.setdefault(camp, []).append((ag, cpc))

    kw_by_ag = {}  # ag_name -> [(text, match_type)]
    for ag, text, match_type in KEYWORDS:
        kw_by_ag.setdefault(ag, []).append((text, match_type))

    rsa_by_ag = {}  # ag_name -> rsa_data
    for rsa_data in RSA_DATA:
        rsa_by_ag[rsa_data["ad_group"]] = rsa_data

    campaign_resources = {}
    ag_resources = {}

    print(f"Creating campaigns for customer {customer_id}...\n")

    for camp_name, budget_micros in CAMPAIGNS:
        print(f"Campaign: {camp_name}")

        budget_resource = create_budget(client, customer_id, camp_name, budget_micros, dry_run)
        camp_resource = create_campaign(client, customer_id, camp_name, budget_resource, dry_run)
        campaign_resources[camp_name] = camp_resource

        # Campaign-level negative keywords
        if camp_name == "Search_Brand_Snoots_MaxConv":
            create_negative_keywords(client, customer_id, camp_resource, BRAND_NEGATIVES, dry_run)
        elif camp_name in NB_CAMPAIGNS:
            create_negative_keywords(client, customer_id, camp_resource, NB_NEGATIVES, dry_run)

        # Ad groups
        for ag_name, cpc_micros in ag_by_campaign.get(camp_name, []):
            print(f"  Ad Group: {ag_name}")
            ag_resource = create_ad_group(client, customer_id, camp_resource, ag_name, cpc_micros, dry_run)
            ag_resources[ag_name] = ag_resource

            # Keywords
            kws = kw_by_ag.get(ag_name, [])
            if kws:
                create_keywords(client, customer_id, ag_resource, kws, dry_run)
                if dry_run:
                    pass  # already printed inside
                else:
                    print(f"    Added {len(kws)} keywords")

            # RSA
            if ag_name in rsa_by_ag:
                create_rsa(client, customer_id, ag_resource, rsa_by_ag[ag_name], dry_run)
                if not dry_run:
                    print(f"    Added RSA")

        print()

    print("Done!")
    if dry_run:
        print("\nRe-run without --dry-run to create everything in Google Ads.")

if __name__ == "__main__":
    try:
        main()
    except GoogleAdsException as ex:
        print(f"Google Ads API error:")
        for error in ex.failure.errors:
            print(f"  {error.message}")
        sys.exit(1)
