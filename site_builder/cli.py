from __future__ import annotations

import argparse
from pathlib import Path

from site_builder.generator import SpecError, generate_site, load_spec


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a static website from a JSON specification.",
    )
    parser.add_argument(
        "--spec",
        type=Path,
        required=True,
        help="Path to the JSON specification file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("dist"),
        help="Directory to write the generated site.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        spec = load_spec(args.spec)
    except (OSError, SpecError) as exc:
        parser.error(str(exc))
        return 2

    output_path = generate_site(spec, args.output)
    print(f"Site generated at {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
