# Methodology

How this tool turns a system description into a number, and what that number
does and does not mean.

## 1. The assessment unit is the control, not the framework

A framework is a container. The assessable unit is a single control with a
stated intent, a weight, and a list of evidence a competent assessor would ask
for. Frameworks overlap heavily — ISO/IEC 42001's event logging control and the
EU AI Act's automatic logging obligation are substantially the same engineering
work — and the library keeps them as separate controls rather than merging
them, because an organisation has to satisfy each authority separately even
when one piece of evidence serves both.

This means the totals are **not** a count of distinct engineering tasks. A
system with good logging closes several controls at once. The report is
organised by framework for that reason.

## 2. Applicability is resolved before scoring

Every control carries an `applies_when` list of conditions evaluated against
the system's declared characteristics. All conditions must hold (logical AND);
an empty list means the control always applies.

A control that does not apply is marked `not_applicable`, scored zero, and
listed in the report's scope-exclusion section. It is never silently dropped.

**Why this matters.** The most common failure in compliance tooling is scoring
a system against controls that have no bearing on it, which produces a low
score that nobody believes and everybody ignores. The second most common
failure is the reverse — excluding controls quietly, so the scope decision is
never reviewed. Both are failures of the same kind: the scoping judgement is
the assessment, and it belongs in the output where it can be challenged.

## 3. Risk tiering gates scope

The system's characteristics resolve to a single tier by checking, in order:
`prohibited`, `high`, `limited`, `minimal`. The first tier with a satisfied
condition wins, so the tier is always the highest that applies.

The resolved tier is then injected back into the characteristics as
`_risk_tier`, which lets controls declare `applies_when: [{field: _risk_tier,
equals: high}]`. This is how the EU AI Act's high-risk obligations switch on
without special-casing them in code.

**Limitation.** Tier resolution here is indicative engineering triage. Legal
classification under the EU AI Act depends on intended purpose, deployment
context, and annex membership in ways this tool does not model.

## 4. Weight expresses consequence of absence

| Weight | Meaning |
|---:|---|
| 3 | Fundamental — absence is a blocking gap |
| 2 | Material — absence creates real exposure |
| 1 | Hygiene — absence is a finding, not a risk |

Weights are assigned per control in the library and are a judgement call. They
are visible and editable in YAML precisely so that a reviewer can disagree with
one and change it rather than argue with a black box.

## 5. Status reduces weight to residual risk

```
residual = weight × factor(status)
```

| Status | Factor | Rationale |
|---|---:|---|
| `implemented` | 0.0 | Control is in place |
| `partial` | 0.5 | Something exists; it does not fully meet the intent |
| `missing` | 1.0 | Nothing in place |
| `not_assessed` | 1.0 | Unknown is treated as absent |
| `not_applicable` | 0.0 | Out of scope |

**The `partial` factor is the weakest assumption in the model.** A half-built
control is not reliably half as risky as a missing one — sometimes it is worse,
because it creates the appearance of coverage. 0.5 is chosen for being
defensible and obvious rather than accurate. If you need precision here, split
the control into two.

**Unknown is scored as absent, deliberately.** Treating `not_assessed` as
neutral would let an organisation improve its score by assessing less. The
report lists these separately so the reader can see which part of the residual
total is genuine absence and which part is simply unexamined.

## 6. Severity is derived, not declared

| | weight 3 | weight 2 | weight 1 |
|---|---|---|---|
| `missing` / `not_assessed` | Critical | High | Medium |
| `partial` | High | Medium | Low |

Severity drives the ordering of the risk register. It is a function of weight
and status only — it does not model likelihood, because likelihood of a
*governance* failure is not meaningfully estimable from a system description.

## 7. Coverage

```
coverage = controls fully implemented ÷ applicable controls
```

Partial counts as zero here, unlike in residual scoring. Coverage answers
"what fraction is actually done" and a half-done control is not done. The two
measures are intentionally different, and the report shows both.

## What this method cannot do

- **It cannot verify a status.** Every status is self-declared. The tool adds
  structure and consistency to an honest assessment; it detects nothing about a
  dishonest one.
- **It cannot assess evidence quality.** `implemented` with a one-page policy
  and `implemented` with a tested, reviewed control programme score identically.
- **It cannot determine legal obligation.** Which law applies to a given system
  in a given jurisdiction is a legal question.
- **It cannot measure the model.** Accuracy, bias, and robustness controls are
  recorded here as governance facts — whether a test exists and what it found.
  Running those tests is separate work.

## Reassessment

The residual total is designed to be tracked over time for the same system. A
meaningful reassessment changes statuses and leaves the library fixed; changing
weights and statuses together makes the trend uninterpretable. If the library
is updated, record which version each assessment ran against.
