"""
stamp_protocol.py — K3 (B3, §5/§9 Q3): version-stamps a protocol JSON file and
prints its content hash for pasting into a pre_registration.yaml brief's
machine_constraints.protocol_ref_content_hash.

Computes a STRUCTURAL hash (json.dumps(obj, sort_keys=True) before hashing,
not raw bytes) so the hash is tolerant of key reordering from hand edits --
appropriate here since a protocol file is meant to be human-authored/edited,
unlike K4's byte-verbatim brief-install hash. The hash is computed over the
file's own body MINUS its own protocol_version/protocol_content_hash fields
(avoids a circular hash-of-a-hash problem). This formula is deliberately
duplicated (not imported) from workflow/run_phase1_research.py's
_compute_protocol_content_hash -- that module pulls in claude_agent_sdk/
google.genai at import time, too heavy a dependency for this standalone
tool. tests/test_k3_protocol_pinning.py's round-trip fixture asserts the
two stay identical for the same input.

CLI:
  python strategy-research/tools/stamp_protocol.py protocols/ts_trend_daily_v2.json
  python strategy-research/tools/stamp_protocol.py protocols/ts_trend_daily_v2.json --version 2026-07-15
"""
import argparse
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

_HERE = Path(__file__).resolve().parent      # strategy-research/tools/
_SR = _HERE.parent                            # strategy-research/


def compute_protocol_content_hash(obj: dict) -> str:
    """Same formula as run_phase1_research.py's _compute_protocol_content_hash,
    operating on an already-loaded dict rather than re-reading the file."""
    stripped = {k: v for k, v in obj.items() if k not in ("protocol_version", "protocol_content_hash")}
    canonical = json.dumps(stripped, sort_keys=True)
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def stamp(path: Path, version: str) -> str:
    """
    Writes protocol_version/protocol_content_hash into the file at `path`
    (computed over everything else), returning the hash written.
    """
    obj = json.loads(path.read_text(encoding="utf-8"))
    content_hash = compute_protocol_content_hash(obj)

    obj["protocol_version"] = version
    obj["protocol_content_hash"] = content_hash
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")
    return content_hash


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Stamp a protocol JSON with protocol_version/protocol_content_hash "
                     "and print the hash for machine_constraints.protocol_ref_content_hash."
    )
    parser.add_argument("protocol_path", help="Path to the protocol JSON file (e.g. protocols/ts_trend_daily_v2.json).")
    parser.add_argument(
        "--version",
        default=None,
        help="protocol_version value to stamp. Defaults to today's date (YYYY-MM-DD).",
    )
    args = parser.parse_args()

    path = Path(args.protocol_path)
    if not path.is_absolute():
        # Resolve relative to repo root (strategy-research/), matching how
        # machine_constraints.protocol_ref values are written/read.
        candidate = _SR / path
        path = candidate if candidate.exists() else path
    if not path.exists():
        print(f"ERROR: protocol file not found at {path}", file=sys.stderr)
        sys.exit(1)

    version = args.version or date.today().isoformat()
    content_hash = stamp(path, version)

    print(f"Stamped {path}")
    print(f"  protocol_version:      {version}")
    print(f"  protocol_content_hash: {content_hash}")
    print()
    print("Paste into pre_registration.yaml's machine_constraints:")
    print(f'  protocol_ref_content_hash: "{content_hash}"')


if __name__ == "__main__":
    main()
