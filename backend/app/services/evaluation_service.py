from typing import Any, Dict, List

from app.core.constants import DEFAULT_DECISION_ORDER
from app.services.condition_evaluator import evaluate_condition_with_trace
from app.services.explanation_service import (
    build_explanation,
    build_next_steps,
    build_summary,
)
from app.services.qualitative_service import build_qualitative_review_hints
from app.services.resolution_service import (
    collect_legal_basis_articles,
    collect_required_actions,
    resolve_final_decision,
)


def build_pack_info(pack_data: Dict[str, Any]) -> Dict[str, str]:
    return {
        "pack_id": pack_data["pack_id"],
        "pack_name": pack_data["pack_name"],
        "jurisdiction": pack_data["jurisdiction"],
        "version": pack_data["version"],
        "description": pack_data["description"],
    }


def build_rule_rationale(rule: Dict[str, Any], matched_facts: List[str]) -> str:
    facts_text = "; ".join(matched_facts)
    explanation_template = rule.get("explanation_template")

    if explanation_template and facts_text:
        return f"{explanation_template} 확인 사실: {facts_text}"

    if facts_text:
        return f"{rule['message']} 확인 사실: {facts_text}"

    return rule["message"]


def sort_triggered_rules(
    triggered_rules: List[Dict[str, Any]],
    decision_order: List[str],
) -> List[Dict[str, Any]]:
    decision_rank = {
        decision: index for index, decision in enumerate(decision_order)
    }
    return sorted(
        triggered_rules,
        key=lambda item: (
            decision_rank.get(item["decision"], len(decision_order)),
            -item.get("priority", 0),
            item["rule_id"],
        ),
    )


def infer_rule_group(rule: Dict[str, Any]) -> str:
    explicit = rule.get("rule_group") or rule.get("scope")
    if explicit:
        return str(explicit)

    category = str(rule.get("category", "")).lower()
    rule_id = str(rule.get("rule_id", "")).lower()

    if any(token in category for token in ("transfer", "allowance_path")):
        if "onward" in category or "subsequent" in category or "onward" in rule_id:
            return "onward_transfer"
        return "outbound_transfer"
    if any(token in category for token in ("security", "incident", "breach")):
        return "security_baseline"
    if any(token in category for token in ("processor", "subprocessor")):
        return "processor_governance"
    if any(token in category for token in ("sensitive", "special_category", "unique_identifier")):
        return "sensitive_data"
    if any(token in category for token in ("transparency", "notice", "rights")):
        return "transparency_notice"
    if any(token in category for token in ("lawfulness", "governance", "accountability", "retention", "minimization")):
        return "domestic_processing"
    if "target" in category or "scope" in category:
        return "extraterritorial_scope"
    return "general"


def filter_rules_for_groups(
    rules: List[Dict[str, Any]],
    active_rule_groups: List[str] | None,
) -> tuple[List[Dict[str, Any]], int]:
    if active_rule_groups is None:
        return rules, 0

    active = set(active_rule_groups)
    filtered = [rule for rule in rules if infer_rule_group(rule) in active]
    return filtered, len(rules) - len(filtered)


def build_input_observations(merged_input: Dict[str, Any]) -> List[str]:
    cross_border_observation = None

    if "transfer_outside_kingdom" in merged_input:
        cross_border_observation = "사우디 기준 국외 이전 여부: " + (
            "예" if merged_input.get("transfer_outside_kingdom") else "아니오"
        )
    elif "transfer_outside_brazil" in merged_input:
        cross_border_observation = "브라질 LGPD 기준 국제이전 여부: " + (
            "예" if merged_input.get("transfer_outside_brazil") else "아니오"
        )
    elif "transfer_outside_korea" in merged_input:
        cross_border_observation = "한국 PIPA 기준 국외이전 여부: " + (
            "예" if merged_input.get("transfer_outside_korea") else "아니오"
        )
    elif "transfer_outside_taiwan" in merged_input:
        cross_border_observation = "대만 PDPA 기준 국외전송 여부: " + (
            "예" if merged_input.get("transfer_outside_taiwan") else "아니오"
        )
    elif "is_third_country_transfer" in merged_input:
        cross_border_observation = "제3국 이전 여부: " + (
            "예" if merged_input.get("is_third_country_transfer") else "아니오"
        )

    observations = [
        f"데이터셋: {merged_input.get('dataset_name', '미확인')}",
        "정보주체 범위: "
        + str(
            merged_input.get(
                "data_subject_region",
                merged_input.get("data_subject_connection", "미확인"),
            )
        ),
        f"현재 리전: {merged_input.get('current_region', '미확인')}",
        f"대상 리전: {merged_input.get('target_region', '미확인')}",
        f"대상 국가: {merged_input.get('target_country', '미확인')}",
    ]

    if cross_border_observation:
        observations.append(cross_border_observation)

    return observations


def evaluate_rules_for_groups(
    merged_input: Dict[str, Any],
    pack_data: Dict[str, Any],
    active_rule_groups: List[str] | None = None,
    evaluation_role: str | None = None,
) -> Dict[str, Any]:
    condition_context = dict(merged_input)
    condition_context["evaluation_role"] = evaluation_role
    decision_model = pack_data.get("decision_model", {})
    decision_order = decision_model.get(
        "precedence",
        DEFAULT_DECISION_ORDER,
    )

    triggered_rules: List[Dict[str, Any]] = []
    rule_results: List[Dict[str, Any]] = []

    all_rules = pack_data.get("rules", [])
    rules, skipped_rule_count = filter_rules_for_groups(
        all_rules,
        active_rule_groups,
    )

    for rule in rules:
        when_clause = rule.get("when", {})
        condition_result = evaluate_condition_with_trace(when_clause, condition_context)
        reasoning = condition_result["facts"] or condition_result["unmet_facts"]

        rule_results.append(
            {
                "rule_id": rule["rule_id"],
                "title": rule["title"],
                "category": rule["category"],
                "rule_group": infer_rule_group(rule),
                "matched": condition_result["matched"],
                "decision": rule["decision"] if condition_result["matched"] else None,
                "reasoning": reasoning,
            }
        )

        if not condition_result["matched"]:
            continue

        matched_facts = condition_result["facts"]
        triggered_rules.append(
            {
                "rule_id": rule["rule_id"],
                "article": str(rule["article"]),
                "title": rule["title"],
                "category": rule["category"],
                "rule_group": infer_rule_group(rule),
                "priority": rule["priority"],
                "decision": rule["decision"],
                "message": rule["message"],
                "rationale": build_rule_rationale(rule, matched_facts),
                "matched_facts": matched_facts,
                "required_evidence": rule.get("required_evidence", []),
                "required_actions": rule.get("required_actions", []),
                "references": rule.get("references", []),
                "reviewer_notes": rule.get("reviewer_notes", []),
            }
        )

    triggered_rules = sort_triggered_rules(triggered_rules, decision_order)

    final_decision = resolve_final_decision(triggered_rules, decision_order)
    legal_basis_articles = collect_legal_basis_articles(triggered_rules)
    required_actions = collect_required_actions(triggered_rules)

    summary = build_summary(final_decision, triggered_rules)
    explanation = build_explanation(
        final_decision=final_decision,
        merged_input=merged_input,
        triggered_rules=triggered_rules,
        legal_basis_articles=legal_basis_articles,
    )
    next_steps = build_next_steps(final_decision, required_actions)

    qualitative_review_hints = build_qualitative_review_hints(
        pack_data=pack_data,
        triggered_rules=triggered_rules,
        final_decision=final_decision,
        merged_input=merged_input,
    )

    return {
        "final_decision": final_decision,
        "summary": summary,
        "explanation": explanation,
        "legal_basis_articles": legal_basis_articles,
        "required_actions": required_actions,
        "next_steps": next_steps,
        "qualitative_review_hints": qualitative_review_hints,
        "triggered_rules": triggered_rules,
        "pack_info": build_pack_info(pack_data),
        "evaluation_trace": {
            "decision_order": decision_order,
            "evaluated_rule_count": len(rules),
            "matched_rule_count": len(triggered_rules),
            "strictest_triggered_decision": final_decision,
            "evaluation_role": evaluation_role,
            "active_rule_groups": active_rule_groups,
            "skipped_rule_count": skipped_rule_count,
            "skipped_rules_reason": (
                "Filtered by active rule groups for transfer-context evaluation."
                if active_rule_groups is not None
                else None
            ),
            "input_observations": build_input_observations(merged_input),
            "rule_results": rule_results,
        },
        "merged_input": merged_input,
    }


def evaluate_rules(
    merged_input: Dict[str, Any],
    pack_data: Dict[str, Any],
) -> Dict[str, Any]:
    return evaluate_rules_for_groups(
        merged_input=merged_input,
        pack_data=pack_data,
        active_rule_groups=None,
        evaluation_role=None,
    )
