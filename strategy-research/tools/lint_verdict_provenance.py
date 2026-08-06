"""
lint_verdict_provenance.py -- standalone G6 checker (C7-EXT-R / D-4).

WHY THIS EXISTS, AND WHY IT IS SEPARATE FROM ANY WRITE PATH.

The independent audit (engineering/sessions/session_reports/20260722_c7ext_audit.md) found that
`validate_verdict_provenance` had exactly ONE call site in the whole repository:
inside run_phase1_research._write_kb_findings_entry. Two consequences followed,
and this tool closes the second:

  1. config/campaign_queue.yaml was never validated at all. That is fixed at the
     writer (run_campaign._save_queue).

  2. campaign_knowledge_base.yaml was validated only as a SIDE EFFECT of the
     orchestrator happening to write a finding. A hand edit -- which is exactly
     how the XS_momentum entry arrived -- was unchecked until, and unless, some
     later orchestrator run touched the file. Between runs, nothing looked.

So the check must be runnable with no write involved, on demand, in CI, or by a
reviewer who simply wants to know whether the campaign's memory is honest right
now. That is this file.

    python strategy-research/tools/lint_verdict_provenance.py
    python strategy-research/tools/lint_verdict_provenance.py --root <dir>

Exit 0 = every verdict-bearing record either cites a resolvable
pass_rule_evaluation.yaml or honestly declares `verdict_status: ungated`.
Exit 1 = at least one record asserts something about a hypothesis that nothing
in the repository backs.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import yaml  # noqa: E402

import record_schema  # noqa: E402
import verdict_criteria_evaluator as vce  # noqa: E402


def _load(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def lint_verdict_provenance(root=None) -> list:
    """Returns a list of violation strings; empty means clean.

    Checks BOTH stores, because a verdict is equally consequential whichever one
    a later reader finds it in."""
    base = Path(root) if root is not None else _HERE.parent
    violations = []

    sources = (
        ("campaign_knowledge_base.yaml", "findings", base / "campaign_record" / "campaign_knowledge_base.yaml",
         record_schema.KB_FINDING_SCHEMA),
        ("campaign_queue.yaml", "queue", base / "config" / "campaign_queue.yaml",
         record_schema.QUEUE_ENTRY_SCHEMA),
    )
    for label, key, path, schema in sources:
        document = _load(path)
        for entry in document.get(key) or []:
            if not isinstance(entry, dict):
                continue
            name = entry.get("id") or entry.get("hypothesis_id") or "<unnamed>"
            try:
                # C7-EXT-R2: this now checks the closed record schema as well as
                # provenance -- an unknown field is a violation in its own right.
                vce.validate_verdict_provenance(
                    entry, entry_ref=f"{label} entry {name!r}", root=base,
                    schema=schema)
            except vce.UngatedVerdictError as exc:
                violations.append(str(exc))
    return violations


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--root", default=None,
                        help="strategy-research/ root (defaults to this file's parent)")
    args = parser.parse_args(argv)

    base = Path(args.root) if args.root else _HERE.parent
    violations = lint_verdict_provenance(base)

    if violations:
        print(f"FAIL  {len(violations)} ungated verdict(s) in the campaign record:\n")
        for violation in violations:
            print(f"  - {violation}\n")
        print("Each must either cite a pass_rule_evaluation.yaml that resolves, or "
              "declare `verdict_status: ungated` and keep its measurements.")
        return 1

    gated = vce.honest_verdict_count(
        _load(base / "campaign_record" / "campaign_knowledge_base.yaml"),
        _load(base / "config" / "campaign_queue.yaml"),
        root=base)
    print("OK  every verdict-bearing record is either gated or declared ungated.")
    print(f"    gated verdicts: {len(gated)} {gated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
