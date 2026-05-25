import type { FieldOption } from "./workspace-types";
import type { GuidedField } from "./guided-pack-types";

export const LEGAL_RESEARCH_DATE = "2026-05-07";

export const targetBooleanOptions: FieldOption[] = [
  { value: "yes", label: "예" },
  { value: "no", label: "아니오" },
  { value: "unknown", label: "잘 모르겠음" },
];

export function targetBooleanToPayloadValue(value: string | undefined) {
  if (value === "yes" || value === "true") {
    return true;
  }
  if (value === "no" || value === "false") {
    return false;
  }
  return null;
}

export const recipientRoleOptions: FieldOption[] = [
  { value: "", label: "잘 모르겠음" },
  { value: "controller", label: "Controller / 개인정보처리자" },
  { value: "processor", label: "Processor / 수탁자" },
  { value: "subprocessor", label: "Sub-processor / 재수탁자" },
  { value: "storage_only", label: "단순 보관" },
  { value: "unknown", label: "잘 모르겠음" },
];

export const COMMON_TARGET_FIELDS: GuidedField[] = [
  {
    key: "recipient_role",
    label: "수신자 역할",
    helper: "목표지 수신자가 controller, processor, 수탁자, 단순 보관자 중 어떤 지위인지 확인합니다. 역할이 불명확하면 계약과 실제 처리 지시 관계를 검토해야 합니다.",
    legalBasis: "GDPR Article 28; Korea PIPA Article 26; Taiwan PDPA Article 4",
    sourceType: "official_law",
    kind: "select",
    options: recipientRoleOptions,
  },
  {
    key: "recipient_has_target_establishment",
    label: "목표지 내 사업장 또는 처리 위치",
    helper: "수신자가 목표지에 법인, 지점, 처리 시설, 클라우드 리전 등 실제 처리 연결점을 두는지 확인합니다.",
    legalBasis: "GDPR Article 3(1); LGPD Article 3; Saudi PDPL scope review",
    sourceType: "official_law",
    kind: "segmented",
    options: targetBooleanOptions,
  },
  {
    key: "target_residents_included",
    label: "목표지 정보주체 데이터 포함",
    helper: "이전 데이터셋에 목표지에 있는 사람 또는 목표지 거주자의 개인정보가 포함되는지 확인합니다.",
    legalBasis: "GDPR Article 3(2); LGPD Article 3; PIPC foreign-business guidance",
    sourceType: "regulator_guidance",
    kind: "segmented",
    options: targetBooleanOptions,
  },
  {
    key: "offers_services_to_target_residents",
    label: "목표지 정보주체 대상 상품·서비스 제공",
    helper: "서비스, 결제, 언어, 배송, 마케팅 등이 목표지 정보주체를 대상으로 하는지 확인합니다.",
    legalBasis: "GDPR Article 3(2)(a); LGPD Article 3(II); PIPC foreign-business guidance",
    sourceType: "regulator_guidance",
    kind: "segmented",
    options: targetBooleanOptions,
  },
  {
    key: "monitors_target_residents",
    label: "목표지 정보주체 행동 모니터링",
    helper: "목표지 정보주체의 앱·웹 행동 추적, 프로파일링, 맞춤형 광고, 위치 분석 등이 있는지 확인합니다.",
    legalBasis: "GDPR Article 3(2)(b); LGPD Article 3 applicability review",
    sourceType: "official_law",
    kind: "segmented",
    options: targetBooleanOptions,
  },
  {
    key: "onward_transfer_planned",
    label: "후속 이전 예정",
    helper: "목표지 수신자가 데이터를 다시 다른 국가, 계열사, 하위 처리자에게 이전하거나 접근시킬 예정인지 확인합니다.",
    legalBasis: "GDPR Article 44; Saudi Transfer Regulation Article 5; ANPD Resolution 19/2024 Article 2",
    sourceType: "official_law",
    kind: "segmented",
    options: targetBooleanOptions,
  },
  {
    key: "destination_processing_purpose_defined",
    label: "목표지 처리 목적 문서화",
    helper: "목표지에서 수행할 처리 목적, 범위, 보관기간, 접근 주체가 문서화되어 있는지 확인합니다.",
    legalBasis: "GDPR Articles 13-14; Korea PIPA Article 30; LGPD Articles 6 and 9",
    sourceType: "official_law",
    kind: "segmented",
    options: targetBooleanOptions,
  },
  {
    key: "destination_processor_contract_ready",
    label: "목표지 처리자 계약·위탁 조건 준비",
    helper: "수신자가 processor/수탁자라면 처리 지시, 보안, 하위 처리자, 반환·삭제, 감사 조건이 계약에 반영되어 있는지 확인합니다.",
    legalBasis: "GDPR Article 28; Korea PIPA Article 26; Taiwan PDPA Article 4",
    sourceType: "official_law",
    kind: "segmented",
    options: targetBooleanOptions,
  },
];

export const TARGET_LAW_FIELDS_BY_PACK: Record<string, GuidedField[]> = {
  gdpr: [
    {
      key: "gdpr_eu_data_subjects_included",
      label: "EU/EEA 내 정보주체 데이터 포함",
      helper: "처리 대상자가 EU/EEA에 있는 사람인지 확인합니다. 국적이 아니라 처리 활동과 EU/EEA 내 사람의 연결성을 기준으로 검토합니다.",
      legalBasis: "GDPR Article 3(2)",
      sourceType: "official_law",
      kind: "segmented",
      options: targetBooleanOptions,
    },
    {
      key: "gdpr_eu_establishment_involved",
      label: "EU/EEA 내 controller 또는 processor 사업장 관여",
      helper: "EU/EEA 내 사업장의 활동 맥락에서 처리되는지 확인합니다. 처리 장소가 EU 밖이어도 적용될 수 있습니다.",
      legalBasis: "GDPR Article 3(1)",
      sourceType: "official_law",
      kind: "segmented",
      options: targetBooleanOptions,
    },
    {
      key: "gdpr_offers_goods_or_services_to_eu",
      label: "EU/EEA 내 정보주체 대상 상품·서비스 제공",
      helper: "결제 여부와 무관하게 EU/EEA 내 사람에게 상품·서비스 제공 의도가 있는지 확인합니다.",
      legalBasis: "GDPR Article 3(2)(a)",
      sourceType: "official_law",
      kind: "segmented",
      options: targetBooleanOptions,
    },
    {
      key: "gdpr_monitors_eu_behavior",
      label: "EU/EEA 내 행동 모니터링",
      helper: "EU/EEA 내 행동 추적, 프로파일링, 광고 식별자 분석 등 모니터링 처리인지 확인합니다.",
      legalBasis: "GDPR Article 3(2)(b)",
      sourceType: "official_law",
      kind: "segmented",
      options: targetBooleanOptions,
    },
    {
      key: "gdpr_processor_contract_ready",
      label: "Processor 계약/DPA 준비",
      helper: "수신자가 processor라면 Article 28 수준의 계약 또는 법적 행위가 준비되어 있는지 확인합니다.",
      legalBasis: "GDPR Article 28",
      sourceType: "official_law",
      kind: "segmented",
      options: targetBooleanOptions,
    },
    {
      key: "gdpr_onward_transfer_safeguard_ready",
      label: "후속 이전 보호조치 준비",
      helper: "EU/EEA 밖 또는 다른 제3국으로의 후속 이전이 있다면 적정성, SCC, BCR, 예외 등 Chapter V 경로가 준비되어 있는지 확인합니다.",
      legalBasis: "GDPR Articles 44-49",
      sourceType: "official_law",
      kind: "segmented",
      options: targetBooleanOptions,
    },
  ],
  korea_pipa: [
    {
      key: "pipa_korean_data_subjects_included",
      label: "한국 정보주체 개인정보 포함",
      helper: "한국에 있는 정보주체 또는 한국 이용자의 개인정보가 처리되는지 확인합니다.",
      legalBasis: "PIPC foreign-business guidance; PIPA Articles 35-38",
      sourceType: "regulator_guidance",
      kind: "segmented",
      options: targetBooleanOptions,
    },
    {
      key: "pipa_services_to_korean_users",
      label: "한국 이용자 대상 상품·서비스 제공",
      helper: "외국 사업자라도 한국 이용자에게 상품·서비스를 제공하며 개인정보를 처리하는지 확인합니다.",
      legalBasis: "PIPC foreign-business guidance",
      sourceType: "regulator_guidance",
      kind: "segmented",
      options: targetBooleanOptions,
    },
    {
      key: "pipa_effect_on_korean_data_subjects",
      label: "한국 정보주체 권리·이익에 직접 영향 가능성",
      helper: "처리 결과가 한국 정보주체의 권리 행사, 서비스 이용, 피해구제에 직접 영향을 줄 수 있는지 확인합니다.",
      legalBasis: "PIPC foreign-business guidance; PIPA Articles 35-38",
      sourceType: "regulator_guidance",
      kind: "segmented",
      options: targetBooleanOptions,
    },
    {
      key: "pipa_domestic_agent_or_establishment",
      label: "한국 내 사업장 또는 국내대리인 관련성",
      helper: "한국 내 사업장, 수신자, 또는 국내대리인 지정 검토 대상인지 확인합니다.",
      legalBasis: "PIPA Article 31-2",
      sourceType: "official_law",
      kind: "segmented",
      options: targetBooleanOptions,
    },
    {
      key: "pipa_cross_border_notice_items_ready",
      label: "국외이전 고지·공개 항목 준비",
      helper: "국외 제공, 조회, 위탁, 보관에 관한 수령자, 국가, 목적, 항목, 기간, 거부권 등 고지·공개 항목을 준비했는지 확인합니다.",
      legalBasis: "PIPA Article 28-8",
      sourceType: "official_law",
      kind: "segmented",
      options: targetBooleanOptions,
    },
    {
      key: "pipa_privacy_policy_disclosure_ready",
      label: "개인정보 처리방침 공개 준비",
      helper: "위탁·국외이전·처리 목적 등 개인정보 처리방침 공개 항목이 최신 상태인지 확인합니다.",
      legalBasis: "PIPA Article 30",
      sourceType: "official_law",
      kind: "segmented",
      options: targetBooleanOptions,
    },
  ],
  saudi_pdpl: [
    {
      key: "pdpl_saudi_data_subjects_included",
      label: "사우디 정보주체 개인정보 포함",
      helper: "처리 데이터가 사우디 내 개인 또는 사우디와 실질적으로 연결된 정보주체에 관한 것인지 확인합니다.",
      legalBasis: "Saudi PDPL scope; PDPL Article 29",
      sourceType: "official_law",
      kind: "segmented",
      options: targetBooleanOptions,
    },
    {
      key: "pdpl_saudi_controller_or_processor_involved",
      label: "사우디 내 controller 또는 processor 관여",
      helper: "사우디 내 controller, processor, 지점, 데이터센터가 처리 흐름에 관여하는지 확인합니다.",
      legalBasis: "Saudi PDPL controller/processor obligations",
      sourceType: "official_law",
      kind: "segmented",
      options: targetBooleanOptions,
    },
    {
      key: "pdpl_sensitive_or_special_data",
      label: "민감정보 또는 특수 데이터 포함",
      helper: "민감정보가 계속적 또는 광범위하게 국외이전되는 경우 위험평가가 요구될 수 있으므로 데이터 범위를 확인합니다.",
      legalBasis: "Saudi Transfer Regulation Article 8",
      sourceType: "official_law",
      kind: "segmented",
      options: targetBooleanOptions,
    },
    {
      key: "pdpl_transfer_regulation_safeguards_ready",
      label: "PDPL 이전 규정상 보호조치 준비",
      helper: "표준계약조항, 구속규칙, 인증 등 이전 규정상 보호조치가 준비되어 있는지 확인합니다.",
      legalBasis: "Saudi Transfer Regulation Article 5",
      sourceType: "official_law",
      kind: "segmented",
      options: targetBooleanOptions,
    },
    {
      key: "pdpl_scc_or_adequacy_ready",
      label: "적정 보호수준 또는 SCC/BCR 경로 확인",
      helper: "수령국의 적정 보호수준 또는 SDAIA 기준 보호조치 경로가 확인되었는지 검토합니다.",
      legalBasis: "Saudi PDPL Article 29; Transfer Regulation Articles 3 and 5",
      sourceType: "official_law",
      kind: "segmented",
      options: targetBooleanOptions,
    },
    {
      key: "pdpl_onward_transfer_planned",
      label: "후속 이전 예정",
      helper: "사우디 밖으로 이전된 개인정보가 다시 다른 국가나 조직으로 이전되는지 확인합니다.",
      legalBasis: "Saudi Transfer Regulation Article 5",
      sourceType: "official_law",
      kind: "segmented",
      options: targetBooleanOptions,
    },
  ],
  lgpd: [
    {
      key: "lgpd_brazil_data_subjects_included",
      label: "브라질 내 개인의 개인정보 처리",
      helper: "처리 활동이 브라질 내 개인에게 상품·서비스를 제공하거나 브라질 내 개인의 데이터를 처리하는지 확인합니다.",
      legalBasis: "LGPD Article 3(II)",
      sourceType: "official_law",
      kind: "segmented",
      options: targetBooleanOptions,
    },
    {
      key: "lgpd_data_collected_in_brazil",
      label: "브라질 내 수집 데이터",
      helper: "개인정보가 브라질 영토 안에서 수집되었는지 확인합니다.",
      legalBasis: "LGPD Article 3(III)",
      sourceType: "official_law",
      kind: "segmented",
      options: targetBooleanOptions,
    },
    {
      key: "lgpd_services_to_brazil_residents",
      label: "브라질 내 개인 대상 상품·서비스 제공",
      helper: "처리 목적이 브라질 내 개인에게 상품 또는 서비스를 제공하는 것인지 확인합니다.",
      legalBasis: "LGPD Article 3(II)",
      sourceType: "official_law",
      kind: "segmented",
      options: targetBooleanOptions,
    },
    {
      key: "lgpd_international_transfer_mechanism_ready",
      label: "ANPD 국제이전 메커니즘 준비",
      helper: "적정성, 표준계약조항, 특정계약조항, 글로벌 기업규칙, 예외 등 유효한 국제이전 메커니즘을 확인합니다.",
      legalBasis: "LGPD Articles 33-36; Resolution CD/ANPD No. 19/2024 Articles 4 and 9",
      sourceType: "official_law",
      kind: "segmented",
      options: targetBooleanOptions,
    },
    {
      key: "lgpd_data_subject_rights_process_ready",
      label: "정보주체 권리 대응 절차 준비",
      helper: "접근, 정정, 삭제, 이동성, 처리 확인 등 정보주체 권리 요청 대응 절차가 준비되어 있는지 확인합니다.",
      legalBasis: "LGPD Article 18",
      sourceType: "official_law",
      kind: "segmented",
      options: targetBooleanOptions,
    },
  ],
  taiwan: [
    {
      key: "taiwan_data_subjects_included",
      label: "대만 정보주체 개인정보 포함",
      helper: "대만 정보주체 개인정보가 수집, 처리, 이용되는지 확인합니다.",
      legalBasis: "Taiwan PDPA Articles 2, 8-9",
      sourceType: "official_law",
      kind: "segmented",
      options: targetBooleanOptions,
    },
    {
      key: "taiwan_recipient_processing_in_taiwan",
      label: "대만 내 수신자 처리",
      helper: "대만 내 수신자, 지점, 처리시설 또는 위탁 처리자가 처리 흐름에 관여하는지 확인합니다.",
      legalBasis: "Taiwan PDPA Articles 4, 19-20",
      sourceType: "official_law",
      kind: "segmented",
      options: targetBooleanOptions,
    },
    {
      key: "taiwan_recipient_country_protection_adequate",
      label: "수신국 개인정보 보호수준 충분성",
      helper: "수신국에 적절한 개인정보 보호 법제가 부족해 정보주체 권익이 해칠 우려가 있는지 검토합니다.",
      legalBasis: "Taiwan PDPA Article 21(3)",
      sourceType: "official_law",
      kind: "segmented",
      options: targetBooleanOptions,
    },
    {
      key: "taiwan_circumvention_transfer_risk",
      label: "PDPA 우회 이전 가능성",
      helper: "대만 PDPA 적용을 피하기 위해 제3국을 우회하는 국제전송 구조인지 확인합니다.",
      legalBasis: "Taiwan PDPA Article 21(4)",
      sourceType: "official_law",
      kind: "segmented",
      options: targetBooleanOptions,
    },
    {
      key: "taiwan_sector_restriction_possible",
      label: "산업별 감독기관 제한 가능성",
      helper: "금융, 의료, 통신 등 산업별 주무기관이 국제전송을 제한할 수 있는지 확인합니다.",
      legalBasis: "Taiwan PDPA Article 21",
      sourceType: "manual_review_checklist",
      kind: "segmented",
      options: targetBooleanOptions,
    },
    {
      key: "taiwan_security_maintenance_ready",
      label: "보안 및 유지관리 조치 준비",
      helper: "도난, 변경, 훼손, 멸실, 유출 방지를 위한 보안 및 유지관리 조치가 준비되어 있는지 확인합니다.",
      legalBasis: "Taiwan PDPA Article 20-1",
      sourceType: "official_law",
      kind: "segmented",
      options: targetBooleanOptions,
    },
  ],
};

export const TARGET_LAW_RESEARCH_NOTES: Record<string, string[]> = {
  gdpr: [
    "EUR-Lex Regulation (EU) 2016/679 Articles 3, 9, 13-14, 28, 44-49 checked",
  ],
  korea_pipa: [
    "KLRI/National Law Information Center PIPA Articles 28-8, 30, 31-2, 34, 35-38 checked",
    "PIPC cross-border transfer and foreign-business guidance checked",
  ],
  saudi_pdpl: [
    "SDAIA PDPL Article 29 and Regulation on Personal Data Transfer Outside the Kingdom Articles 4, 5, 7 checked",
  ],
  lgpd: [
    "Brazil LGPD Articles 3, 18, 33-36 and ANPD Resolution CD/ANPD No. 19/2024 checked",
  ],
  taiwan: [
    "Taiwan MOJ/PDPC PDPA Articles 8-9, 20-1, 21 checked",
  ],
};

export function getTargetLawFields(packId: string | null | undefined) {
  if (!packId) {
    return [];
  }
  return TARGET_LAW_FIELDS_BY_PACK[packId] ?? [];
}

export function getTargetLawLabel(packId: string | null | undefined) {
  const labels: Record<string, string> = {
    gdpr: "GDPR 추가 확인 항목",
    korea_pipa: "Korea PIPA 추가 확인 항목",
    saudi_pdpl: "Saudi PDPL 추가 확인 항목",
    lgpd: "Brazil LGPD 추가 확인 항목",
    taiwan: "Taiwan PDPA 추가 확인 항목",
  };
  return packId ? labels[packId] ?? "현재 해당 목표지 법률팩 없음" : "현재 해당 목표지 법률팩 없음";
}
