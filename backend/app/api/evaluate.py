from fastapi import APIRouter, HTTPException

from app.schemas.evaluate_request import EvaluateRequest
from app.schemas.evaluation import FinalEvaluationResponse
from app.schemas.merge import MergeSampleRequest
from app.schemas.transfer_context import (
    EvaluateTransferRequest,
    EvaluateTransferResponse,
)
from app.services.derived_fields import (
    build_common_transfer_derived_fields,
    country_to_pack_id,
    derive_source_country,
    derive_target_country,
)
from app.services.evaluation_service import evaluate_rules, evaluate_rules_for_groups
from app.services.file_loader import load_json_file, load_yaml_file
from app.services.merge_service import flatten_schema_fields, is_nullable_field, merge_inputs
from app.services.pack_applicability_service import select_applicable_packs
from app.services.pack_loader import load_input_schema, load_pack
from app.services.request_merge_service import build_merged_input_from_request
from app.utils.path_helper import get_sample_input_path

router = APIRouter(prefix="/api/v1", tags=["evaluate"])


def dedupe_strings(values: list[str]) -> list[str]:
    seen = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def strongest_decision(results: list[dict]) -> str:
    precedence = ["deny", "manual_review", "condition_allow", "allow"]
    decisions = [result["final_decision"] for result in results]
    for decision in precedence:
        if decision in decisions:
            return decision
    return "manual_review"


def normalize_unknowns(value):
    if isinstance(value, dict):
        return {key: normalize_unknowns(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize_unknowns(item) for item in value]
    if value == "unknown":
        return None
    return value


def build_transfer_context_dict(payload: EvaluateTransferRequest) -> dict:
    target_applicability_data = normalize_unknowns(payload.target_applicability_data)
    base_policy_data = normalize_unknowns(payload.policy_data)
    aws_data = normalize_unknowns(payload.aws_data)

    source_region = payload.source_region or aws_data.get("source_region") or aws_data.get(
        "current_region"
    )
    target_region = payload.target_region or base_policy_data.get("target_region")
    source_country = payload.source_country or derive_source_country(
        source_region,
        aws_data.get("current_region"),
    )
    target_country = payload.target_country or derive_target_country(target_region)
    derived_target_pack_id = None
    if target_country:
        derived_target_pack_id = country_to_pack_id(target_country)

    context = {
        **aws_data,
        **base_policy_data,
        **target_applicability_data,
        "source_region": source_region,
        "current_region": aws_data.get("current_region") or source_region,
        "target_region": target_region,
        "source_country": source_country,
        "target_country": target_country,
        "source_pack_id": payload.source_pack_id,
        "target_pack_id": payload.target_pack_id or target_applicability_data.get("target_pack_id"),
        "source_pack_id_override": payload.source_pack_id is not None,
        "target_pack_id_override": payload.target_pack_id is not None
        and payload.target_pack_id != derived_target_pack_id,
    }
    context.update(build_common_transfer_derived_fields(context))
    return context


def build_transfer_merge_payload(context: dict, payload: EvaluateTransferRequest) -> tuple[dict, dict]:
    aws_data = {
        **normalize_unknowns(payload.aws_data),
        "current_region": context.get("current_region") or context.get("source_region"),
        "source_region": context.get("source_region"),
    }
    policy_data = {
        **normalize_unknowns(payload.policy_data),
        **normalize_unknowns(payload.target_applicability_data),
        "target_region": context.get("target_region"),
        "source_region": context.get("source_region"),
        "source_country": context.get("source_country"),
        "target_country": context.get("target_country"),
        "source_pack_id": context.get("source_pack_id"),
        "target_pack_id": context.get("target_pack_id"),
    }
    if "dataset_name" not in policy_data or policy_data.get("dataset_name") is None:
        policy_data["dataset_name"] = "transfer-assessment"
    return aws_data, policy_data


def fill_required_schema_defaults(
    *,
    pack_id: str,
    aws_data: dict,
    policy_data: dict,
) -> tuple[dict, dict]:
    schema = load_input_schema(pack_id=pack_id)
    aws_next = dict(aws_data)
    policy_next = dict(policy_data)

    for field_name, meta in flatten_schema_fields(schema).items():
        if meta.get("required") is not True:
            continue
        if field_name in aws_next or field_name in policy_next:
            continue
        if is_nullable_field(meta):
            policy_next[field_name] = None
            continue
        if field_name == "dataset_name":
            policy_next[field_name] = "transfer-assessment"
        elif field_name in {"current_region", "source_region"}:
            aws_next[field_name] = aws_data.get("current_region") or aws_data.get(
                "source_region"
            )
        elif field_name == "target_region":
            policy_next[field_name] = policy_data.get("target_region")
        elif field_name in {"data_subject_region", "data_subject_connection"}:
            policy_next[field_name] = policy_data.get("data_subject_region") or "OTHER"
        else:
            policy_next[field_name] = "unknown"

    return aws_next, policy_next


@router.post("/evaluate-sample", response_model=FinalEvaluationResponse)
def evaluate_sample(payload: MergeSampleRequest):
    try:
        sample_input_path = get_sample_input_path()

        schema = load_input_schema(
            pack_id=payload.pack_id,
            schema_file_name=payload.schema_file_name,
        )
        aws_data = load_json_file(sample_input_path / payload.aws_file_name)
        policy_data = load_yaml_file(sample_input_path / payload.policy_file_name)

        merged_input = merge_inputs(schema, aws_data, policy_data)
        pack_data = load_pack(pack_id=payload.pack_id)

        return evaluate_rules(merged_input=merged_input, pack_data=pack_data)

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/evaluate", response_model=FinalEvaluationResponse)
def evaluate(payload: EvaluateRequest):
    try:
        merged_input = build_merged_input_from_request(
            aws_data=payload.aws_data,
            policy_data=payload.policy_data,
            pack_id=payload.pack_id,
            schema_file_name=payload.schema_file_name,
        )

        pack_data = load_pack(
            pack_id=payload.pack_id,
            file_name=payload.pack_file_name,
        )

        return evaluate_rules(
            merged_input=merged_input,
            pack_data=pack_data,
        )

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/evaluate-transfer", response_model=EvaluateTransferResponse)
def evaluate_transfer(payload: EvaluateTransferRequest):
    try:
        context = build_transfer_context_dict(payload)
        selected_packs = select_applicable_packs(context)
        if not selected_packs:
            raise ValueError(
                "No applicable source or target policy pack could be inferred. Provide source_pack_id or a supported source region."
            )

        aws_data, policy_data = build_transfer_merge_payload(context, payload)
        pack_results = []
        raw_results = []

        for selected in selected_packs:
            pack_aws_data, pack_policy_data = fill_required_schema_defaults(
                pack_id=selected["pack_id"],
                aws_data=aws_data,
                policy_data=policy_data,
            )
            merged_input = build_merged_input_from_request(
                aws_data=pack_aws_data,
                policy_data=pack_policy_data,
                pack_id=selected["pack_id"],
            )
            merged_input.update(context)
            pack_data = load_pack(pack_id=selected["pack_id"])
            result = evaluate_rules_for_groups(
                merged_input=merged_input,
                pack_data=pack_data,
                active_rule_groups=selected["rule_groups"],
                evaluation_role=selected["evaluation_role"],
            )
            raw_results.append(result)
            pack_results.append(
                {
                    "pack_id": selected["pack_id"],
                    "evaluation_role": selected["evaluation_role"],
                    "result": result,
                }
            )

        final_decision = strongest_decision(raw_results)
        merged_required_actions = dedupe_strings(
            [
                action
                for result in raw_results
                for action in result.get("required_actions", [])
            ]
        )
        merged_legal_basis_articles = dedupe_strings(
            [
                article
                for result in raw_results
                for article in result.get("legal_basis_articles", [])
            ]
        )
        global_next_steps = dedupe_strings(
            [step for result in raw_results for step in result.get("next_steps", [])]
        )

        return {
            "final_decision": final_decision,
            "summary": (
                f"Transfer evaluation completed for {len(pack_results)} policy pack(s). "
                "Source law was evaluated as required; target law was included only when applicability was indicated or ambiguous."
            ),
            "source_country": context.get("source_country"),
            "target_country": context.get("target_country"),
            "selected_packs": selected_packs,
            "pack_results": pack_results,
            "merged_required_actions": merged_required_actions,
            "merged_legal_basis_articles": merged_legal_basis_articles,
            "global_next_steps": global_next_steps,
        }

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
