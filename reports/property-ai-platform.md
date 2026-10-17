# AI Compliance Assessment — Property Portfolio AI Platform (anonymised)

**System owner:** Head of Operations  
**Purpose:** Digitises tenancy, maintenance, and contract management for a mid-size property portfolio, with a retrieval-based Arabic assistant that answers operational questions over the organisation's own records and surfaces contract terms to non-technical staff.  
**Assessment date:** 2026-10-18  
**EU AI Act risk tier (indicative):** limited  
**Frameworks assessed:** EUAIACT, ISO42001, PDPL, SDAIA

> This is a self-assessment produced by an automated mapper. It is not a certification, an audit opinion, or legal advice.

## 1. Summary

48 controls applicable · 38% implemented · 30 open gaps

**Critical:** 8 · **High:** 16 · **Medium:** 6 · **Low:** 0

| Framework | Applicable | Implemented | Coverage | Residual risk |
|---|---:|---:|---:|---:|
| EUAIACT | 3 | 1 | 33% | 3.5 / 8 |
| ISO42001 | 21 | 8 | 38% | 22.5 / 51 |
| PDPL | 9 | 0 | 0% | 19.5 / 25 |
| SDAIA | 15 | 9 | 60% | 10.0 / 39 |

Residual risk is the sum of control weights remaining after implementation status is applied (partial counts as half).

## 2. Risk register — prioritised gaps

| # | Severity | Control | Framework | Status | Residual |
|---:|---|---|---|---|---:|
| 1 | Critical | ISO42001-A.2.2 — AI policy | ISO42001 | Missing | 3.0 |
| 2 | Critical | ISO42001-A.5.2 — AI system impact assessment process | ISO42001 | Missing | 3.0 |
| 3 | Critical | ISO42001-A.5.4 — Assessing impacts on individuals | ISO42001 | Missing | 3.0 |
| 4 | Critical | PDPL-03 — Privacy notice provided to data subjects | PDPL | Missing | 3.0 |
| 5 | Critical | PDPL-04 — Data subject rights are operable | PDPL | Missing | 3.0 |
| 6 | Critical | PDPL-06 — Cross-border transfer assessed | PDPL | Missing | 3.0 |
| 7 | Critical | PDPL-08 — Breach detection and notification readiness | PDPL | Missing | 3.0 |
| 8 | Critical | SDAIA-01.1 — Fairness — bias assessment performed | SDAIA | Missing | 3.0 |
| 9 | High | EUAIACT-T1 — Transparency — users informed they interact with an AI system | EUAIACT | Partial | 1.5 |
| 10 | High | ISO42001-A.10.2 — Allocation of responsibility across the supply chain | ISO42001 | Partial | 1.5 |
| 11 | High | ISO42001-A.3.2 — AI roles and responsibilities | ISO42001 | Partial | 1.5 |
| 12 | High | ISO42001-A.4.3 — Data resources | ISO42001 | Partial | 1.5 |
| 13 | High | ISO42001-A.6.2.6 — AI system operation and monitoring | ISO42001 | Partial | 1.5 |
| 14 | High | ISO42001-A.8.2 — Information for interested parties | ISO42001 | Partial | 1.5 |
| 15 | High | PDPL-01 — Lawful basis for processing identified | PDPL | Partial | 1.5 |
| 16 | High | PDPL-02 — Purpose limitation enforced | PDPL | Partial | 1.5 |
| 17 | High | PDPL-07 — Processor obligations flowed down | PDPL | Partial | 1.5 |
| 18 | High | SDAIA-02.1 — Privacy & security — personal data minimisation | SDAIA | Partial | 1.5 |
| 19 | High | SDAIA-02.3 — Privacy & security — prompt and output handling | SDAIA | Partial | 1.5 |
| 20 | High | SDAIA-06.1 — Transparency & explainability — disclosure of AI involvement | SDAIA | Partial | 1.5 |
| 21 | High | SDAIA-07.1 — Accountability — named accountable owner | SDAIA | Partial | 1.5 |
| 22 | High | EUAIACT-T2 — Transparency — AI-generated content marked | EUAIACT | Missing | 2.0 |
| 23 | High | ISO42001-A.3.3 — Reporting of concerns | ISO42001 | Missing | 2.0 |
| 24 | High | PDPL-10 — Record of processing activities maintained | PDPL | Missing | 2.0 |
| 25 | Medium | ISO42001-A.7.5 — Data provenance | ISO42001 | Partial | 1.0 |
| 26 | Medium | ISO42001-A.8.3 — Reporting of AI system failures | ISO42001 | Partial | 1.0 |
| 27 | Medium | ISO42001-A.9.2 — Processes for responsible use | ISO42001 | Partial | 1.0 |
| 28 | Medium | PDPL-05 — Retention limits defined and enforced | PDPL | Partial | 1.0 |
| 29 | Medium | SDAIA-05.3 — Reliability & safety — change control | SDAIA | Partial | 1.0 |
| 30 | Medium | ISO42001-A.2.4 — Alignment with other organisational policies | ISO42001 | Missing | 1.0 |

## 3. Findings in detail

### ISO42001-A.2.2 — AI policy

**Framework:** ISO/IEC 42001:2023 — Artificial Intelligence Management System  
**Theme:** Policies for AI  
**Status:** Missing · **Severity:** Critical

**What good looks like.** The organisation has a documented, approved AI policy that states its objectives, its risk appetite, and who owns AI decisions.

**Evidence an assessor would ask for:**
- Approved AI policy document with version and approval date
- Evidence of periodic review

**Note from the system owner.** The client is a family business with no prior governance documentation. The policy layer is genuinely absent rather than undocumented — this is typical of the segment and is the bulk of the remediation effort.


### ISO42001-A.5.2 — AI system impact assessment process

**Framework:** ISO/IEC 42001:2023 — Artificial Intelligence Management System  
**Theme:** Impact assessment  
**Status:** Missing · **Severity:** Critical

**What good looks like.** A repeatable process exists for assessing the impact of the system on individuals and groups, performed before deployment and after material change.

**Evidence an assessor would ask for:**
- Documented impact assessment procedure
- At least one completed assessment for this system

### ISO42001-A.5.4 — Assessing impacts on individuals

**Framework:** ISO/IEC 42001:2023 — Artificial Intelligence Management System  
**Theme:** Impact assessment  
**Status:** Missing · **Severity:** Critical

**What good looks like.** The assessment specifically considers harms to individuals, including those who are not direct users of the system.

**Evidence an assessor would ask for:**
- Impact assessment section covering affected individuals

### PDPL-03 — Privacy notice provided to data subjects

**Framework:** Personal Data Protection Law (Saudi Arabia) — AI-relevant obligations  
**Theme:** Transparency  
**Status:** Missing · **Severity:** Critical

**What good looks like.** Data subjects are informed of what is collected, why, who it is shared with, and how long it is kept.

**Evidence an assessor would ask for:**
- Published privacy notice in Arabic

### PDPL-04 — Data subject rights are operable

**Framework:** Personal Data Protection Law (Saudi Arabia) — AI-relevant obligations  
**Theme:** Data subject rights  
**Status:** Missing · **Severity:** Critical

**What good looks like.** Access, correction, and deletion requests can actually be fulfilled by the system within the required period — including data held in vector stores, caches, and logs.

**Evidence an assessor would ask for:**
- Documented request procedure with response deadline
- Demonstrated deletion across all stores including derived indexes

**Note from the system owner.** Deletion is implemented for primary records but has not been proven across the retrieval index and conversation logs. This is the highest-priority engineering gap.


### PDPL-06 — Cross-border transfer assessed

**Framework:** Personal Data Protection Law (Saudi Arabia) — AI-relevant obligations  
**Theme:** Transfers  
**Status:** Missing · **Severity:** Critical

**What good looks like.** Where personal data leaves the Kingdom — including by being sent to a model API hosted abroad — the transfer condition is identified and documented.

**Evidence an assessor would ask for:**
- Transfer impact assessment
- Identified transfer mechanism and destination jurisdiction

**Note from the system owner.** Prompts containing tenant personal data reach a model API hosted outside the Kingdom. No transfer assessment exists. Treated as the highest-priority legal gap.


### PDPL-08 — Breach detection and notification readiness

**Framework:** Personal Data Protection Law (Saudi Arabia) — AI-relevant obligations  
**Theme:** Incident  
**Status:** Missing · **Severity:** Critical

**What good looks like.** A personal data breach can be detected, assessed, and notified within the required timeframe.

**Evidence an assessor would ask for:**
- Breach response procedure with notification timeline
- Evidence of at least one rehearsal

### SDAIA-01.1 — Fairness — bias assessment performed

**Framework:** SDAIA AI Ethics Principles (Kingdom of Saudi Arabia)  
**Theme:** Fairness  
**Status:** Missing · **Severity:** Critical

**What good looks like.** The system has been tested for disparate behaviour across the groups it serves, with recorded results rather than an assumption of neutrality.

**Evidence an assessor would ask for:**
- Bias test results across relevant groups
- Definition of the groups considered and why

### EUAIACT-T1 — Transparency — users informed they interact with an AI system

**Framework:** EU AI Act — provider obligations (risk-tiered)  
**Theme:** Transparency obligations  
**Status:** Partial · **Severity:** High

**What good looks like.** People interacting with the system are informed of that fact unless it is obvious from the context.

**Evidence an assessor would ask for:**
- Disclosure in the interface

### ISO42001-A.10.2 — Allocation of responsibility across the supply chain

**Framework:** ISO/IEC 42001:2023 — Artificial Intelligence Management System  
**Theme:** Third-party relationships  
**Status:** Partial · **Severity:** High

**What good looks like.** Where a third party supplies the model or infrastructure, responsibility for each obligation is allocated in writing.

**Evidence an assessor would ask for:**
- Contract or DPA allocating AI responsibilities

### ISO42001-A.3.2 — AI roles and responsibilities

**Framework:** ISO/IEC 42001:2023 — Artificial Intelligence Management System  
**Theme:** Internal organisation  
**Status:** Partial · **Severity:** High

**What good looks like.** Named individuals are accountable for the AI system across its lifecycle, not a diffuse team.

**Evidence an assessor would ask for:**
- RACI matrix naming system owner, data owner, and risk owner

### ISO42001-A.4.3 — Data resources

**Framework:** ISO/IEC 42001:2023 — Artificial Intelligence Management System  
**Theme:** Resources for AI systems  
**Status:** Partial · **Severity:** High

**What good looks like.** Every dataset the system reads or writes is identified, with its origin, lawful basis, and quality characteristics.

**Evidence an assessor would ask for:**
- Data inventory with source and lawful basis per dataset
- Documented data quality criteria

### ISO42001-A.6.2.6 — AI system operation and monitoring

**Framework:** ISO/IEC 42001:2023 — Artificial Intelligence Management System  
**Theme:** AI system lifecycle  
**Status:** Partial · **Severity:** High

**What good looks like.** Production behaviour is monitored against defined signals, with thresholds that trigger human review.

**Evidence an assessor would ask for:**
- Monitoring dashboard or alert configuration
- Defined thresholds and escalation owner

### ISO42001-A.8.2 — Information for interested parties

**Framework:** ISO/IEC 42001:2023 — Artificial Intelligence Management System  
**Theme:** Information for interested parties  
**Status:** Partial · **Severity:** High

**What good looks like.** Users and affected parties are told, in language they understand, that they are interacting with an AI system and what its limits are.

**Evidence an assessor would ask for:**
- User-facing AI disclosure text
- Documented limitations communicated to users

### PDPL-01 — Lawful basis for processing identified

**Framework:** Personal Data Protection Law (Saudi Arabia) — AI-relevant obligations  
**Theme:** Lawfulness  
**Status:** Partial · **Severity:** High

**What good looks like.** Each processing purpose has an identified lawful basis recorded before processing begins.

**Evidence an assessor would ask for:**
- Record of processing activities with basis per purpose

### PDPL-02 — Purpose limitation enforced

**Framework:** Personal Data Protection Law (Saudi Arabia) — AI-relevant obligations  
**Theme:** Lawfulness  
**Status:** Partial · **Severity:** High

**What good looks like.** Personal data is not reused for a purpose incompatible with the one it was collected for — including reuse for model development.

**Evidence an assessor would ask for:**
- Documented purposes
- Technical controls preventing out-of-purpose access

### PDPL-07 — Processor obligations flowed down

**Framework:** Personal Data Protection Law (Saudi Arabia) — AI-relevant obligations  
**Theme:** Third parties  
**Status:** Partial · **Severity:** High

**What good looks like.** Vendors processing personal data on the organisation's behalf are bound by written terms covering security, sub-processing, and deletion.

**Evidence an assessor would ask for:**
- Data processing agreement with each processor

### SDAIA-02.1 — Privacy & security — personal data minimisation

**Framework:** SDAIA AI Ethics Principles (Kingdom of Saudi Arabia)  
**Theme:** Privacy and Security  
**Status:** Partial · **Severity:** High

**What good looks like.** The system processes only the personal data it needs, and that need is documented per field.

**Evidence an assessor would ask for:**
- Field-level justification for personal data collected

### SDAIA-02.3 — Privacy & security — prompt and output handling

**Framework:** SDAIA AI Ethics Principles (Kingdom of Saudi Arabia)  
**Theme:** Privacy and Security  
**Status:** Partial · **Severity:** High

**What good looks like.** Personal data sent to or returned by a model provider is controlled, and retention by the provider is known and acceptable.

**Evidence an assessor would ask for:**
- Provider data-retention terms on file
- Redaction or minimisation applied before sending

### SDAIA-06.1 — Transparency & explainability — disclosure of AI involvement

**Framework:** SDAIA AI Ethics Principles (Kingdom of Saudi Arabia)  
**Theme:** Transparency and Explainability  
**Status:** Partial · **Severity:** High

**What good looks like.** Affected people are told when AI contributed to an output that concerns them.

**Evidence an assessor would ask for:**
- Disclosure text and where it appears

### SDAIA-07.1 — Accountability — named accountable owner

**Framework:** SDAIA AI Ethics Principles (Kingdom of Saudi Arabia)  
**Theme:** Accountability and Responsibility  
**Status:** Partial · **Severity:** High

**What good looks like.** A specific person, not a department, is accountable for the system's behaviour in production.

**Evidence an assessor would ask for:**
- Named owner recorded with date of assignment

### EUAIACT-T2 — Transparency — AI-generated content marked

**Framework:** EU AI Act — provider obligations (risk-tiered)  
**Theme:** Transparency obligations  
**Status:** Missing · **Severity:** High

**What good looks like.** Synthetic text, image, or audio output is detectable as machine-generated where it could be mistaken for human-authored material.

**Evidence an assessor would ask for:**
- Marking or labelling mechanism

### ISO42001-A.3.3 — Reporting of concerns

**Framework:** ISO/IEC 42001:2023 — Artificial Intelligence Management System  
**Theme:** Internal organisation  
**Status:** Missing · **Severity:** High

**What good looks like.** Staff and users have a defined route to raise concerns about AI behaviour without going through the system owner.

**Evidence an assessor would ask for:**
- Documented escalation channel
- Log of raised concerns and their resolution

### PDPL-10 — Record of processing activities maintained

**Framework:** Personal Data Protection Law (Saudi Arabia) — AI-relevant obligations  
**Theme:** Accountability  
**Status:** Missing · **Severity:** High

**What good looks like.** A current register of processing activities exists and reflects what the system actually does.

**Evidence an assessor would ask for:**
- Record of processing activities, dated and current

### ISO42001-A.7.5 — Data provenance

**Framework:** ISO/IEC 42001:2023 — Artificial Intelligence Management System  
**Theme:** Data for AI systems  
**Status:** Partial · **Severity:** Medium

**What good looks like.** The origin and chain of custody of each dataset can be reconstructed.

**Evidence an assessor would ask for:**
- Provenance records per dataset

### ISO42001-A.8.3 — Reporting of AI system failures

**Framework:** ISO/IEC 42001:2023 — Artificial Intelligence Management System  
**Theme:** Information for interested parties  
**Status:** Partial · **Severity:** Medium

**What good looks like.** External parties can report incorrect or harmful output, and those reports reach a named owner.

**Evidence an assessor would ask for:**
- Feedback or incident reporting channel

### ISO42001-A.9.2 — Processes for responsible use

**Framework:** ISO/IEC 42001:2023 — Artificial Intelligence Management System  
**Theme:** Responsible use  
**Status:** Partial · **Severity:** Medium

**What good looks like.** Permitted and prohibited uses are defined, and the system is constrained to the permitted ones rather than relying on user discretion.

**Evidence an assessor would ask for:**
- Acceptable-use definition
- Technical or procedural enforcement of limits

### PDPL-05 — Retention limits defined and enforced

**Framework:** Personal Data Protection Law (Saudi Arabia) — AI-relevant obligations  
**Theme:** Data lifecycle  
**Status:** Partial · **Severity:** Medium

**What good looks like.** Personal data, including conversation logs and prompts, has a defined retention period that is automatically enforced.

**Evidence an assessor would ask for:**
- Retention schedule
- Automated deletion job or policy configuration

### SDAIA-05.3 — Reliability & safety — change control

**Framework:** SDAIA AI Ethics Principles (Kingdom of Saudi Arabia)  
**Theme:** Reliability and Safety  
**Status:** Partial · **Severity:** Medium

**What good looks like.** Model, prompt, and data changes go through review and re-testing before reaching production.

**Evidence an assessor would ask for:**
- Change control record for AI components

### ISO42001-A.2.4 — Alignment with other organisational policies

**Framework:** ISO/IEC 42001:2023 — Artificial Intelligence Management System  
**Theme:** Policies for AI  
**Status:** Missing · **Severity:** Medium

**What good looks like.** The AI policy does not contradict existing security, privacy, and procurement policies, and cross-references them.

**Evidence an assessor would ask for:**
- Cross-reference matrix between the AI policy and existing policies

## 5. Scope excluded

9 controls were out of scope based on the system's declared characteristics. Scope decisions are an assessment input, not a finding — if a characteristic was declared wrongly, the exclusion is wrong too.

- `EUAIACT-H1` — Risk management system across the lifecycle
- `EUAIACT-H2` — Data governance for training, validation and testing data
- `EUAIACT-H3` — Technical documentation maintained
- `EUAIACT-H4` — Automatic logging of events
- `EUAIACT-H5` — Human oversight designed in
- `EUAIACT-H6` — Accuracy, robustness and cybersecurity
- `EUAIACT-H7` — Post-market monitoring
- `ISO42001-A.7.2` — Data for development and enhancement
- `PDPL-09` — Impact assessment for high-risk processing
