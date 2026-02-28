from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class ResearchReport(BaseModel):
    report_id: str
    title: str
    date: datetime
    author: str
    report_type: str
    source_url: str
    attachment_urls: List[str] = []
    normalized_text: str = ""
    tags: List[str] = []
    asset_class_tags: List[str] = []
    region_tags: List[str] = []
    sector_tags: List[str] = []
    company_tags: List[str] = []
    time_horizon: str = ""
    risk_conditions: str = ""

class SmartMoneyVideo(BaseModel):
    video_id: str
    title: str
    publish_date: datetime
    source_url: str
    series_name: str = ""
    duration: str = ""
    description: str = ""
    transcript_or_summary: str = ""
    tags: List[str] = []
    asset_class_tags: List[str] = []
    region_tags: List[str] = []
    sector_tags: List[str] = []
    company_tags: List[str] = []
    education_level: str = "" # beginner, intermediate, advanced
    content_style: str = "" # urgent market, analytical, thematic, educational, narrative 
    recommended_routine: str = ""

class HybridContentBundle(BaseModel):
    bundle_id: str
    routine_type: str # A, B, C, D
    report_id: Optional[str] = None
    video_id: Optional[str] = None
    match_reason: str = ""
    target_segments: List[str] = []
    pb_summary: str = ""
    client_summary: str = ""
    recommended_cta: str = ""
    urgency: str = ""
    confidence: str = ""
    compliance_notes: str = ""

class CustomerProfile(BaseModel):
    customer_id: str
    asset_tier: str
    trading_frequency: str
    risk_profile: str = ""
    portfolio_style: str = ""
    account_types: List[str] = []
    sector_exposures: List[str] = []
    geographic_exposures: List[str] = []
    cash_ratio: float = 0.0
    concentration_flags: List[str] = []
    engagement_level: str = ""
    media_preference: str = ""
    segment_id: str # S1, S2, S3, S4
    modifiers: List[str] = []

class PBActionDraft(BaseModel):
    action_id: str
    customer_id: str
    bundle_id: str
    routine_type: str
    outreach_channel: str = ""
    pb_talking_points: str = ""
    client_message_draft: str = ""
    follow_up_priority: int = 0
    traceability: str = ""
    review_required: bool = True

class AuditRecord(BaseModel):
    audit_id: str
    timestamp: datetime
    report_id: Optional[str] = None
    video_id: Optional[str] = None
    customer_id: Optional[str] = None
    workflow_name: str
    decision_points: Dict = {}
    generated_outputs: Dict = {}
    rationale: str = ""
    human_review_status: str = "pending"
