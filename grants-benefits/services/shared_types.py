"""
Grants & Benefits — Shared type definitions and enums.

Follows the same pattern as surplus-recovery/packages/shared_types/types.py
"""
from enum import Enum
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional


# ============================================
# Enums
# ============================================

class ProgramCategory(str, Enum):
    BUSINESS_GRANT = "business_grant"
    PERSONAL_GRANT = "personal_grant"
    HOUSING_ASSISTANCE = "housing_assistance"
    ENERGY_ASSISTANCE = "energy_assistance"
    FOOD_ASSISTANCE = "food_assistance"
    HEALTHCARE = "healthcare"
    EDUCATION_TRAINING = "education_training"
    TAX_CREDIT = "tax_credit"
    TECHNOLOGY_ASSISTANCE = "technology_assistance"
    UNCLAIMED_FUNDS = "unclaimed_funds"
    EMERGENCY_ASSISTANCE = "emergency_assistance"
    VETERAN_BENEFITS = "veteran_benefits"
    CHILDCARE_ASSISTANCE = "childcare_assistance"
    TRANSPORTATION = "transportation"
    CASH_ASSISTANCE = "cash_assistance"
    LOAN_PROGRAM = "loan_program"


class BenefitType(str, Enum):
    GRANT = "grant"
    VOUCHER = "voucher"
    TAX_CREDIT = "tax_credit"
    SERVICE = "service"
    LOAN = "loan"
    REBATE = "rebate"
    DISCOUNT = "discount"
    CASH = "cash"
    IN_KIND = "in_kind"


class ApplicationMethod(str, Enum):
    ONLINE = "online"
    MAIL = "mail"
    IN_PERSON = "in_person"
    PHONE = "phone"
    MIXED = "mixed"


class ApplicationComplexity(str, Enum):
    SIMPLE = "simple"      # < 30 min, basic info
    MEDIUM = "medium"      # 30-60 min, some docs needed
    COMPLEX = "complex"    # 1+ hrs, multiple docs, interviews


class AgencyLevel(str, Enum):
    FEDERAL = "federal"
    STATE = "state"
    COUNTY = "county"
    CITY = "city"
    NONPROFIT = "nonprofit"
    PRIVATE = "private"


class OpportunityStatus(str, Enum):
    DISCOVERED = "discovered"
    SCREENING = "screening"
    ELIGIBLE = "eligible"
    NOT_ELIGIBLE = "not_eligible"
    QUEUED_TO_APPLY = "queued_to_apply"
    APPLYING = "applying"
    SUBMITTED = "submitted"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    DENIED = "denied"
    RECEIVED = "received"
    EXPIRED = "expired"
    NEEDS_INFO = "needs_info"
    SKIPPED = "skipped"


class ScanSource(str, Enum):
    GRANTS_GOV = "grants_gov"
    SAM_GOV = "sam_gov"
    SBA = "sba"
    HUD = "hud"
    USDA = "usda"
    BENEFITS_GOV = "benefits_gov"
    STATE_PORTAL = "state_portal"
    COUNTY_PORTAL = "county_portal"
    NONPROFIT_DB = "nonprofit_db"
    MANUAL = "manual"
    CLAUDE_RESEARCH = "claude_research"


# ============================================
# Data Classes
# ============================================

@dataclass
class Program:
    """A government/nonprofit program that provides benefits."""
    id: str
    name: str
    category: ProgramCategory
    benefit_type: BenefitType
    description: str

    # What you get
    amount_min: float = 0.0
    amount_max: float = 0.0
    amount_recurring: bool = False
    amount_frequency: str = ""  # monthly, annual, one_time
    amount_description: str = ""

    # Provider
    agency: str = ""
    agency_level: AgencyLevel = AgencyLevel.FEDERAL
    website: str = ""
    application_url: str = ""
    phone: str = ""

    # Eligibility
    income_limit_fpl_percent: float = 0.0  # 0 = no limit
    income_limit_dollar: float = 0.0
    income_limit_ami_percent: float = 0.0  # Area Median Income
    state_specific: str = ""  # empty = nationwide
    requires_us_citizen: bool = False
    requires_business: bool = False
    requires_veteran: bool = False
    requires_disabled: bool = False
    requires_first_time_homebuyer: bool = False
    min_age: int = 0
    max_age: int = 999
    max_employees: int = 0  # 0 = no limit
    other_requirements: list = field(default_factory=list)

    # Application
    application_method: ApplicationMethod = ApplicationMethod.ONLINE
    application_complexity: ApplicationComplexity = ApplicationComplexity.MEDIUM
    estimated_processing_days: int = 30
    deadline: Optional[str] = None
    rolling_applications: bool = True
    documents_needed: list = field(default_factory=list)

    # Metadata
    source: ScanSource = ScanSource.MANUAL
    last_verified: str = ""
    notes: str = ""
    tags: list = field(default_factory=list)
    is_active: bool = True


@dataclass
class UserProfile:
    """The applicant's complete profile for eligibility matching."""
    # Identity
    full_name: str = ""
    email: str = ""
    phone: str = ""
    date_of_birth: str = ""

    # Location
    address: str = ""
    city: str = ""
    state: str = "FL"
    zip_code: str = ""
    county: str = ""

    # Household
    household_size: int = 1
    annual_income: float = 0.0
    monthly_income: float = 0.0
    dependents: int = 0
    marital_status: str = "single"

    # Demographics
    age: int = 0
    is_veteran: bool = False
    is_disabled: bool = False
    citizenship_status: str = "us_citizen"

    # Business
    has_business: bool = True
    business_name: str = "Typically Not Lifestyle LLC"
    business_type: str = "LLC"
    business_ein: str = ""
    business_state: str = "FL"
    business_industry: str = "technology_services"
    business_revenue_annual: float = 0.0
    business_employees: int = 1
    business_years: float = 1.0
    is_minority_owned: bool = False
    is_woman_owned: bool = False
    is_veteran_owned: bool = False
    sam_registered: bool = False

    # Housing
    current_housing: str = "renting"
    monthly_rent: float = 0.0
    is_first_time_homebuyer: bool = True
    desired_home_price: float = 300000.0

    # Education & Employment
    education_level: str = ""
    employment_status: str = "self_employed"

    # Current benefits
    current_benefits: list = field(default_factory=list)
    credit_score_range: str = ""  # poor, fair, good, excellent


@dataclass
class ScoredOpportunity:
    """A matched program with its priority score breakdown."""
    program_id: str
    total_score: float
    amount_score: float
    likelihood_score: float
    effort_score: float
    speed_score: float
    estimated_annual_value: float
    eligibility_notes: str = ""
    action_items: list = field(default_factory=list)
