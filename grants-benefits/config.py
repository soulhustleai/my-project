"""
Grants & Benefits Automation System — Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()


# === API Keys ===
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM = os.getenv("TWILIO_FROM_NUMBER", "+18446439825")
MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL", "")

# === User Profile Defaults ===
USER_STATE = os.getenv("USER_STATE", "FL")
USER_COUNTY = os.getenv("USER_COUNTY", "Broward")
USER_ZIP = os.getenv("USER_ZIP", "33301")

# === Scoring Weights ===
SCORE_WEIGHT_AMOUNT = 0.30        # How much money is available
SCORE_WEIGHT_LIKELIHOOD = 0.35    # How likely to qualify
SCORE_WEIGHT_EFFORT = 0.20        # How easy to apply
SCORE_WEIGHT_SPEED = 0.15         # How fast to receive funds

# === Thresholds ===
MIN_SCORE_TO_APPLY = 40           # Minimum score to auto-queue for application
MIN_SCORE_TO_NOTIFY = 25          # Minimum score to notify Edwin

# === Scan Intervals ===
GRANTS_SCAN_INTERVAL_HOURS = 24   # How often to scan grants.gov
BENEFITS_SCAN_INTERVAL_HOURS = 168  # Weekly benefits re-screen
HOUSING_SCAN_INTERVAL_HOURS = 72  # Every 3 days for housing

# === Claude AI Config ===
CLAUDE_MODEL = "claude-sonnet-4-20250514"
CLAUDE_MAX_TOKENS = 4096

# === Data Sources ===
GRANTS_GOV_API_BASE = "https://www.grants.gov/grantsws/rest"
GRANTS_GOV_SEARCH_URL = "https://www.grants.gov/grantsws/rest/opportunities/search/"
SAM_GOV_API_BASE = "https://api.sam.gov/opportunities/v2"
USA_SPENDING_API = "https://api.usaspending.gov/api/v2"
HUD_API_BASE = "https://www.huduser.gov/hudapi/public"
BENEFITS_GOV_URL = "https://www.benefits.gov"

# === Program Categories ===
PROGRAM_CATEGORIES = [
    "business_grants",
    "personal_grants",
    "housing_assistance",
    "energy_assistance",
    "food_assistance",
    "healthcare",
    "education_training",
    "tax_credits",
    "technology_assistance",
    "unclaimed_funds",
    "emergency_assistance",
    "veteran_benefits",
    "disability_benefits",
    "childcare_assistance",
    "transportation_assistance",
]
