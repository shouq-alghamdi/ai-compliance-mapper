# Control Library Schema

Each framework file is a YAML document:

```yaml
framework:
  id: ISO42001
  name: ISO/IEC 42001:2023 — AI Management System
  version: "2023"
  authority: ISO/IEC
  note: Practitioner mapping. Not the official normative text.

controls:
  - id: ISO42001-A.2.2
    title: AI policy
    theme: Policies
    intent: >
      One sentence, in plain language, describing what good looks like.
    applies_when: []          # empty = always applicable
    weight: 3                 # 1..3 — contribution to inherent risk if absent
    evidence:                 # what an auditor would ask to see
      - Approved AI policy document
      - Evidence of annual review
```

## `applies_when`

A list of conditions. **All** must be true for the control to apply
(logical AND). Each condition is:

```yaml
- field: processes_personal_data   # key under `characteristics` in the system profile
  equals: true                     # or: in: [a, b]  /  not_equals: x
```

An empty list means the control always applies.

## `weight`

| Weight | Meaning |
|---|---|
| 1 | Hygiene — absence is a finding, not a risk |
| 2 | Material — absence creates real exposure |
| 3 | Fundamental — absence is a blocking gap |

## Control status (supplied by the system profile)

`implemented` · `partial` · `missing` · `not_applicable` · `not_assessed`

Anything not listed in the profile defaults to `not_assessed`, which is
scored as `missing` but reported separately — an unassessed control is a
finding about the assessment, not only about the system.
