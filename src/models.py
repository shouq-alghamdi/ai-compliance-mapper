"""Core data structures for the compliance mapper."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Status(str, Enum):
    """Implementation status of a control for a given system."""

    IMPLEMENTED = "implemented"
    PARTIAL = "partial"
    MISSING = "missing"
    NOT_APPLICABLE = "not_applicable"
    NOT_ASSESSED = "not_assessed"


# How much of a control's weight remains as residual risk at each status.
RESIDUAL_FACTOR: dict[Status, float] = {
    Status.IMPLEMENTED: 0.0,
    Status.PARTIAL: 0.5,
    Status.MISSING: 1.0,
    Status.NOT_ASSESSED: 1.0,
    Status.NOT_APPLICABLE: 0.0,
}


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"


@dataclass(frozen=True)
class Condition:
    """A single applicability test against a system characteristic."""

    field: str
    equals: Any = None
    not_equals: Any = None
    in_: list[Any] | None = None

    def evaluate(self, characteristics: dict[str, Any]) -> bool:
        value = characteristics.get(self.field)
        if self.equals is not None:
            return value == self.equals
        if self.not_equals is not None:
            return value != self.not_equals
        if self.in_ is not None:
            return value in self.in_
        # A condition with no operator is treated as a truthiness test.
        return bool(value)


@dataclass(frozen=True)
class Control:
    id: str
    title: str
    theme: str
    intent: str
    weight: int
    framework_id: str
    framework_name: str
    evidence: tuple[str, ...] = ()
    applies_when: tuple[Condition, ...] = ()

    def applies_to(self, characteristics: dict[str, Any]) -> bool:
        """All conditions must hold (logical AND). No conditions = always applies."""
        return all(c.evaluate(characteristics) for c in self.applies_when)


@dataclass
class SystemProfile:
    name: str
    owner: str
    purpose: str
    characteristics: dict[str, Any] = field(default_factory=dict)
    control_status: dict[str, Status] = field(default_factory=dict)
    notes: dict[str, str] = field(default_factory=dict)

    def status_for(self, control_id: str) -> Status:
        return self.control_status.get(control_id, Status.NOT_ASSESSED)


@dataclass
class Finding:
    """One assessed control, with its residual risk."""

    control: Control
    status: Status
    residual_score: float
    severity: Severity
    note: str = ""

    @property
    def is_gap(self) -> bool:
        return self.status in (
            Status.MISSING,
            Status.PARTIAL,
            Status.NOT_ASSESSED,
        )


@dataclass
class Assessment:
    profile: SystemProfile
    findings: list[Finding]
    risk_tier: str
    frameworks: list[str]

    @property
    def applicable(self) -> list[Finding]:
        return [f for f in self.findings if f.status is not Status.NOT_APPLICABLE]

    @property
    def gaps(self) -> list[Finding]:
        return [f for f in self.applicable if f.is_gap]

    @property
    def coverage(self) -> float:
        """Share of applicable controls fully implemented, 0.0-1.0."""
        applicable = self.applicable
        if not applicable:
            return 0.0
        done = sum(1 for f in applicable if f.status is Status.IMPLEMENTED)
        return done / len(applicable)

    @property
    def residual_total(self) -> float:
        return sum(f.residual_score for f in self.applicable)

    @property
    def inherent_total(self) -> float:
        return float(sum(f.control.weight for f in self.applicable))
