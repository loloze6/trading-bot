"""
Regression suite — fork issue #36 (dedup collapses prescreen+backtest rows).

deduplicate_trials keyed on forecast_hash ALONE. Once forecast_hash is populated
(post-S1), a single run's prescreen row and backtest row share the same
forecast_hash and collide — dedup drops one, silently removing the backtest
Sharpe from the deflated-Sharpe N (N feeds the single-use holdout gate). Fix:
key dedup on (forecast_hash, source), matching the read-side guard's
(trial_id, source) convention (deflate_sharpe.py::check_no_duplicate_trial_ids).

Null-hash rows stay always-kept (today's live ledger is all null-hash), so the
change is a byte-exact no-op on every existing row and only changes behaviour for
the future hashed-collision case.
"""

import sys
from pathlib import Path

TOOLS_PATH = Path(__file__).parent.parent / "tools"
sys.path.insert(0, str(TOOLS_PATH))

import deflate_sharpe as ds  # noqa: E402


def test_prescreen_and_backtest_rows_both_survive_dedup():
    """#36 regression: a run's prescreen + backtest rows carry the SAME
    forecast_hash but differ by source; both must survive so the backtest Sharpe
    reaches the DSR sample. RED under the forecast_hash-only key (n_removed==1)."""
    shared = "run_042_forecast_deadbeef"
    prescreen = {
        "trial_id": "run_042",
        "source": "prescreen",
        "sharpe": None,
        "forecast_hash": shared,
        "statistic_valid": "expectancy",
    }
    backtest = {
        "trial_id": "run_042",
        "source": "backtest",
        "sharpe": 1.37,
        "forecast_hash": shared,
        "statistic_valid": "sharpe",
        "n_trades": 120,
    }

    kept, n_removed = ds.deduplicate_trials([prescreen, backtest])

    assert n_removed == 0, (
        "prescreen and backtest rows of one run share a forecast_hash but differ "
        f"by source — neither is a duplicate; got n_removed={n_removed}"
    )
    assert len(kept) == 2
    assert any(r["source"] == "backtest" and r["sharpe"] == 1.37 for r in kept), (
        "the backtest Sharpe row must survive dedup — it feeds the DSR sample"
    )


def test_same_hash_same_source_still_deduped():
    """The fix must still collapse a GENUINE duplicate: identical forecast_hash
    AND identical source (a dual-writer race or replayed row)."""
    shared = "keltner_v1_forecast_abc123"
    a = {
        "trial_id": "run_a",
        "source": "backtest",
        "forecast_hash": shared,
        "sharpe": 1.0,
    }
    b = {
        "trial_id": "run_b",
        "source": "backtest",
        "forecast_hash": shared,
        "sharpe": 1.0,
    }

    kept, n_removed = ds.deduplicate_trials([a, b])

    assert n_removed == 1
    assert len(kept) == 1


def test_null_hash_rows_are_byte_identical_noop():
    """No-op guarantee: today's live ledger is all null forecast_hash. Every row
    stays, in order, N unchanged — proving the fix does not perturb existing
    campaign_state (Jeremy validated N=14 byte-identical on the live ledger)."""
    records = [
        {"trial_id": f"run_{i:03d}", "source": "backtest", "sharpe": float(i)}
        for i in range(14)
    ]

    kept, n_removed = ds.deduplicate_trials(records)

    assert n_removed == 0
    assert len(kept) == 14
    assert kept == records
