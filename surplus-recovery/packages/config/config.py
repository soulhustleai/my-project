"""
Configuration module — loads environment variables and provides typed access.
"""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    # Supabase
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_SERVICE_KEY", "")

    # Anthropic (Claude API)
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    claude_model_parse: str = os.getenv("CLAUDE_MODEL_PARSE", "claude-haiku-4-5-20251001")
    claude_model_complex: str = os.getenv("CLAUDE_MODEL_COMPLEX", "claude-sonnet-4-6")

    # Lob (Direct Mail)
    lob_api_key: str = os.getenv("LOB_API_KEY", "")
    lob_test_mode: bool = os.getenv("LOB_TEST_MODE", "true").lower() == "true"

    # Twilio (SMS)
    twilio_account_sid: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    twilio_auth_token: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    twilio_phone_number: str = os.getenv("TWILIO_PHONE_NUMBER", "")

    # People Data Labs (Enrichment)
    pdl_api_key: str = os.getenv("PDL_API_KEY", "")

    # Business Info
    business_name: str = os.getenv("BUSINESS_NAME", "")
    business_phone: str = os.getenv("BUSINESS_PHONE", "")
    business_email: str = os.getenv("BUSINESS_EMAIL", "")
    business_address: str = os.getenv("BUSINESS_ADDRESS", "")
    business_website: str = os.getenv("BUSINESS_WEBSITE", "")

    # Scoring thresholds
    min_surplus_amount: float = float(os.getenv("MIN_SURPLUS_AMOUNT", "1000"))
    min_score_to_enrich: float = float(os.getenv("MIN_SCORE_TO_ENRICH", "20"))
    min_surplus_for_phone: float = float(os.getenv("MIN_SURPLUS_FOR_PHONE", "10000"))

    # Enrichment
    max_enrichments_per_day: int = int(os.getenv("MAX_ENRICHMENTS_PER_DAY", "100"))

    # Sentry
    sentry_dsn: str = os.getenv("SENTRY_DSN", "")


config = Config()
