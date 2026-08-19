"""
E-025 S4 PR-1 -- unit tests for the pure `union_merge_trial_ledgers` function
in deflate_sharpe.py (the trial_sharpes list-region union of the dual-writer
merge). Synthetic dict fixtures only: no market data, no git, no I/O.

Pins D2-D4 of research/E025_S4_DESIGN_v5.md:
  - a = master (order preserved), b = fork; append-only union on (trial_id, source)
  - shared-ancestor rows kept once; a genuinely divergent shared row REFUSES
  - canonical equality is per-field with a NaN-pair carve-out
  - never aliases/mutates inputs; postcondition = no duplicate (trial_id, source)
"""

import copy
import math
import sys
from pathlib import Path

import pytest

TOOLS_PATH = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(TOOLS_PATH))

import deflate_sharpe as ds  # noqa: E402


# ---------------------------------------------------------------------------
# Row factories -- fresh objects each call so a and b never share references
# ---------------------------------------------------------------------------

def _counted(trial_id, sharpe, fh):
    return {
        "trial_id": trial_id,
        "source": "backtest",
        "statistic_valid": "sharpe",
        "sharpe": sharpe,
        "forecast_hash": fh,
    }


def _prescreen(trial_id, fh, source="prescreen"):
    return {
        "trial_id": trial_id,
        "source": source,
        "statistic_valid": "neither",
        "sharpe": None,
        "forecast_hash": fh,
    }


def _shared_base():
    # one COUNTED row + neither (prescreen) rows + one prescreen_backfill row
    return [
        _counted("run_030", -0.6375, "h_030"),
        _prescreen("run_030", "h_030p"),
        _prescreen("run_031", "h_031p"),
        _prescreen("run_041", "h_041b", source="prescreen_backfill"),
    ]


# ---------------------------------------------------------------------------
# Test 1 -- two divergent ledgers union into base-once + all 4 novel rows
# ---------------------------------------------------------------------------

def test_union_merge_two_divergent_ledgers():
    a = [
        *_shared_base(),
        _prescreen("run_045", "h_045p"),
        _counted("run_045", 0.3, "h_045b"),
    ]
    b = [
        *copy.deepcopy(_shared_base()),
        _prescreen("run_d_007", "h_d007p"),
        {
            "trial_id": "run_d_007",
            "source": "backtest_failed",
            "statistic_valid": "neither",
            "sharpe": None,
            "forecast_hash": None,
        },
    ]

    merged = ds.union_merge_trial_ledgers(a, b)

    # base counted once (4 shared rows), plus 2 master-novel + 2 fork-novel
    assert len(merged) == len(_shared_base()) + 4

    keys = {(r["trial_id"], r["source"]) for r in merged}
    assert ("run_045", "prescreen") in keys
    assert ("run_045", "backtest") in keys
    assert ("run_d_007", "prescreen") in keys
    assert ("run_d_007", "backtest_failed") in keys

    ds.check_no_duplicate_trial_ids(merged)  # postcondition holds

    # explicit pinned literals, each counted once -- NOT a concat comparison
    assert ds.load_sharpe_trials({"trial_sharpes": merged})[0] == [-0.6375, 0.3]


# ---------------------------------------------------------------------------
# Test 2 -- a genuinely divergent shared row refuses
# ---------------------------------------------------------------------------

def test_union_merge_refuses_true_collision():
    a = [_counted("run_045", 0.3, "h_045b")]
    b = [_counted("run_045", 0.9, "h_045b_alt")]

    with pytest.raises(ValueError) as exc:
        ds.union_merge_trial_ledgers(a, b)

    msg = str(exc.value)
    assert "run_045" in msg and "backtest" in msg  # names the key
    assert "sharpe" in msg  # names the differing field


# ---------------------------------------------------------------------------
# Test 3 -- append-only; inputs untouched; no aliasing
# ---------------------------------------------------------------------------

def test_union_merge_is_append_only():
    a = [*_shared_base(), _counted("run_045", 0.3, "h_045b")]
    b = [_prescreen("run_d_007", "h_d007p")]
    a_snapshot = copy.deepcopy(a)
    b_snapshot = copy.deepcopy(b)

    merged = ds.union_merge_trial_ledgers(a, b)

    # a's rows come first, in a-order, content-equal
    assert merged[: len(a)] == a
    # inputs unchanged by the call
    assert a == a_snapshot
    assert b == b_snapshot
    # mutating a merged row must not reach back into a or b (deepcopy, no alias)
    merged[0]["sharpe"] = 999.0
    assert a == a_snapshot
    assert b == b_snapshot


# ---------------------------------------------------------------------------
# Test 4 -- same trial_id, different source, straddling both sides: keep both
# ---------------------------------------------------------------------------

def test_union_merge_keeps_second_source_row_for_same_trial_id():
    a = [_prescreen("run_d_007", "h_d007p")]
    b = [_counted("run_d_007", 0.42, "h_d007b")]

    merged = ds.union_merge_trial_ledgers(a, b)

    same_id = [r for r in merged if r["trial_id"] == "run_d_007"]
    assert len(same_id) == 2
    assert {r["source"] for r in same_id} == {"prescreen", "backtest"}


# ---------------------------------------------------------------------------
# Test 5 -- identical rows on both sides collapse to one, no refuse
# ---------------------------------------------------------------------------

def test_union_merge_tolerates_shared_ancestor_rows():
    a = [_counted("run_030", -0.6375, "h_030")]
    b = [_counted("run_030", -0.6375, "h_030")]

    merged = ds.union_merge_trial_ledgers(a, b)

    assert len(merged) == 1
    assert merged[0]["trial_id"] == "run_030"


# ---------------------------------------------------------------------------
# Test 6 -- byte-identical shared row carrying NaN is not falsely refused
# ---------------------------------------------------------------------------

def test_union_merge_shared_row_with_nan_sharpe_not_false_refused():
    row_a = _counted("run_030", float("nan"), "h_030")
    row_b = _counted("run_030", float("nan"), "h_030")
    # sanity: a naive whole-dict == would call these unequal (NaN != NaN)
    assert row_a != row_b

    merged = ds.union_merge_trial_ledgers([row_a], [row_b])

    assert len(merged) == 1
    assert math.isnan(merged[0]["sharpe"])


# ---------------------------------------------------------------------------
# Test 7 -- order is a's rows (a-order) then b's novel rows (b-order)
# ---------------------------------------------------------------------------

def test_union_merge_preserves_order_a_then_b():
    a = [
        _counted("run_030", -0.6375, "h_030"),
        _prescreen("run_030", "h_030p"),
    ]
    b = [
        _prescreen("run_d_007", "h_d007p"),
        _counted("run_d_007", 0.42, "h_d007b"),
    ]

    merged = ds.union_merge_trial_ledgers(a, b)

    assert [(r["trial_id"], r["source"]) for r in merged] == [
        ("run_030", "backtest"),
        ("run_030", "prescreen"),
        ("run_d_007", "prescreen"),
        ("run_d_007", "backtest"),
    ]
