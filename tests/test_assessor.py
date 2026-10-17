"""Tests for applicability, tiering, and scoring."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.assessor import assess, prioritised_gaps, resolve_risk_tier, severity_for
from src.loader import LoaderError, load_library, load_profile
from src.models import Condition, Control, Severity, Status, SystemProfile

ROOT = Path(__file__).resolve().parent.parent
CONTROLS = ROOT / "controls"
EXAMPLE = ROOT / "examples" / "property-ai-platform.yaml"


def make_control(cid="X-1", weight=3, conditions=()):
    return Control(
        id=cid,
        title="Test control",
        theme="Test",
        intent="Something good.",
        weight=weight,
        framework_id="TEST",
        framework_name="Test framework",
        applies_when=tuple(conditions),
    )


# --- applicability ---------------------------------------------------------


def test_control_with_no_conditions_always_applies():
    assert make_control().applies_to({})


def test_condition_equals_gates_applicability():
    control = make_control(
        conditions=[Condition(field="processes_personal_data", equals=True)]
    )
    assert control.applies_to({"processes_personal_data": True})
    assert not control.applies_to({"processes_personal_data": False})
    assert not control.applies_to({})


def test_multiple_conditions_are_anded():
    control = make_control(
        conditions=[
            Condition(field="a", equals=True),
            Condition(field="b", equals=True),
        ]
    )
    assert control.applies_to({"a": True, "b": True})
    assert not control.applies_to({"a": True, "b": False})


def test_condition_in_operator():
    control = make_control(conditions=[Condition(field="tier", in_=["high", "limited"])])
    assert control.applies_to({"tier": "high"})
    assert not control.applies_to({"tier": "minimal"})


# --- risk tiering ----------------------------------------------------------


TIER_RULES = {
    "prohibited": {"when_any": [{"field": "social_scoring", "equals": True}]},
    "high": {"when_any": [{"field": "biometric", "equals": True}]},
    "limited": {"when_any": [{"field": "user_facing", "equals": True}]},
    "minimal": {"when_any": []},
}


def test_prohibited_beats_everything():
    tier = resolve_risk_tier(
        {"social_scoring": True, "biometric": True, "user_facing": True}, TIER_RULES
    )
    assert tier == "prohibited"


def test_high_beats_limited():
    assert resolve_risk_tier({"biometric": True, "user_facing": True}, TIER_RULES) == "high"


def test_falls_through_to_minimal():
    assert resolve_risk_tier({"user_facing": False}, TIER_RULES) == "minimal"


def test_no_rules_gives_unclassified():
    assert resolve_risk_tier({}, {}) == "unclassified"


# --- severity --------------------------------------------------------------


@pytest.mark.parametrize(
    "weight,status,expected",
    [
        (3, Status.MISSING, Severity.CRITICAL),
        (3, Status.NOT_ASSESSED, Severity.CRITICAL),
        (3, Status.PARTIAL, Severity.HIGH),
        (2, Status.MISSING, Severity.HIGH),
        (1, Status.MISSING, Severity.MEDIUM),
        (1, Status.PARTIAL, Severity.LOW),
        (3, Status.IMPLEMENTED, Severity.NONE),
    ],
)
def test_severity_mapping(weight, status, expected):
    assert severity_for(weight, status) is expected


# --- scoring ---------------------------------------------------------------


def test_partial_counts_as_half_residual():
    profile = SystemProfile(
        name="S", owner="O", purpose="P", control_status={"X-1": Status.PARTIAL}
    )
    result = assess(profile, [make_control(weight=2)])
    assert result.findings[0].residual_score == pytest.approx(1.0)


def test_unlisted_control_defaults_to_not_assessed_and_full_residual():
    profile = SystemProfile(name="S", owner="O", purpose="P")
    result = assess(profile, [make_control(weight=3)])
    finding = result.findings[0]
    assert finding.status is Status.NOT_ASSESSED
    assert finding.residual_score == pytest.approx(3.0)
    assert finding.is_gap


def test_inapplicable_control_scores_zero_and_is_not_a_gap():
    control = make_control(conditions=[Condition(field="biometric", equals=True)])
    profile = SystemProfile(
        name="S", owner="O", purpose="P", characteristics={"biometric": False}
    )
    result = assess(profile, [control])
    assert result.findings[0].status is Status.NOT_APPLICABLE
    assert result.gaps == []
    assert result.coverage == 0.0


def test_coverage_is_share_of_applicable_implemented():
    controls = [make_control("A"), make_control("B")]
    profile = SystemProfile(
        name="S",
        owner="O",
        purpose="P",
        control_status={"A": Status.IMPLEMENTED, "B": Status.MISSING},
    )
    assert assess(profile, controls).coverage == pytest.approx(0.5)


def test_gaps_are_ordered_by_severity():
    controls = [make_control("LOW", weight=1), make_control("CRIT", weight=3)]
    profile = SystemProfile(
        name="S",
        owner="O",
        purpose="P",
        control_status={"LOW": Status.MISSING, "CRIT": Status.MISSING},
    )
    ordered = prioritised_gaps(assess(profile, controls))
    assert [f.control.id for f in ordered] == ["CRIT", "LOW"]


# --- loading ---------------------------------------------------------------


def test_every_shipped_framework_loads():
    metas, controls = load_library(CONTROLS)
    assert {m["id"] for m in metas} == {"ISO42001", "SDAIA", "PDPL", "EUAIACT"}
    assert len(controls) > 40


def test_control_ids_are_globally_unique():
    _, controls = load_library(CONTROLS)
    ids = [c.id for c in controls]
    assert len(ids) == len(set(ids))


def test_framework_filter_narrows_the_library():
    _, controls = load_library(CONTROLS, only=["PDPL"])
    assert {c.framework_id for c in controls} == {"PDPL"}


def test_bad_status_value_is_rejected_with_a_useful_message(tmp_path):
    bad = tmp_path / "bad.yaml"
    bad.write_text(
        "system:\n  name: S\n  owner: O\n  purpose: P\n"
        "control_status:\n  PDPL-01: done\n",
        encoding="utf-8",
    )
    with pytest.raises(LoaderError, match="not a valid status"):
        load_profile(bad)


# --- end to end ------------------------------------------------------------


def test_example_profile_assesses_end_to_end():
    _, controls = load_library(CONTROLS)
    profile = load_profile(EXAMPLE)
    result = assess(profile, controls, _tier_rules())
    assert result.risk_tier == "limited"
    assert len(result.applicable) > 40
    assert 0.0 < result.coverage < 1.0
    assert result.residual_total < result.inherent_total


def _tier_rules():
    metas, _ = load_library(CONTROLS)
    for meta in metas:
        if meta.get("risk_tiers"):
            return meta["risk_tiers"]
    return {}
