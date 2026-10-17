"""Report rendering: Markdown risk register and gap report."""

from __future__ import annotations

from datetime import date

from .assessor import prioritised_gaps
from .models import Assessment, Severity, Status

SEVERITY_LABEL = {
    Severity.CRITICAL: "Critical",
    Severity.HIGH: "High",
    Severity.MEDIUM: "Medium",
    Severity.LOW: "Low",
    Severity.NONE: "—",
}

STATUS_LABEL = {
    Status.IMPLEMENTED: "Implemented",
    Status.PARTIAL: "Partial",
    Status.MISSING: "Missing",
    Status.NOT_ASSESSED: "Not assessed",
    Status.NOT_APPLICABLE: "N/A",
}


def _summary_table(assessment: Assessment) -> str:
    rows = []
    for framework in assessment.frameworks:
        items = [
            f
            for f in assessment.applicable
            if f.control.framework_id == framework
        ]
        if not items:
            continue
        done = sum(1 for f in items if f.status is Status.IMPLEMENTED)
        residual = sum(f.residual_score for f in items)
        inherent = sum(f.control.weight for f in items)
        pct = (done / len(items)) * 100
        rows.append(
            f"| {framework} | {len(items)} | {done} | {pct:.0f}% | "
            f"{residual:.1f} / {inherent:.0f} |"
        )
    header = (
        "| Framework | Applicable | Implemented | Coverage | Residual risk |\n"
        "|---|---:|---:|---:|---:|"
    )
    return header + "\n" + "\n".join(rows)


def _severity_counts(assessment: Assessment) -> str:
    counts = {s: 0 for s in Severity if s is not Severity.NONE}
    for finding in assessment.gaps:
        counts[finding.severity] += 1
    parts = [
        f"**{SEVERITY_LABEL[s]}:** {n}"
        for s, n in counts.items()
        if s is not Severity.NONE
    ]
    return " · ".join(parts)


def render_markdown(assessment: Assessment, assessed_on: date | None = None) -> str:
    profile = assessment.profile
    assessed_on = assessed_on or date.today()
    gaps = prioritised_gaps(assessment)
    not_assessed = [f for f in assessment.applicable if f.status is Status.NOT_ASSESSED]

    lines: list[str] = []
    add = lines.append

    add(f"# AI Compliance Assessment — {profile.name}")
    add("")
    add(f"**System owner:** {profile.owner}  ")
    add(f"**Purpose:** {' '.join(profile.purpose.split())}  ")
    add(f"**Assessment date:** {assessed_on.isoformat()}  ")
    add(f"**EU AI Act risk tier (indicative):** {assessment.risk_tier}  ")
    add(f"**Frameworks assessed:** {', '.join(assessment.frameworks)}")
    add("")
    add(
        "> This is a self-assessment produced by an automated mapper. "
        "It is not a certification, an audit opinion, or legal advice."
    )
    add("")

    add("## 1. Summary")
    add("")
    add(
        f"{len(assessment.applicable)} controls applicable · "
        f"{assessment.coverage * 100:.0f}% implemented · "
        f"{len(gaps)} open gaps"
    )
    add("")
    add(_severity_counts(assessment))
    add("")
    add(_summary_table(assessment))
    add("")
    add(
        "Residual risk is the sum of control weights remaining after "
        "implementation status is applied (partial counts as half)."
    )
    add("")

    add("## 2. Risk register — prioritised gaps")
    add("")
    if not gaps:
        add("No open gaps against the applicable control set.")
        add("")
    else:
        add("| # | Severity | Control | Framework | Status | Residual |")
        add("|---:|---|---|---|---|---:|")
        for i, f in enumerate(gaps, start=1):
            add(
                f"| {i} | {SEVERITY_LABEL[f.severity]} | "
                f"{f.control.id} — {f.control.title} | {f.control.framework_id} | "
                f"{STATUS_LABEL[f.status]} | {f.residual_score:.1f} |"
            )
        add("")

    add("## 3. Findings in detail")
    add("")
    for f in gaps:
        add(f"### {f.control.id} — {f.control.title}")
        add("")
        add(f"**Framework:** {f.control.framework_name}  ")
        add(f"**Theme:** {f.control.theme}  ")
        add(f"**Status:** {STATUS_LABEL[f.status]} · "
            f"**Severity:** {SEVERITY_LABEL[f.severity]}")
        add("")
        add(f"**What good looks like.** {f.control.intent}")
        add("")
        if f.control.evidence:
            add("**Evidence an assessor would ask for:**")
            for item in f.control.evidence:
                add(f"- {item}")
            add("")
        if f.note:
            add(f"**Note from the system owner.** {f.note}")
            add("")

    if not_assessed:
        add("## 4. Controls not yet assessed")
        add("")
        add(
            "These applicable controls had no status recorded. They are scored "
            "as missing, but the finding is about the completeness of the "
            "assessment as much as about the system."
        )
        add("")
        for f in not_assessed:
            add(f"- `{f.control.id}` — {f.control.title}")
        add("")

    add("## 5. Scope excluded")
    add("")
    excluded = [f for f in assessment.findings if f.status is Status.NOT_APPLICABLE]
    if not excluded:
        add("No controls were excluded.")
    else:
        add(
            f"{len(excluded)} controls were out of scope based on the system's "
            "declared characteristics. Scope decisions are an assessment input, "
            "not a finding — if a characteristic was declared wrongly, the "
            "exclusion is wrong too."
        )
        add("")
        for f in excluded:
            add(f"- `{f.control.id}` — {f.control.title}")
    add("")

    return "\n".join(lines)
