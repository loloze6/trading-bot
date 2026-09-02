"""
E-041: regression guard for the real campaign_config.yaml flag values.

WHY THIS EXISTS
---------------
E-041's decision (Jerémy, 2026-09-01): a finished, tested feature defaults
ON; staying off needs a stated reason. The eight flags are being switched on
one at a time, each in its own commit -- this file is the accumulating
regression guard so a flag switched on cannot silently drift back to off
without the suite noticing. It reads the REAL config file, not a sandboxed
copy (test_exclusion_digest_input.py and its siblings already prove each
flag's on/off BEHAVIOR against a sandboxed ROOT; this file only pins which
value the real repo ships).

This is deliberately a small, flat file rather than E-041 S2's planned
register+test (owner, criterion, mechanically checked against the code) --
that is a bigger piece of work, not yet built. Until it exists, add one
function here per flag switched on.
"""
from __future__ import annotations

from pathlib import Path

import yaml

_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "campaign_config.yaml"


def _load_orchestrator_flags() -> dict:
    with open(_CONFIG_PATH, encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    return cfg.get("orchestrator") or {}


def test_exclusion_digest_input_is_on() -> None:
    """Switched on 2026-09-02 (E-041, flag 2 of 7). See campaign_config.yaml's
    own comment for the declared-output-change note."""
    flags = _load_orchestrator_flags()
    assert flags.get("exclusion_digest_input", {}).get("enabled") is True, (
        "orchestrator.exclusion_digest_input.enabled reverted to off. This was "
        "switched on deliberately (E-041) -- if reverting was intentional, "
        "update this test with the reason; if not, this is the regression."
    )
