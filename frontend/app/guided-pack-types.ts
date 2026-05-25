import type { FieldOption, JsonObject } from "./workspace-types";

export type GuidedFormState = Record<string, string>;

export type GuidedField = {
  key: string;
  label: string;
  helper: string;
  legalBasis?: string;
  sourceType?: "official_law" | "regulator_guidance" | "manual_review_checklist";
  tooltip?: string;
  kind: "select" | "segmented" | "text";
  options?: FieldOption[];
  required?: boolean;
  visibleIf?: (state: GuidedFormState) => boolean;
};

export type GuidedStep = {
  id: string;
  title: string;
  description: string;
  fields: GuidedField[];
};

export type PackUiDefinition = {
  id: string;
  label: string;
  subtitle: string;
  storageKey: string;
  steps: GuidedStep[];
  defaultState: GuidedFormState;
  validate: (state: GuidedFormState) => string[];
  buildPayload: (state: GuidedFormState) => {
    aws_data: JsonObject;
    policy_data: JsonObject;
  };
  buildAdvisoryNotes: (state: GuidedFormState) => string[];
  buildSummaryRows: (state: GuidedFormState) => Array<{
    label: string;
    value: string;
  }>;
};
