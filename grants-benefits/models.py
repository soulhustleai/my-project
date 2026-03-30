"""
Grants & Benefits Automation System — Data Models
"""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class ProgramCategory(str, Enum):
    BUSINESS_GRANT = "business_grants"
    PERSONAL_GRANT = "personal_grants"
    HOUSING = "housing_assistance"
    ENERGY = "energy_assistance"
    FOOD = "food_assistance"
    HEALTHCARE = "healthcare"
    EDUCATION = "education_training"
    TAX_CREDIT = "tax_credits"
    TECHNOLOGY = "technology_assistance"
    UNCLAIMED = "unclaimed_funds"
    EMERGENCY = "emergency_assistance"
    VETERAN = "veteran_benefits"
    DISABILITY = "disability_benefits"
    CHILDCARE = "childcare_assistance"
    TRANSPORTATION = "transportation_assistance"


class OpportunityStatus(str, Enum):
    DISCOVERED = "discovered"
    SCREENING = "screening"
    ELIGIBLE = "eligible"
    NOT_ELIGIBLE = "not_eligible"
    QUEUED = "queued"
    APPLYING = "applying"
    SUBMITTED = "submitted"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    DENIED = "denied"
    RECEIVED = "received"
    EXPIRED = "expired"


class ApplicationStatus(str, Enum):
    DRAFT = "draft"
    READY = "ready"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    ADDITIONAL_INFO_NEEDED = "additional_info_needed"
    APPROVED = "approved"
    DENIED = "denied"
    WITHDRAWN = "withdrawn"


@dataclass
class UserProfile:
    """The applicant's profile for eligibility matching."""
    full_name: str = ""
    email: str = ""
    phone: str = ""
    date_of_birth: str = ""
    ssn_last4: str = ""  # Only last 4, never store full SSN

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
    is_head_of_household: bool = True
    dependents: int = 0
    marital_status: str = "single"  # single, married, divorced, widowed

    # Demographics
    age: int = 0
    gender: str = ""
    race_ethnicity: str = ""
    is_veteran: bool = False
    is_disabled: bool = False
    citizenship_status: str = "us_citizen"  # us_citizen, permanent_resident, other

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
    is_disadvantaged: bool = False
    sam_registered: bool = False
    duns_number: str = ""
    cage_code: str = ""

    # Housing
    current_housing: str = "renting"  # renting, owning, homeless, other
    monthly_rent: float = 0.0
    is_first_time_homebuyer: bool = True
    desired_home_price: float = 300000.0

    # Education
    education_level: str = ""  # high_school, associates, bachelors, masters, doctorate
    is_student: bool = False

    # Employment
    employment_status: str = "self_employed"  # employed, self_employed, unemployed, retired
    employer: str = ""

    # Benefits currently receiving
    current_benefits: list = field(default_factory=list)

    # Credit
    credit_score_range: str = ""  # poor, fair, good, excellent


@dataclass
class Program:
    """A government/nonprofit program that provides benefits."""
    id: str = ""
    name: str = ""
    category: ProgramCategory = ProgramCategory.PERSONAL_GRANT
    subcategory: str = ""
    description: str = ""

    # What you get
    benefit_type: str = ""  # cash, voucher, tax_credit, service, loan, grant
    amount_min: float = 0.0
    amount_max: float = 0.0
    amount_recurring: bool = False  # monthly benefit vs one-time
    amount_description: str = ""

    # Who provides it
    agency: str = ""
    agency_level: str = ""  # federal, state, county, city, nonprofit
    website: str = ""
    application_url: str = ""
    phone: str = ""

    # Eligibility
    income_limit_percent_fpl: float = 0.0  # % of Federal Poverty Level
    income_limit_dollar: float = 0.0
    state_specific: str = ""  # empty = all states
    requires_us_citizen: bool = False
    requires_business: bool = False
    requires_veteran: bool = False
    requires_disabled: bool = False
    min_age: int = 0
    max_age: int = 999
    other_requirements: str = ""

    # Application
    application_method: str = ""  # online, mail, in_person, phone
    application_complexity: str = "medium"  # simple, medium, complex
    estimated_processing_days: int = 30
    deadline: Optional[str] = None
    rolling_applications: bool = True
    documents_needed: list = field(default_factory=list)

    # Metadata
    last_verified: str = ""
    source_url: str = ""
    notes: str = ""


@dataclass
class Opportunity:
    """A matched program opportunity for the user."""
    id: str = ""
    program_id: str = ""
    program_name: str = ""
    category: str = ""
    status: OpportunityStatus = OpportunityStatus.DISCOVERED

    # Scoring
    score: float = 0.0
    amount_score: float = 0.0
    likelihood_score: float = 0.0
    effort_score: float = 0.0
    speed_score: float = 0.0

    # Estimated value
    estimated_value: float = 0.0
    estimated_annual_value: float = 0.0

    # Application tracking
    application_status: ApplicationStatus = ApplicationStatus.DRAFT
    applied_date: Optional[str] = None
    deadline: Optional[str] = None
    follow_up_date: Optional[str] = None
    decision_date: Optional[str] = None

    # Notes
    eligibility_notes: str = ""
    action_items: list = field(default_factory=list)
    documents_needed: list = field(default_factory=list)

    # Timestamps
    discovered_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
