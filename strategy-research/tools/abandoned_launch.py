"""
abandoned_launch.py -- E-061 C1.4 (fourth-round review fix 9).

A run dir left behind by a launch that raised before run_loop
(run_campaign._halt_launch_exception) is marked `status: abandoned_launch` in
its pipeline_state.yaml. It spent nothing, belongs to no lineage and must not
count as campaign knowledge: every scanner that walks runs/run_* for that
knowledge skips it through is_abandoned_launch (build_exclusion_digest,
near_miss_scoreboard, replay_repeat_gate; run_campaign's reconcile_orphans
treats it as known). Run-id allocation still sees the directory, so its
number is never reused.

Dependency-light (yaml only), importable from tools/ and workflow/ alike.
"""
from __future__ import annotations

from pathlib import Path

import yaml

ABANDONED_LAUNCH_STATUS = "abandoned_launch"


def is_abandoned_launch(run_dir) -> bool:
    """True when run_dir/pipeline_state.yaml reads status: abandoned_launch.
    An absent or unreadable state is not an abandoned launch."""
    path = Path(run_dir) / "pipeline_state.yaml"
    try:
        state = yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else None
    except Exception:  # noqa: BLE001 -- an unreadable state is simply not ours
        return False
    return isinstance(state, dict) and state.get("status") == ABANDONED_LAUNCH_STATUS
