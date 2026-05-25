from typing import Any, Dict, List

from app.core.constants import EU_EEA_COUNTRIES
from app.services.derived_fields import country_to_pack_id


SOURCE_OUTBOUND_GROUPS = [
    "outbound_transfer",
    "security_baseline",
    "processor_governance",
    "sensitive_data",
    "transparency_notice",
]

DOMESTIC_GROUPS = [
    "domestic_processing",
    "security_baseline",
    "processor_governance",
    "sensitive_data",
    "transparency_notice",
]

TARGET_GROUPS = [
    "target_processing",
    "extraterritorial_scope",
    "processor_governance",
    "onward_transfer",
    "sensitive_data",
    "transparency_notice",
]

TARGET_GROUPS_BY_PACK = {
    "gdpr": [
        "extraterritorial_scope",
        "target_processor_governance",
        "target_onward_transfer",
        "target_transparency",
        "target_sensitive_data",
    ],
    "korea_pipa": [
        "extraterritorial_scope",
        "target_processor_governance",
        "target_onward_transfer",
        "target_transparency",
        "domestic_agent",
    ],
    "saudi_pdpl": [
        "target_processing",
        "target_sensitive_data",
        "target_processor_governance",
        "target_onward_transfer",
        "risk_assessment",
        "transfer_safeguards",
    ],
    "lgpd": [
        "extraterritorial_scope",
        "international_transfer",
        "target_onward_transfer",
        "target_transparency",
    ],
    "taiwan": [
        "target_processing",
        "target_security_baseline",
        "target_onward_transfer",
        "authority_restriction_review",
        "recipient_country_protection",
    ],
}

TARGET_CORE_FIELDS = [
    "recipient_has_target_establishment",
    "target_residents_included",
    "recipient_role",
    "onward_transfer_planned",
]

TARGET_FIELDS_BY_PACK = {
    "gdpr": [
        "gdpr_eu_data_subjects_included",
        "gdpr_eu_establishment_involved",
        "gdpr_offers_goods_or_services_to_eu",
        "gdpr_monitors_eu_behavior",
        "gdpr_processor_contract_ready",
        "gdpr_onward_transfer_safeguard_ready",
    ],
    "korea_pipa": [
        "pipa_korean_data_subjects_included",
        "pipa_services_to_korean_users",
        "pipa_effect_on_korean_data_subjects",
        "pipa_domestic_agent_or_establishment",
        "pipa_cross_border_notice_items_ready",
        "pipa_privacy_policy_disclosure_ready",
    ],
    "saudi_pdpl": [
        "pdpl_saudi_data_subjects_included",
        "pdpl_saudi_controller_or_processor_involved",
        "pdpl_sensitive_or_special_data",
        "pdpl_transfer_regulation_safeguards_ready",
        "pdpl_scc_or_adequacy_ready",
        "pdpl_onward_transfer_planned",
    ],
    "lgpd": [
        "lgpd_brazil_data_subjects_included",
        "lgpd_data_collected_in_brazil",
        "lgpd_services_to_brazil_residents",
        "lgpd_international_transfer_mechanism_ready",
        "lgpd_data_subject_rights_process_ready",
    ],
    "taiwan": [
        "taiwan_data_subjects_included",
        "taiwan_recipient_processing_in_taiwan",
        "taiwan_recipient_country_protection_adequate",
        "taiwan_circumvention_transfer_risk",
        "taiwan_sector_restriction_possible",
        "taiwan_security_maintenance_ready",
    ],
}


def describe_pack_reason(pack_id: str, country: str | None, role: str) -> str:
    label = {
        "gdpr": "EU/EEA GDPR",
        "korea_pipa": "Korea PIPA",
        "saudi_pdpl": "Saudi PDPL",
        "lgpd": "Brazil LGPD",
        "taiwan": "Taiwan PDPA",
    }.get(pack_id, pack_id)

    if role == "source_required":
        return f"Source country {country or 'unknown'} maps to {label}; outbound transfer or domestic baseline review is required."
    if role == "target_conditional_candidate":
        return f"Target country {country or 'unknown'} maps to {label}, but key applicability answers are unknown, so legal review is required."
    if role == "manual_override":
        return f"{label} was selected by manual override."
    return f"Target country {country or 'unknown'} maps to {label}; target processing, scope, or onward-transfer applicability should be checked."


def target_rule_groups_for_pack(pack_id: str) -> List[str]:
    return TARGET_GROUPS_BY_PACK.get(pack_id, TARGET_GROUPS)


def target_conditions_present(context: Dict[str, Any], target_pack_id: str | None = None) -> bool:
    pack_specific_true = False
    if target_pack_id:
        pack_specific_true = any(
            context.get(field) is True
            for field in TARGET_FIELDS_BY_PACK.get(target_pack_id, [])
        )

    return any(
        (
            pack_specific_true,
            context.get("recipient_has_target_establishment") is True,
            context.get("target_residents_included") is True,
            context.get("offers_services_to_target_residents") is True,
            context.get("monitors_target_residents") is True,
            context.get("onward_transfer_planned") is True,
            context.get("contains_sensitive_data") is True,
            context.get("data_subject_region")
            in {
                context.get("target_country"),
                "EU" if context.get("target_country") in EU_EEA_COUNTRIES else None,
                "EEA" if context.get("target_country") in EU_EEA_COUNTRIES else None,
            },
        )
    )


def target_answers_ambiguous(context: Dict[str, Any], target_pack_id: str | None = None) -> bool:
    fields = list(TARGET_CORE_FIELDS)
    if target_pack_id:
        fields.extend(TARGET_FIELDS_BY_PACK.get(target_pack_id, []))
    return any(context.get(field) is None for field in fields)


def select_applicable_packs(context: Dict[str, Any]) -> List[Dict[str, Any]]:
    source_country = context.get("source_country")
    target_country = context.get("target_country")
    source_pack_id = context.get("source_pack_id") or country_to_pack_id(source_country)
    target_pack_id = context.get("target_pack_id") or country_to_pack_id(target_country)
    source_override = context.get("source_pack_id_override") is True
    target_override = context.get("target_pack_id_override") is True
    same_country = (
        source_country is not None
        and target_country is not None
        and source_country == target_country
    )
    same_legal_pack = (
        source_pack_id is not None
        and target_pack_id is not None
        and source_pack_id == target_pack_id
    )

    selected: List[Dict[str, Any]] = []
    seen: set[str] = set()

    if source_pack_id:
        source_groups = DOMESTIC_GROUPS if same_country or same_legal_pack else SOURCE_OUTBOUND_GROUPS
        selected.append(
            {
                "pack_id": source_pack_id,
                "evaluation_role": "manual_override"
                if source_override
                else "source_required",
                "reason": describe_pack_reason(
                    source_pack_id,
                    source_country,
                    "manual_override" if source_override else "source_required",
                ),
                "rule_groups": source_groups,
            }
        )
        seen.add(source_pack_id)

    if not target_pack_id or target_pack_id in seen:
        return selected

    if target_override:
        selected.append(
            {
                "pack_id": target_pack_id,
                "evaluation_role": "manual_override",
                "reason": describe_pack_reason(
                    target_pack_id,
                    target_country,
                    "manual_override",
                ),
                "rule_groups": target_rule_groups_for_pack(target_pack_id),
            }
        )
        return selected

    if target_conditions_present(context, target_pack_id):
        selected.append(
            {
                "pack_id": target_pack_id,
                "evaluation_role": "target_conditional",
                "reason": describe_pack_reason(
                    target_pack_id,
                    target_country,
                    "target_conditional",
                ),
                "rule_groups": target_rule_groups_for_pack(target_pack_id),
            }
        )
    elif target_answers_ambiguous(context, target_pack_id):
        selected.append(
            {
                "pack_id": target_pack_id,
                "evaluation_role": "target_conditional_candidate",
                "reason": describe_pack_reason(
                    target_pack_id,
                    target_country,
                    "target_conditional_candidate",
                ),
                "rule_groups": target_rule_groups_for_pack(target_pack_id),
            }
        )

    return selected
