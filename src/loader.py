"""Loading of control libraries and system profiles from YAML."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .models import Condition, Control, Status, SystemProfile


class LoaderError(Exception):
    """Raised when a control file or system profile is malformed."""


def _parse_conditions(raw: Any, control_id: str) -> tuple[Condition, ...]:
    if not raw:
        return ()
    if not isinstance(raw, list):
        raise LoaderError(f"{control_id}: applies_when must be a list")
    out = []
    for item in raw:
        if not isinstance(item, dict) or "field" not in item:
            raise LoaderError(f"{control_id}: each condition needs a 'field'")
        out.append(
            Condition(
                field=item["field"],
                equals=item.get("equals"),
                not_equals=item.get("not_equals"),
                in_=item.get("in"),
            )
        )
    return tuple(out)


def load_framework(path: Path) -> tuple[dict[str, Any], list[Control]]:
    """Load one framework YAML file. Returns (framework_meta, controls)."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "framework" not in data:
        raise LoaderError(f"{path.name}: missing 'framework' block")

    meta = data["framework"]
    meta["risk_tiers"] = data.get("risk_tiers", {})
    controls: list[Control] = []

    for raw in data.get("controls", []):
        for required in ("id", "title", "weight"):
            if required not in raw:
                raise LoaderError(f"{path.name}: control missing '{required}'")
        weight = raw["weight"]
        if weight not in (1, 2, 3):
            raise LoaderError(f"{raw['id']}: weight must be 1, 2 or 3")
        controls.append(
            Control(
                id=raw["id"],
                title=raw["title"],
                theme=raw.get("theme", "General"),
                intent=(raw.get("intent") or "").strip(),
                weight=weight,
                framework_id=meta["id"],
                framework_name=meta["name"],
                evidence=tuple(raw.get("evidence", ())),
                applies_when=_parse_conditions(raw.get("applies_when"), raw["id"]),
            )
        )

    ids = [c.id for c in controls]
    duplicates = {i for i in ids if ids.count(i) > 1}
    if duplicates:
        raise LoaderError(f"{path.name}: duplicate control ids: {sorted(duplicates)}")

    return meta, controls


def load_library(
    controls_dir: Path, only: list[str] | None = None
) -> tuple[list[dict[str, Any]], list[Control]]:
    """Load every framework in a directory, optionally filtered by framework id."""
    metas: list[dict[str, Any]] = []
    controls: list[Control] = []

    for path in sorted(controls_dir.glob("*.yaml")):
        meta, items = load_framework(path)
        if only and meta["id"] not in only:
            continue
        metas.append(meta)
        controls.extend(items)

    if not controls:
        raise LoaderError(f"No controls loaded from {controls_dir}")
    return metas, controls


def load_profile(path: Path) -> SystemProfile:
    """Load a system profile YAML file."""
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "system" not in data:
        raise LoaderError(f"{path.name}: missing 'system' block")

    system = data["system"]
    for required in ("name", "owner", "purpose"):
        if required not in system:
            raise LoaderError(f"{path.name}: system missing '{required}'")

    raw_status = data.get("control_status") or {}
    status: dict[str, Status] = {}
    for control_id, value in raw_status.items():
        try:
            status[control_id] = Status(value)
        except ValueError as exc:
            valid = ", ".join(s.value for s in Status)
            raise LoaderError(
                f"{path.name}: '{value}' is not a valid status for {control_id}. "
                f"Use one of: {valid}"
            ) from exc

    characteristics = dict(data.get("characteristics") or {})
    characteristics.setdefault("deployment", system.get("deployment", "development"))

    return SystemProfile(
        name=system["name"],
        owner=system["owner"],
        purpose=system["purpose"],
        characteristics=characteristics,
        control_status=status,
        notes=dict(data.get("notes") or {}),
    )
