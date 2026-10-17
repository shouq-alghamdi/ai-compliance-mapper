"""Applicability resolution, risk tiering, and residual risk scoring."""

from __future__ import annotations

from typing import Any

from .models import (
    RESIDUAL_FACTOR,
    Assessment,
    Control,
    Finding,
    Severity,
    Status,
    SystemProfile,
)

TIER_ORDER = ["prohibited", "high", "limited", "minimal"]


def resolve_risk_tier(characteristics: dict[str, Any], tier_rules: dict) -> str:
    """Return the highest tier whose `when_any` conditions are satisfied."""
    if not tier_rules:
        return "unclassified"

    for tier in TIER_ORDER:
        rule = tier_rules.get(tier)
        if rule is None:
            continue
        conditions = rule.get("when_any", [])
        if not conditions:
            # An empty when_any is the catch-all floor for that tier.
            return tier
        for cond in conditions:
            if characteristics.get(cond["field"]) == cond.get("equals"):
                return tier
    return "minimal"


def severity_for(weight: int, status: Status) -> Severity:
    """Map (control weight, status) onto a reportable severity."""
    if status in (Status.IMPLEMENTED, Status.NOT_APPLICABLE):
        return Severity.NONE
    if status is Status.PARTIAL:
        return {3: Severity.HIGH, 2: Severity.MEDIUM, 1: Severity.LOW}[weight]
    # MISSING or NOT_ASSESSED
    return {3: Severity.CRITICAL, 2: Severity.HIGH, 1: Severity.MEDIUM}[weight]


def assess(
    profile: SystemProfile,
    controls: list[Control],
    tier_rules: dict | None = None,
) -> Assessment:
    """Run a full assessment of one system profile against a control library."""
    characteristics = dict(profile.characteristics)

    risk_tier = resolve_risk_tier(characteristics, tier_rules or {})
    # Expose the resolved tier so controls can key off it (see EUAIACT-H*).
    characteristics["_risk_tier"] = risk_tier

    findings: list[Finding] = []
    for control in controls:
        if not control.applies_to(characteristics):
            findings.append(
                Finding(
                    control=control,
                    status=Status.NOT_APPLICABLE,
                    residual_score=0.0,
                    severity=Severity.NONE,
                    note="Out of scope for this system's characteristics.",
                )
            )
            continue

        status = profile.status_for(control.id)
        residual = control.weight * RESIDUAL_FACTOR[status]
        findings.append(
            Finding(
                control=control,
                status=status,
                residual_score=residual,
                severity=severity_for(control.weight, status),
                note=profile.notes.get(control.id, ""),
            )
        )

    frameworks = sorted({c.framework_id for c in controls})
    return Assessment(
        profile=profile,
        findings=findings,
        risk_tier=risk_tier,
        frameworks=frameworks,
    )


SEVERITY_RANK = {
    Severity.CRITICAL: 0,
    Severity.HIGH: 1,
    Severity.MEDIUM: 2,
    Severity.LOW: 3,
    Severity.NONE: 4,
}


def prioritised_gaps(assessment: Assessment) -> list[Finding]:
    """Gaps ordered by severity, then by control weight, then by id."""
    return sorted(
        assessment.gaps,
        key=lambda f: (
            SEVERITY_RANK[f.severity],
            -f.control.weight,
            f.control.id,
        ),
    )
