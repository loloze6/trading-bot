"""
F4d wiring: a pre-registered significance_methodology must GOVERN the run, not
merely be audited after it.

Guards the second run_060 halt of 2026-08-28. The brief pinned
machine_constraints.significance_methodology=episode_blocked_a851a, but
prescreen_signal.py reads that flag only from candidate_strategy_config.json
(`config_raw.get("significance_methodology")`) and nothing carried the value
across. The backtest_specification agent had not written the field, so the
a851a branch never ran, the default block-Fisher path ran instead, and the
conformance gate correctly halted the campaign.

The gate is the audit; _ensure_significance_methodology_pinned is the wiring.
Without the wiring the pin is a statement no code acts on, and each run has to
be repaired by hand after the gate catches it.
"""
import json
import random
import sys
from pathlib import Path

import pytest

_SR = Path(__file__).parent.parent
sys.path.insert(0, str(_SR / "workflow"))
sys.path.insert(0, str(_SR / "tools"))

import run_phase1_research as rpr  # noqa: E402


def _config(tmp_path, **extra):
    p = tmp_path / "candidate_strategy_config.json"
    p.write_text(json.dumps(
        {"aux_feeds": [], "regime_detector": {}, "strategies": {}, **extra}), encoding="utf-8")
    return p


def test_pin_is_propagated_into_the_config(tmp_path):
    """The exact run_060 case: pinned in the brief, absent from the config."""
    cfg = _config(tmp_path)
    assert "significance_methodology" not in json.loads(cfg.read_text(encoding="utf-8"))

    wrote = rpr._ensure_significance_methodology_pinned(
        cfg, {"significance_methodology": "episode_blocked_a851a"}, "run_test")

    assert wrote is True
    assert json.loads(cfg.read_text(encoding="utf-8"))["significance_methodology"] \
        == "episode_blocked_a851a"


def test_it_is_idempotent(tmp_path):
    """run_loop() re-enters a run repeatedly; a conforming config is left alone."""
    cfg = _config(tmp_path, significance_methodology="episode_blocked_a851a")
    before = cfg.read_text(encoding="utf-8")
    wrote = rpr._ensure_significance_methodology_pinned(
        cfg, {"significance_methodology": "episode_blocked_a851a"}, "run_test")
    assert wrote is False
    assert cfg.read_text(encoding="utf-8") == before


def test_a_conflicting_config_raises_rather_than_being_overwritten(tmp_path):
    """Two deliberate, contradictory statements. Silently preferring either one
    is how a run ends up testing something nobody registered."""
    cfg = _config(tmp_path, significance_methodology="something_else")
    with pytest.raises(RuntimeError, match="conflicting"):
        rpr._ensure_significance_methodology_pinned(
            cfg, {"significance_methodology": "episode_blocked_a851a"}, "run_test")
    assert json.loads(cfg.read_text(encoding="utf-8"))["significance_methodology"] \
        == "something_else", "the config must be left untouched"


def test_no_pin_is_a_no_op(tmp_path):
    """Briefs without machine_constraints keep their existing behaviour exactly."""
    cfg = _config(tmp_path)
    before = cfg.read_text(encoding="utf-8")
    assert rpr._ensure_significance_methodology_pinned(cfg, {}, "run_test") is False
    assert cfg.read_text(encoding="utf-8") == before


def test_a_pin_with_no_config_raises(tmp_path):
    """Enforcing a pin on a config that was never written is not something to
    paper over -- it means the preceding stage did not deliver."""
    with pytest.raises(FileNotFoundError):
        rpr._ensure_significance_methodology_pinned(
            tmp_path / "missing.json",
            {"significance_methodology": "episode_blocked_a851a"}, "run_test")


def test_the_pinned_value_actually_reaches_the_prescreen_branch(tmp_path):
    """End to end on the contract that matters: after propagation, the flag is
    where prescreen_signal.py looks for it. The a851a branch is gated on
    exactly this expression."""
    cfg = _config(tmp_path)
    rpr._ensure_significance_methodology_pinned(
        cfg, {"significance_methodology": "episode_blocked_a851a"}, "run_test")
    config_raw = json.loads(cfg.read_text(encoding="utf-8"))
    assert config_raw.get("significance_methodology") == "episode_blocked_a851a"


# ---------------------------------------------------------------------------
# The methodology LABEL now tracks the block size it was computed with.
# ---------------------------------------------------------------------------

def test_label_is_unchanged_at_1h_so_the_archive_reproduces():
    """block_24_fisher_z was hardcoded. Deriving it must not rename a single
    archived 1h result: at 1h the derived block size is 24, so the label is
    byte-identical."""
    from timeframe import bars_per_day
    assert f"block_{bars_per_day('1h')}_fisher_z" == "block_24_fisher_z"


def test_label_tracks_the_block_size_on_other_timeframes():
    """A 4h run used to stamp 'block_24' into its artifact while dividing by 6.
    The label is what a later reader reconstructs the method from."""
    from timeframe import bars_per_day
    assert f"block_{bars_per_day('4h')}_fisher_z" == "block_6_fisher_z"
    assert f"block_{bars_per_day('1d')}_fisher_z" == "block_1_fisher_z"


def test_a_derived_label_is_still_not_an_a851a_outcome():
    """The conformance gate detects 'the a851a flag was ignored' by checking
    membership in episode_significance.VALID_METHODS. Renaming the default label
    must not accidentally make it look like a valid a851a outcome."""
    import episode_significance as es
    from timeframe import bars_per_day
    for tf in ("1h", "4h", "1d", "15m"):
        assert f"block_{bars_per_day(tf)}_fisher_z" not in es.VALID_METHODS


# ---------------------------------------------------------------------------
# CUL-51: the dense-fallback method LABEL tracks the block size it divided by,
# the conformance gate accepts that derived family, and block_size is no longer
# silently defaulted to 24.
# ---------------------------------------------------------------------------


def _dense_records(n=400, active_frac=0.6, seed=17):
    """Records dense enough (>=50% active) to route to the block dense-fallback
    branch, with mixed forecast/return values (not a vacuous uniform fixture)
    and enough active bars that even block_size=96 (15m) is smaller than the
    active sample."""
    rng = random.Random(seed)
    recs = []
    for i in range(n):
        active = rng.random() < active_frac
        base = rng.uniform(-1.0, 1.0) if active else 0.0
        ret = 25.0 * base + rng.gauss(0.0, 40.0)
        recs.append({
            "active": active,
            "forecast": base,
            "next_return_bps": ret,
            "symbol": "BTCUSDT",
            "timestamp": i,
        })
    return recs


def test_dense_fallback_label_tracks_the_block_size():
    """The label stamped into the artifact must name the block size actually
    divided by — block_6 at 4h, not the old hardcoded block_24."""
    import episode_significance as es
    result = es.compute_a851a_significance(_dense_records(), block_size=6)
    assert result["method"] == "block_6_dense_fallback"
    assert result["density_pct"] >= 50.0


def test_dense_fallback_label_is_unchanged_at_1h():
    """At 1h the derived block size is 24, so the label is byte-identical to the
    old literal and the entire 1h archive still reproduces."""
    import episode_significance as es
    from timeframe import bars_per_day
    result = es.compute_a851a_significance(_dense_records(), block_size=bars_per_day("1h"))
    assert result["method"] == "block_24_dense_fallback"


def test_derived_dense_fallback_is_accepted_by_the_conformance_gate():
    """The F5 trap: deriving the label without widening the gate's acceptance
    from a closed set to a predicate converts a cosmetic misreport into a hard
    conformance halt on every non-1h run. A 4h block_6_dense_fallback is a
    legitimate A8.5.1a outcome and must pass the gate with zero violations."""
    constraints = {"significance_methodology": "episode_blocked_a851a"}
    result = {"significance_methodology_used": "block_6_dense_fallback"}
    violations = rpr._check_prescreen_conformance(result, constraints, {})
    assert violations == []


def test_fisher_z_is_still_not_an_a851a_outcome_under_the_predicate():
    """The widened acceptance must stay narrow enough that block_<n>_fisher_z —
    prescreen_signal.py's OLD default, the 'a851a flag was ignored' signal — is
    still rejected for every block size."""
    import episode_significance as es
    from timeframe import bars_per_day
    for tf in ("1h", "4h", "1d", "15m"):
        assert not es.is_a851a_method(f"block_{bars_per_day(tf)}_fisher_z")


def test_block_size_is_not_silently_defaulted():
    """The removed `block_size=24` default was the CUL-9/CUL-51 bug class — a
    silent 24 that mislabels and misdivides every non-1h run. Omitting it must
    fail loud, not assume 24."""
    import episode_significance as es
    with pytest.raises(ValueError):
        es.compute_a851a_significance(_dense_records())
