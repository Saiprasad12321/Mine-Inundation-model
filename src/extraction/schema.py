"""Pydantic data models for the Mine Inundation Intelligence System."""
from typing import List, Optional
from pydantic import BaseModel, Field

class PersonCasualty(BaseModel):
    name: Optional[str] = None
    designation: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None

class InundationIncident(BaseModel):
    incident_id: str = Field(..., description="Unique Incident Identifier")
    source_pdf: str = Field(..., description="Source PDF filename")
    pdf_page: int = Field(..., description="1-based PDF document page number")
    pdf_page_end: Optional[int] = Field(None, description="Ending page number if spans multiple pages")
    printed_page: Optional[int] = Field(None, description="Printed page number from original publication")
    report_type: str = Field(..., description="Detailed Fatal Accident Report, Major Accident Since 1901, or Court of Inquiry")
    report_title: str = Field(..., description="Report title or case headline")
    accident_date: Optional[str] = Field(None, description="Date in YYYY-MM-DD or original format")
    accident_time: Optional[str] = Field(None, description="Time of accident if recorded")
    mine_name: str = Field(..., description="Name of the mine")
    owner: Optional[str] = Field(None, description="Owner / Company operating the mine")
    district: Optional[str] = Field(None, description="District where mine is situated")
    state: Optional[str] = Field(None, description="State where mine is situated")
    mine_type: Optional[str] = Field(None, description="Belowground, Opencast, or Above Ground")
    mineral: str = Field(..., description="Coal, Non-Coal (e.g. Uranium, Stone, Limestone, Mica)")
    dgms_code: Optional[str] = Field(None, description="DGMS Cause code, e.g. 0991 (Irruption of water)")
    dgms_cause_category: Optional[str] = Field(None, description="DGMS standard cause category name")
    
    fatalities: int = Field(0, description="Total confirmed fatalities")
    serious_injuries: int = Field(0, description="Total serious injuries reported")
    persons_killed_details: List[str] = Field(default_factory=list, description="Verbatim names and designations of deceased")
    
    incident_description: str = Field(..., description="Detailed narrative of what transpired")
    inundation_source: Optional[str] = Field(None, description="Physical origin of water/slurry (e.g. Old workings, jore, stowing)")
    inundation_mechanism: Optional[str] = Field(None, description="Physical ingress mechanism (barrier failure, dam collapse, puncture)")
    direct_cause: Optional[str] = Field(None, description="Immediate cause of death or catastrophe")
    root_cause: Optional[str] = Field(None, description="Underlying engineering, supervisory, or organizational root cause")
    contributing_factors: List[str] = Field(default_factory=list, description="Geological, weather, or human contributing factors")
    geological_hydrological_conditions: Optional[str] = Field(None, description="Strata, hydrostatic head, water bodies, or rainfall conditions")
    warning_signs_monitoring_failures: Optional[str] = Field(None, description="Pre-accident warning indicators or lack of monitoring")
    safety_precautions_equipment: Optional[str] = Field(None, description="Dams, stoppings, pumps, PPE, or barricades involved")
    
    property_damage_operational_consequences: Optional[str] = Field(None, description="Consequences to mine workings, flooding, or equipment loss")
    official_investigation_findings: Optional[str] = Field(None, description="Verbatim DGMS findings ('Had...' paras)")
    statutory_violations: List[str] = Field(default_factory=list, description="Specific CMR/MMR regulations or Mines Act sections contravened")
    officially_recommended_corrective_actions: Optional[str] = Field(None, description="Statutory or court recommendations")
    ai_preventive_suggestions: List[str] = Field(default_factory=list, description="Engineered preventive suggestions")
    
    supporting_source_passages: str = Field(..., description="Exact quoted evidence from source PDF")
    confidence_score: float = Field(..., description="Automated classification confidence (0.0 to 1.0)")
    verification_status: str = Field(..., description="Verified Inundation | Related Water Incident | Unverified / Ambiguous")
    is_verified_inundation: bool = Field(..., description="True if primary inundation inrush event")
    duplicate_of: Optional[str] = Field(None, description="Incident ID of primary record if duplicate reference")
    review_notes: Optional[str] = Field(None, description="Auditor review notes and rationale")
