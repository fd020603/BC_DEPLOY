import {
  COMMON_TARGET_FIELDS,
  TARGET_LAW_FIELDS_BY_PACK,
  getTargetLawFields,
  targetBooleanToPayloadValue,
} from "./target-law-question-config";

function assert(condition: boolean, message: string) {
  if (!condition) {
    throw new Error(message);
  }
}

export function runTargetLawQuestionConfigTests() {
  assert(getTargetLawFields("gdpr").some((field) => field.key === "gdpr_eu_data_subjects_included"), "EU/EEA target region must expose GDPR-specific questions.");
  assert(getTargetLawFields("korea_pipa").some((field) => field.key === "pipa_korean_data_subjects_included"), "Korea target region must expose PIPA-specific questions.");
  assert(getTargetLawFields("saudi_pdpl").some((field) => field.key === "pdpl_saudi_data_subjects_included"), "Saudi target region must expose PDPL-specific questions.");
  assert(getTargetLawFields("lgpd").some((field) => field.key === "lgpd_brazil_data_subjects_included"), "Brazil target region must expose LGPD-specific questions.");
  assert(getTargetLawFields("taiwan").some((field) => field.key === "taiwan_data_subjects_included"), "Taiwan target region must expose Taiwan PDPA-specific questions.");
  assert(getTargetLawFields("unmapped").length === 0, "Unmapped target regions should only use common target questions.");
  assert(COMMON_TARGET_FIELDS.length > 0, "Common target applicability questions must remain available.");
  assert(Object.keys(TARGET_LAW_FIELDS_BY_PACK).length >= 5, "All current target law packs must be configured.");
  assert(targetBooleanToPayloadValue("yes") === true, "yes must map to true.");
  assert(targetBooleanToPayloadValue("no") === false, "no must map to false.");
  assert(targetBooleanToPayloadValue("unknown") === null, "unknown must map to null.");
  assert(targetBooleanToPayloadValue(undefined) === null, "undefined must map to null.");
}
