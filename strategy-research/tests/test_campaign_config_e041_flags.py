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


def test_stale_input_path_fix_is_on() -> None:
    """Switched on 2026-09-02 (E-041, flag 3 of 7). See campaign_config.yaml's
    own comment for the declared-output-change note."""
    flags = _load_orchestrator_flags()
    assert flags.get("stale_input_path_fix", {}).get("enabled") is True, (
        "orchestrator.stale_input_path_fix.enabled reverted to off. This was "
        "switched on deliberately (E-041) -- if reverting was intentional, "
        "update this test with the reason; if not, this is the regression."
    )


def test_variant_selection_record_is_on() -> None:
    """Switched on 2026-09-02 (E-041, flag 4 of 7). See campaign_config.yaml's
    own comment for the declared-output-change note and the compliance check
    behind this call."""
    flags = _load_orchestrator_flags()
    assert flags.get("variant_selection_record", {}).get("enabled") is True, (
        "orchestrator.variant_selection_record.enabled reverted to off. This "
        "was switched on deliberately (E-041) -- if reverting was "
        "intentional, update this test with the reason; if not, this is the "
        "regression."
    )


def test_schedulability_block_is_on() -> None:
    """Switched on 2026-09-02 (E-041, flag 5 of 7). See campaign_config.yaml's
    own comment for the declared-output-change note."""
    flags = _load_orchestrator_flags()
    assert flags.get("schedulability_block", {}).get("enabled") is True, (
        "orchestrator.schedulability_block.enabled reverted to off. This was "
        "switched on deliberately (E-041) -- if reverting was intentional, "
        "update this test with the reason; if not, this is the regression."
    )


def test_anti_adjacency_retry_is_still_off() -> None:
    """INCOMPLETE, not merely not-yet-done -- and not a build gap. E-036's
    fix (composition-fingerprint adjacency, REPEAT/NEIGHBOUR/NOVEL) shipped
    2026-08-27, is built, tested, and measured working exactly as designed
    (2.4-2.8x more distinct strategies correctly recognised). Jerémy
    REJECTED the design itself on review 2026-09-02: given the real strategy
    structure (a regime detector, mapping to per-regime sub-strategies, each
    a weighted composition of components), a flat fingerprint of
    (regime, component, params, weight) is not a convincing answer to "are
    these two strategies the same idea" -- see E-036/EPIC.md's rejection
    entry for the full argument. Unpark trigger: E-036 is deliberately
    restarted with a reconsidered design, not merely re-reviewed."""
    flags = _load_orchestrator_flags()
    assert flags.get("anti_adjacency_retry", {}).get("enabled") is not True, (
        "orchestrator.anti_adjacency_retry.enabled was turned on, but E-036's "
        "design was rejected by Jerémy (2026-09-02), not merely incomplete -- "
        "confirm E-036 has been deliberately restarted with a new design "
        "before removing this guard."
    )


def test_variant_anti_adjacency_gate_is_still_off() -> None:
    """INCOMPLETE for the same reason as anti_adjacency_retry above -- both
    are call sites of the same tools/anti_adjacency_gate.py mechanism and the
    same rejected fingerprint design."""
    flags = _load_orchestrator_flags()
    assert flags.get("variant_anti_adjacency_gate", {}).get("enabled") is not True, (
        "orchestrator.variant_anti_adjacency_gate.enabled was turned on, but "
        "E-036's design was rejected by Jerémy (2026-09-02). Confirm E-036 "
        "has been deliberately restarted with a new design before removing "
        "this guard."
    )
