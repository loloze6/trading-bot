"""
Gap-awareness tests for episode_significance.identify_episodes (CUL-21 / GH#66,
the #50 family). Pre-registered in
docs/analysis-reports/PRESCREEN_GAP_EPISODE_POLICY.md.

An episode gap is measured in TRUE elapsed bars (from timestamps), not list
positions: a data hole between two active bars adds its missing bars to the gap,
so a large enough hole splits an episode a positional count silently merges.

DIRECTION (corrected against the pre-registration by execution, session 25):
true_gap >= positional_gap for every pair, so the gap-aware split set is a
SUPERSET of the positional one -> n_episodes is monotonic NON-DECREASING; the
fix can only RAISE n_episodes (correcting an understatement) or leave it equal,
never lower it. EPISODE_POLICY §5/§6 stated the opposite ("down / never rise")
and are inverted; the kill criterion here is "n_episodes never FALLS".

`expected_step=None` reproduces the positional behaviour byte-for-byte.
A symbol boundary in the pooled record list stays on the positional gap
(observation O1 is out of scope and untouched).
"""

import inspect
import random
import sys
from pathlib import Path

import pandas as pd

TOOLS_PATH = Path(__file__).parent.parent / "tools"
if str(TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(TOOLS_PATH))

import episode_significance as es
import run_protocol as rp

_STEP = pd.Timedelta(1, unit="h")
_BASE = pd.Timestamp("2020-01-01 00:00:00")


def _recs(active_flags, holes=None, symbol=None, start_h=0):
    """Per-bar records. `holes` = {index: missing_bars}: after that index the
    timestamp jumps (1 + missing_bars) steps, so `missing_bars` bars are absent
    from the list (a data hole). `start_h` offsets the first timestamp."""
    holes = holes or {}
    recs, h = [], start_h
    for i, a in enumerate(active_flags):
        r = {
            "active": bool(a),
            "timestamp": _BASE + pd.Timedelta(h, unit="h"),
            "forecast": 10.0 if a else 0.0,
            "next_return_bps": float(i),
        }
        if symbol is not None:
            r["symbol"] = symbol
        recs.append(r)
        h += 1 + holes.get(i, 0)
    return recs


def test_identify_episodes_none_is_positional():
    """expected_step=None equals the default (positional) partition on a gappy
    fixture -- the hole is invisible to the None path."""
    recs = _recs([1, 1, 0, 1, 1], holes={1: 10})
    assert es.identify_episodes(recs, gap_bars=2, expected_step=None) == es.identify_episodes(recs, gap_bars=2)
    assert es.identify_episodes(recs, gap_bars=2, expected_step=None) == [[0, 1, 3, 4]]


def test_identify_episodes_hole_splits_merged_episode():
    """Two active bars a small positional distance apart but separated by a data
    hole: positional merges them, gap-aware splits -- exactly one more episode."""
    recs = _recs([1, 1, 0, 1, 1], holes={1: 10})
    pos = es.identify_episodes(recs, gap_bars=2, expected_step=None)
    gap = es.identify_episodes(recs, gap_bars=2, expected_step=_STEP)
    assert pos == [[0, 1, 3, 4]]  # positional gap idx1->idx3 is 1 <= 2 -> merged
    assert gap == [[0, 1], [3, 4]]  # true gap across the hole is 11 > 2 -> split
    assert len(gap) == len(pos) + 1


def test_identify_episodes_same_segment_unchanged():
    """Two active bars in the same contiguous segment (inactive bars between, no
    hole) partition identically with and without expected_step."""
    recs = _recs([1, 0, 0, 1])  # contiguous, positional gap 2
    assert (
        es.identify_episodes(recs, gap_bars=2, expected_step=_STEP)
        == es.identify_episodes(recs, gap_bars=2, expected_step=None)
        == [[0, 3]]
    )


def test_identify_episodes_era_and_gap_compose():
    """An era break and a data hole on the same pair produce exactly one split,
    not two."""
    recs = _recs([1, 1], holes={0: 10}, symbol="S")

    def era(i):
        return 0 if i == 0 else 1

    ep = es.identify_episodes(recs, gap_bars=2, era_of=era, expected_step=_STEP)
    assert ep == [[0], [1]]
    assert len(ep) == 2


def test_identify_episodes_n_episodes_never_falls_on_gappy():
    """Kill criterion (corrected): n_episodes is monotonic non-decreasing --
    gap-awareness can only raise it or leave it equal, never lower it."""
    rng = random.Random(20260903)
    flags = [rng.random() < 0.5 for _ in range(200)]
    holes = {i: rng.choice([0, 0, 0, 5, 50]) for i in range(200)}
    recs = _recs(flags, holes=holes, symbol="S")
    pos = len(es.identify_episodes(recs, gap_bars=48, expected_step=None))
    gap = len(es.identify_episodes(recs, gap_bars=48, expected_step=_STEP))
    assert gap >= pos, f"gap-aware n_episodes fell: {gap} < {pos}"


def test_identify_episodes_cross_symbol_boundary_unchanged():
    """Observation O1 stays untouched: a symbol boundary in the pooled record
    list keeps the positional gap even with expected_step set, so the pooled
    cross-symbol behaviour is byte-identical. Symbol B starts far later in time,
    so without the same-symbol guard the boundary would wrongly split."""
    recs = _recs([1, 1], symbol="A") + _recs([1, 1], symbol="B", start_h=100)
    with_step = es.identify_episodes(recs, gap_bars=2, expected_step=_STEP)
    without = es.identify_episodes(recs, gap_bars=2, expected_step=None)
    assert with_step == without == [[0, 1, 2, 3]]


def test_a851a_min_n_episodes_gate_moves_with_gap():
    """End-to-end through compute_a851a_significance: a fixture whose gap-aware
    n_episodes crosses min_n_episodes selects a different method branch than the
    positional count did (drives the wiring, per PR #65's isolation lesson)."""
    recs = _recs([1] * 8 + [0], holes={i: 50 for i in range(7)}, symbol="S")

    def _run(step):
        return es.compute_a851a_significance(
            recs,
            gap_bars=2,
            density_fallback_pct=100.0,
            min_n_episodes=8,
            block_size=2,
            n_resamples=50,
            seed=0,
            expected_step=step,
        )

    pos = _run(None)
    gap = _run(_STEP)
    assert pos["n_episodes"] == 1
    assert gap["n_episodes"] == 8
    assert pos["method"] == "episode_bootstrap_insufficient_n"
    assert gap["method"] != "episode_bootstrap_insufficient_n"


def test_episode_wiring_passes_expected_step():
    """PR #65 isolation lesson: guard the production call site. Relocated to
    run_protocol.py's _a851a_episode_significance (CUL-265, E-039 step 5) --
    the post-backtest home for this significance method now that the
    signal_prescreen stage it originally lived in is removed. It must pass
    the scalar step into compute_a851a_significance or gap-awareness silently
    turns off in production with unit tests still green."""
    src = inspect.getsource(rp._a851a_episode_significance)
    assert src.count("expected_step=episode_expected_step") == 1
