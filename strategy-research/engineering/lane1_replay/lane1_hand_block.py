"""Lane 1's hand record (D-128): print the registry block for run_084 (SMA 100, fold B) as YAML.

READ ONLY. Writes nothing: it reads the operator checkout's campaign_memory.yaml, runs/run_084 and
campaign_record/block_registry.yaml, builds the block with the registry's own `build_block`
(tools/block_registry.py), and prints the YAML to append under `blocks:` plus the new `revision`.

Usage (from the operator checkout's strategy-research/, code at master):
    ../venv/Scripts/python.exe engineering/lane1_replay/lane1_hand_block.py

Two things differ from a grid registration, both because run_084's stored memory entry is
`refuted` (cells: INCONCLUSIVE, FAIL), which `build_block` refuses (its cell loop requires PASS):
  * the entry copy handed to `build_block` has an EMPTY grid (no criterion, no variant, no cell),
    so `criteria_passed`, `variants_passed` and `numbers` are empty: no grid criterion passed;
  * `timeframe` / `timeframe_category` are the two fields the loader allows next to the fixed list
    (written together); without them composition excludes the block ("no timeframe recorded").
    The values are the run's own protocol timeframe, `1d`, category `daily`.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "tools"))

import block_registry as br  # noqa: E402
import composite_cache as cc  # noqa: E402

RUN_ID = "run_084"


def main() -> None:
    memory = yaml.safe_load((ROOT / "campaign_record" / "campaign_memory.yaml").read_text(encoding="utf-8"))
    entry = dict(memory["runs"][RUN_ID])
    entry["grid"] = {**entry["grid"], "criteria": [], "variants": [], "cells": {}}
    run_dir = ROOT / "runs" / RUN_ID
    manifest = br.load_manifest(run_dir)
    block = br.build_block(run_dir, entry, manifest, root=ROOT)
    protocol_ref = entry["protocol_ref"]
    timeframe = json.loads((ROOT / protocol_ref).read_text(encoding="utf-8")).get("timeframe")
    block["timeframe"] = timeframe
    block["timeframe_category"] = cc.timeframe_category(timeframe)
    registry = br.load_registry(ROOT / "campaign_record" / "block_registry.yaml")
    new_revision = registry["revision"] + 1
    existing = [b["block_id"] for b in registry["blocks"]]
    if block["block_id"] in existing:
        raise SystemExit(f"{block['block_id']} is already registered")
    # the loader's own checks, on the document as it would read after the edit (a temp file
    # outside every repo; the registry itself is never written)
    doc = {**registry, "revision": new_revision, "blocks": registry["blocks"] + [block]}
    with tempfile.TemporaryDirectory() as tmp:
        probe = Path(tmp) / "block_registry.yaml"
        probe.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
        br.load_registry(probe)
    print(f"# loader accepts the edited registry: {block['block_id']}")
    print(f"# registry now: revision {registry['revision']}, {len(existing)} blocks; after: revision {new_revision}")
    print("# --- set `revision:` to", new_revision, "and append this item under `blocks:` ---")
    print(yaml.safe_dump([block], sort_keys=False))


if __name__ == "__main__":
    main()
