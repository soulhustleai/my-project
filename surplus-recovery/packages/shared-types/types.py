"""
Shared type definitions and enums for the surplus recovery system.
"""
from enum import Enum
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


# ============================================
# Enums
# ============================================

class SourceType(str, Enum):
    FORECLOSURE_SURPLUS = "foreclosure_surplus"
    TAX_DEED_OVERAGE = "tax_deed_overage"
    OTHER = "other"


class DataFormat(str, Enum):
    PDF = "pdf"
    HTML_TABLE = "html_table"
    CSV = "csv"
    PORTAL_SEARCH = "portal_search"


class OpportunityStatus(str, Enum):
    NEW = "new"
    QUALIFIED = "qualified"
    ENRICHING = "enriching"
    CONTACTABLE = "contactable"
    OUTREACH_ACTIVE = "outreach_active"
    RESPONDED = "responded"
    INTERESTED = "interested"
    INTAKE_PENDING = "intake_pending"
    SIGNED = "signed"
    DISQUALIFIED = "disqualified"
    ENRICHMENT_FAILED = "enrichment_failed"
    UNRESPONSIVE = "unresponsive"
    DECLINED = "declined"
    DO_NOT_CONTACT = "do_not_contact"


class CaseStatus(str, Enum):
    SIGNED = "signed"
    DOCS_COLLECTING = "docs_collecting"
    DOCS_COMPLETE = "docs_complete"
    CLAIM_PREP = "claim_prep"
    READY_TO_FILE = "ready_to_file"
    FILED = "filed"
    ACKNOWLEDGED = "acknowledged"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    DISBURSEMENT_PENDING = "disbursement_pending"
    DISBURSED = "disbursed"
    FEE_COLLECTED = "fee_collected"
    CLIENT_PAID = "client_paid"
    CLOSED = "closed"
    DENIED = "denied"
    APPEAL = "appeal"
    STALLED = "stalled"
    ESCALATED = "escalated"


class OutreachChannel(str, Enum):
    MAIL = "mail"
    SMS = "sms"
    EMAIL = "email"
    PHONE = "phone"


class OutreachDirection(str, Enum):
    OUTBOUND = "outbound"
    INBOUND = "inbound"


class NotificationPriority(str, Enum):
    P1_URGENT = "p1_urgent"
    P2_ACTION = "p2_action"
    P3_REVIEW = "p3_review"
    P4_INFO = "p4_info"


class NotificationType(str, Enum):
    FOUNDER_ACTION = "founder_action"
    ALERT = "alert"
    INFO = "info"
    ERROR = "error"


class DocumentType(str, Enum):
    AGREEMENT = "agreement"
    AFFIDAVIT = "affidavit"
    ID_COPY = "id_copy"
    CLAIM_FORM = "claim_form"
    COVER_LETTER = "cover_letter"
    POA = "poa"
    W9 = "w9"
    CLAIM_PACKET = "claim_packet"


class EnrichmentSource(str, Enum):
    PDL = "pdl"
    TRUEPEOPLESEARCH = "truepeoplesearch"
    BEENVERIFIED = "beenverified"
    WHITEPAGES = "whitepages"
    MANUAL = "manual"


# ============================================
# Data Classes
# ============================================

@dataclass
class SurplusRecord:
    """A parsed record from a county surplus list."""
    case_number: str
    property_address: Optional[str]
    owner_name: Optional[str]
    surplus_amount: float
    sale_date: Optional[date]
    sale_type: str
    county: str
    state: str
    raw_data: dict


@dataclass
class ScoredOpportunity:
    """An opportunity with its composite score breakdown."""
    opportunity_id: str
    total_score: float
    amount_score: float
    recency_score: float
    identifiability_score: float
    filing_ease_score: float
    competition_score: float


@dataclass
class OutreachStep:
    """A single step in an outreach sequence."""
    step: int
    day: int
    channel: OutreachChannel
    template_id: str
    auto: bool
    requires: Optional[str] = None      # e.g., "email" — only send if claimant has email
    min_amount: Optional[float] = None  # only trigger if surplus >= this amount
