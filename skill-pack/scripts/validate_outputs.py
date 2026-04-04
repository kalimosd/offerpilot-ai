#!/usr/bin/env python3
"""Validate OfferPilot output naming and optional English name ordering."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

OUTPUT_HINTS = ("resume", "cover", "letter")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run lightweight checks on OfferPilot output files."
    )
    parser.add_argument("paths", nargs="+", help="Output files to validate.")
    parser.add_argument(
        "--english-name",
        default=None,
        help="Optional English candidate name to check, e.g. 'GivenName FamilyName'.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    errors: list[str] = []
    warnings: list[str] = []

    for raw_path in args.paths:
        path = Path(raw_path)
        if not path.exists():
            errors.append(f"Missing output file: {path}")
            continue

        lowered_name = path.name.lower()
        if not any(hint in lowered_name for hint in OUTPUT_HINTS):
            warnings.append(
                f"{path} does not look like a standard OfferPilot output filename."
            )

    if args.english_name:
        name = args.english_name.strip()
        if not re.fullmatch(r"[A-Za-z]+(?: [A-Za-z]+)+", name):
            errors.append(
                "--english-name must look like 'GivenName FamilyName' using letters and spaces."
            )
        else:
            parts = name.split()
            if len(parts) != 2:
                warnings.append(
                    "English name has more than two parts. Confirm the intended Given Name + Family Name order manually."
                )

    for warning in warnings:
        print(f"WARNING: {warning}")

    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        return 1

    print("OK: output files passed basic OfferPilot checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
