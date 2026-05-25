from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from app.schemas.decision import DecisionGrade
from app.schemas.evaluation import FinalEvaluationResponse


class TransferContext(BaseModel):
    source_region: Optional[str] = None
    target_region: Optional[str] = None
    source_country: Optional[str] = None
    target_country: Optional[str] = None

    data_subject_region: Optional[str] = None
    recipient_role: Optional[str] = None
    recipient_country: Optional[str] = None
    recipient_establishment_country: Optional[str] = None

    recipient_has_target_establishment: Optional[bool] = None
    offers_services_to_target_residents: Optional[bool] = None
    monitors_target_residents: Optional[bool] = None
    target_residents_included: Optional[bool] = None

    onward_transfer_planned: Optional[bool] = None
    onward_transfer_country: Optional[str] = None

    destination_processing_purpose_defined: Optional[bool] = None
    destination_privacy_notice_ready: Optional[bool] = None
    destination_processor_contract_ready: Optional[bool] = None

    gdpr_eu_data_subjects_included: Optional[bool] = None
    gdpr_eu_establishment_involved: Optional[bool] = None
    gdpr_offers_goods_or_services_to_eu: Optional[bool] = None
    gdpr_monitors_eu_behavior: Optional[bool] = None
    gdpr_processor_contract_ready: Optional[bool] = None
    gdpr_onward_transfer_safeguard_ready: Optional[bool] = None

    pipa_korean_data_subjects_included: Optional[bool] = None
    pipa_services_to_korean_users: Optional[bool] = None
    pipa_effect_on_korean_data_subjects: Optional[bool] = None
    pipa_domestic_agent_or_establishment: Optional[bool] = None
    pipa_cross_border_notice_items_ready: Optional[bool] = None
    pipa_privacy_policy_disclosure_ready: Optional[bool] = None

    pdpl_saudi_data_subjects_included: Optional[bool] = None
    pdpl_saudi_controller_or_processor_involved: Optional[bool] = None
    pdpl_sensitive_or_special_data: Optional[bool] = None
    pdpl_transfer_regulation_safeguards_ready: Optional[bool] = None
    pdpl_scc_or_adequacy_ready: Optional[bool] = None
    pdpl_onward_transfer_planned: Optional[bool] = None

    lgpd_brazil_data_subjects_included: Optional[bool] = None
    lgpd_data_collected_in_brazil: Optional[bool] = None
    lgpd_services_to_brazil_residents: Optional[bool] = None
    lgpd_international_transfer_mechanism_ready: Optional[bool] = None
    lgpd_data_subject_rights_process_ready: Optional[bool] = None

    taiwan_data_subjects_included: Optional[bool] = None
    taiwan_recipient_processing_in_taiwan: Optional[bool] = None
    taiwan_recipient_country_protection_adequate: Optional[bool] = None
    taiwan_circumvention_transfer_risk: Optional[bool] = None
    taiwan_sector_restriction_possible: Optional[bool] = None
    taiwan_security_maintenance_ready: Optional[bool] = None

    target_pack_id: Optional[str] = None
    legal_research_date: Optional[str] = None


class EvaluateTransferRequest(TransferContext):
    aws_data: Dict[str, Any] = Field(default_factory=dict)
    policy_data: Dict[str, Any] = Field(default_factory=dict)
    target_applicability_data: Dict[str, Any] = Field(default_factory=dict)
    source_pack_id: Optional[str] = None
    target_pack_id: Optional[str] = None


class SelectedPackResponse(BaseModel):
    pack_id: str
    evaluation_role: str
    reason: str
    rule_groups: List[str]


class TransferPackResultResponse(BaseModel):
    pack_id: str
    evaluation_role: str
    result: FinalEvaluationResponse


class EvaluateTransferResponse(BaseModel):
    final_decision: DecisionGrade
    summary: str
    source_country: Optional[str]
    target_country: Optional[str]
    selected_packs: List[SelectedPackResponse]
    pack_results: List[TransferPackResultResponse]
    merged_required_actions: List[str]
    merged_legal_basis_articles: List[str]
    global_next_steps: List[str]
