"""Command-line entry point for the AI Compliance Mapper."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .assessor import assess
from .loader import LoaderError, load_library, load_profile
from .report import render_markdown

DEFAULT_CONTROLS = Path(__file__).resolve().parent.parent / "controls"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="compliance-mapper",
        description=(
            "Assess an AI system against ISO/IEC 42001, the SDAIA AI ethics "
            "principles, Saudi PDPL, and the EU AI Act, and produce a risk "
            "register and gap report."
        ),
    )
    parser.add_argument(
        "profile",
        type=Path,
        help="Path to the system profile YAML file.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Write the report here. Prints to stdout if omitted.",
    )
    parser.add_argument(
        "-c",
        "--controls",
        type=Path,
        default=DEFAULT_CONTROLS,
        help="Directory holding the control library (default: ./controls).",
    )
    parser.add_argument(
        "-f",
        "--framework",
        action="append",
        dest="frameworks",
        metavar="ID",
        help=(
            "Limit the assessment to this framework id (repeatable). "
            "e.g. -f ISO42001 -f PDPL"
        ),
    )
    parser.add_argument(
        "--fail-on",
        choices=["critical", "high", "none"],
        default="none",
        help=(
            "Exit with a non-zero status if gaps at this severity or above "
            "exist. Useful in CI."
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        metas, controls = load_library(args.controls, only=args.frameworks)
        profile = load_profile(args.profile)
    except LoaderError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(f"error: file not found: {exc.filename}", file=sys.stderr)
        return 2

    tier_rules: dict = {}
    for meta in metas:
        if meta.get("risk_tiers"):
            tier_rules = meta["risk_tiers"]

    assessment = assess(profile, controls, tier_rules)
    report = render_markdown(assessment)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
        print(
            f"Assessed {profile.name}: "
            f"{len(assessment.applicable)} applicable controls, "
            f"{assessment.coverage * 100:.0f}% implemented, "
            f"{len(assessment.gaps)} gaps.",
            file=sys.stderr,
        )
        print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(report)

    if args.fail_on != "none":
        from .models import Severity

        blocking = {"critical": {Severity.CRITICAL}}
        blocking["high"] = {Severity.CRITICAL, Severity.HIGH}
        hits = [f for f in assessment.gaps if f.severity in blocking[args.fail_on]]
        if hits:
            print(
                f"{len(hits)} gap(s) at or above '{args.fail_on}'.",
                file=sys.stderr,
            )
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
