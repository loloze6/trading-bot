"""Lane 1's hand record (D-128): READ-ONLY check that decide-next's composition input lists
run_084's block as active and the two voided blocks (run_089, run_083) as excluded.

Usage (from the operator checkout's strategy-research/, after the block entry and the `status`
command were applied):
    ../venv/Scripts/python.exe engineering/lane1_replay/lane1_registry_check.py

Calls `tools.decide_next.load_inputs(..., composition_runs=True)` (the same call the campaign
makes, tools/decide_next.py:986) and prints the registry it carries under inputs["composition"],
next to the registry file's own block and status lists. Writes nothing.
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "workflow"))

import block_registry as br  # noqa: E402
import reader_categories  # noqa: E402
import decide_next as dn  # noqa: E402


def main() -> None:
    reg_path = ROOT / "campaign_record" / "block_registry.yaml"
    raw = br.load_registry(reg_path)
    queue = yaml.safe_load((ROOT / "config" / "campaign_queue.yaml").read_text(encoding="utf-8")) or {}
    # the campaign's own category list (tools/reader_categories.py, D-197)
    inputs = dn.load_inputs(ROOT, queue, categories=list(reader_categories.READER_CATEGORIES),
                            composition_runs=True, dsr_basis=None)
    seen = [b["block_id"] for b in inputs["composition"]["registry"]["blocks"]]
    all_ids = [b["block_id"] for b in raw["blocks"]]
    voided = sorted(br.voided_block_ids(raw))
    print(f"registry file: revision {raw['revision']}, {len(all_ids)} blocks")
    for bid in all_ids:
        print(f"  file block: {bid}")
    for rec in raw.get("statuses") or []:
        print(f"  status record: {rec['block_id']} -> {rec['status']} (by {rec['by']}, {rec['at']})")
    print("composition input (inputs['composition']['registry']):")
    for bid in all_ids:
        print(f"  {bid}: {'ACTIVE (listed)' if bid in seen else 'EXCLUDED (voided)' if bid in voided else 'MISSING'}")
    print(f"registry_revision seen by decide-next: {inputs['registry_revision']}")


if __name__ == "__main__":
    main()
