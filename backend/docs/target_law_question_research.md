# Target Law Question Research

## Research date
2026-05-07

This record supports Border Checker as a compliance support and legal review support system. It does not replace legal advice. Target-law results should remain manual-review oriented unless the factual record and official legal basis are clear.

## Sources Checked
- GDPR: EUR-Lex, Regulation (EU) 2016/679, Articles 3, 9, 13-14, 28, 44-49.
- Korea PIPA: KLRI/National Law Information Center Personal Information Protection Act; PIPC cross-border transfer page; PIPC release on Guidelines on Applying PIPA to Foreign Business Operators.
- Saudi PDPL: SDAIA National Data Governance Platform, Personal Data Protection Law and Regulation on Personal Data Transfer Outside the Kingdom.
- Brazil LGPD: Planalto Law No. 13,709/2018; ANPD Resolution CD/ANPD No. 19/2024.
- Taiwan PDPA: Taiwan MOJ Laws & Regulations Database / Preparatory Office of PDPC, Personal Data Protection Act.

## Common Target Questions
- `recipient_role`: needed because controller/processor, entrustment, and commissioned-processing duties differ by law.
- `recipient_has_target_establishment`: common signal for territorial or establishment-based applicability.
- `target_residents_included`: common signal for data-subject connection.
- `offers_services_to_target_residents`: common signal under GDPR Article 3(2)(a), LGPD Article 3, and PIPC foreign-business guidance.
- `monitors_target_residents`: common signal under GDPR Article 3(2)(b), and useful manual-review signal for other laws.
- `onward_transfer_planned`: needed because GDPR Chapter V, Saudi transfer rules, ANPD Resolution 19/2024, and Taiwan Article 21 treat onward/downstream transfers differently.
- `destination_processing_purpose_defined`: supports transparency and purpose-limitation checks.
- `destination_processor_contract_ready`: supports processor/entrustment contract review.

## GDPR
- Articles checked: Article 3; Article 9; Articles 13-14; Article 28; Articles 44-49.
- UI fields derived: `gdpr_eu_data_subjects_included`, `gdpr_eu_establishment_involved`, `gdpr_offers_goods_or_services_to_eu`, `gdpr_monitors_eu_behavior`, `gdpr_processor_contract_ready`, `gdpr_onward_transfer_safeguard_ready`.
- Rule groups: `extraterritorial_scope` for Article 3 threshold; `target_processor_governance` for Article 28; `target_onward_transfer` and `target_transparency` for Chapter V and Articles 13-14.
- Manual review items: Article 3 facts, processor contract sufficiency, onward transfer mechanism, and special-category/notice coverage.

## Korea PIPA
- Articles and guidance checked: PIPA Article 28-8; Article 30; Article 31-2; Article 34; Articles 35-38; PIPC foreign-business guidance; PIPC cross-border transfer page.
- UI fields derived: `pipa_korean_data_subjects_included`, `pipa_services_to_korean_users`, `pipa_effect_on_korean_data_subjects`, `pipa_domestic_agent_or_establishment`, `pipa_cross_border_notice_items_ready`, `pipa_privacy_policy_disclosure_ready`.
- Rule groups: `extraterritorial_scope` for PIPC foreign-business applicability; `target_transparency` for Article 28-8 and Article 30; `domestic_agent` for Article 31-2.
- Manual review items: foreign-business scope is guidance-driven; domestic-agent thresholds depend on facts and decree thresholds; cross-border notice readiness should not auto-allow.

## Saudi PDPL
- Sources checked: SDAIA PDPL materials, Implementing Regulation, and transfer regulation materials.
- Articles/sections checked: PDPL Article 29; Transfer Regulation provisions on general transfer conditions, safeguards, and risk assessment.
- UI fields derived: `pdpl_saudi_data_subjects_included`, `pdpl_saudi_controller_or_processor_involved`, `pdpl_sensitive_or_special_data`, `pdpl_transfer_regulation_safeguards_ready`, `pdpl_scc_or_adequacy_ready`, `pdpl_onward_transfer_planned`.
- Rule groups: `target_processing` for Saudi target involvement; `transfer_safeguards` for adequacy/SCC/BCR-style paths; `risk_assessment` for sensitive or large-scale transfer review.
- Manual review items: official pages expose amended materials in more than one structure; article numbering for risk assessment should be rechecked by counsel against the authoritative Arabic/current text before final legal reliance.

## Brazil LGPD
- Articles checked: LGPD Article 3; Article 18; Articles 33-36; ANPD Resolution CD/ANPD No. 19/2024 Articles 4, 5, 7, 9, 15-17.
- UI fields derived: `lgpd_brazil_data_subjects_included`, `lgpd_data_collected_in_brazil`, `lgpd_services_to_brazil_residents`, `lgpd_international_transfer_mechanism_ready`, `lgpd_data_subject_rights_process_ready`.
- Rule groups: `extraterritorial_scope` for Article 3; `international_transfer` for LGPD/ANPD transfer mechanisms; `target_transparency` for rights and transparency readiness.
- Manual review items: ANPD mechanism fit, SCC migration/contract incorporation, onward transfers, and rights-process evidence.

## Taiwan PDPA
- Articles checked: Article 2; Articles 8-9; Articles 19-20; Article 20-1; Article 21.
- UI fields derived: `taiwan_data_subjects_included`, `taiwan_recipient_processing_in_taiwan`, `taiwan_recipient_country_protection_adequate`, `taiwan_circumvention_transfer_risk`, `taiwan_sector_restriction_possible`, `taiwan_security_maintenance_ready`.
- Rule groups: `target_processing` for collection/processing/use and notice; `recipient_country_protection` for Article 21; `authority_restriction_review` for sector restriction checklist; `target_security_baseline` for Article 20-1.
- Manual review items: sector-specific restrictions and competent-authority limitations should remain checklist items unless an official restriction applies to the scenario.

## Unknown / Null Handling
- UI answers use `yes`, `no`, `unknown`.
- Payload conversion is `yes -> true`, `no -> false`, `unknown -> null`, and missing values -> `null`.
- Backend schema accepts law-specific fields as `Optional[bool]`.
- Policy rules include manual-review evidence-gap rules for `null`; `null` is not treated as `false` and does not create automatic allow.

## Future Legal Review
- Validate Saudi transfer regulation article numbering against the latest official Arabic/current consolidated text.
- Validate Korean domestic-agent thresholds under the current Enforcement Decree for each business size/data scale.
- Add sector-specific Taiwan transfer restrictions when official competent-authority rules are identified.
- Review whether any official EDPB guidance should refine GDPR Article 3 targeting/monitoring examples.
