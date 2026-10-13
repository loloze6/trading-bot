"""D-124 (operator, 2026-10-13): the trial ledger's dedupe key holds the row's `fold`, so the
same config backtested on another fold -- an operator re-run (D-122) -- is its own trial,
with its own deflated Sharpe, instead of collapsing onto the first fold's row (found on
run_090 / run_091, the refolds of run_089: "dedup_collapse ... onto trial 'run_089'").
Rows without a fold dedupe exactly as before.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

SR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SR / "tools"))
sys.path.insert(0, str(SR / "workflow"))

import run_phase1_research as rpr  # noqa: E402
from deflate_sharpe import deduplicate_trials, select_same_basis_sample  # noqa: E402

H = "27c31dff" * 8


def _row(tid, **kw):
    return {"trial_id": tid, "source": "backtest", "statistic_valid": "sharpe", "sharpe": 1.0,
            "forecast_hash": H, **kw}


@pytest.mark.parametrize("dedupe", [deduplicate_trials, rpr._dedupe_trials])
def test_the_same_config_on_three_folds_is_three_trials(dedupe):
    rows = [_row("run_089", fold="B"), _row("run_090", fold="C"), _row("run_091", fold="D")]
    kept, removed = dedupe(rows)
    assert [r["trial_id"] for r in kept] == ["run_089", "run_090", "run_091"] and removed == 0


@pytest.mark.parametrize("dedupe", [deduplicate_trials, rpr._dedupe_trials])
def test_the_same_config_on_the_same_fold_still_collapses(dedupe):
    kept, removed = dedupe([_row("run_089", fold="B"), _row("run_092", fold="B")])
    assert [r["trial_id"] for r in kept] == ["run_089"] and removed == 1


@pytest.mark.parametrize("dedupe", [deduplicate_trials, rpr._dedupe_trials])
def test_rows_without_a_fold_dedupe_as_before(dedupe):
    kept, removed = dedupe([_row("run_070"), _row("run_071")])
    assert removed == 1
    # a fold row never collapses onto a row without one (N can only be over-counted)
    kept, removed = dedupe([_row("run_070"), _row("run_090", fold="C")])
    assert removed == 0


@pytest.mark.parametrize("dedupe", [deduplicate_trials, rpr._dedupe_trials])
@pytest.mark.parametrize("bad", [None, "", 3])
def test_a_malformed_fold_raises(dedupe, bad):
    with pytest.raises(ValueError, match="D-124"):
        dedupe([_row("run_090", fold=bad)])


def test_the_sample_n_counts_each_fold():
    rows = [_row("run_089", fold="B"), _row("run_090", fold="C"), _row("run_091", fold="D")]
    assert select_same_basis_sample(rows)["N"] == 3


def test_a_refold_row_is_no_longer_named_as_collapsed_onto_its_source():
    rows = [_row("run_089", fold="B"), _row("run_090", fold="C")]
    assert rpr._dedup_collapse_target({"rows": rows}, rows[1]) == "another ledger row"
    same = [_row("run_089", fold="B"), _row("run_092", fold="B")]
    assert rpr._dedup_collapse_target({"rows": same}, same[1]) == (
        "trial 'run_089' (same forecast_hash, coins, window fingerprint, fold and source)")
