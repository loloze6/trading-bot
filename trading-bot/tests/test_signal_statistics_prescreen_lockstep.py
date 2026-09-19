"""
E-039 step 5: performance.signal_statistics's ported
pooled_block_adjusted_significance/stationary_block_bootstrap_ic_significance,
pinned-value contract tests.

Originally a lockstep comparison against prescreen_signal.py's originals,
proving the port (CUL-262/264/E-039 step 5 Phase 1) was algorithmically
faithful before prescreen_signal.py was removed (2026-09-12, E-039 step 5
Phase 3) and its dependents (episode_significance.py, run_protocol.py,
whale_footprint_evaluation.py) were repointed here. That comparison's job is
done -- prescreen_signal.py no longer exists to compare against -- so this
file now pins the values the lockstep run last confirmed correct, as a
regression guard on signal_statistics.py itself.

contiguous_segments has its own direct contract tests in
strategy-research/tests/test_contiguous_segments.py; not duplicated here.
"""
import sys
from pathlib import Path

TRADING_BOT_ROOT = Path(__file__).parent.parent
if str(TRADING_BOT_ROOT) not in sys.path:
    sys.path.insert(0, str(TRADING_BOT_ROOT))

from performance.signal_statistics import (
    pooled_block_adjusted_significance,
    stationary_block_bootstrap_ic_significance,
)


# ---------------------------------------------------------------------------
# pooled_block_adjusted_significance
# ---------------------------------------------------------------------------

def test_pooled_block_adjusted_significance_typical():
    result = pooled_block_adjusted_significance([0.15], 400, 24)
    assert result == {
        "pooled_ic": 0.15, "z_stat": 0.5408, "p_value": 0.5886,
        "n_eff": 16, "block_size": 24, "significant": False,
    }


def test_pooled_block_adjusted_significance_empty_ic_values():
    result = pooled_block_adjusted_significance([], 400, 24)
    assert result == {
        "pooled_ic": None, "z_stat": None, "p_value": 1.0,
        "n_eff": 16, "block_size": 24, "significant": False,
    }


def test_pooled_block_adjusted_significance_placeable_blocks():
    result = pooled_block_adjusted_significance(
        [0.05, None, -0.02], 500, 24, placeable_blocks=15)
    assert result == {
        "pooled_ic": 0.015, "z_stat": 0.052, "p_value": 0.9586,
        "n_eff": 15, "block_size": 24, "significant": False,
    }


def test_pooled_block_adjusted_significance_saturated_ic():
    result = pooled_block_adjusted_significance([1.0], 100, 24)
    assert result == {
        "pooled_ic": 1.0, "z_stat": None, "p_value": 0.0,
        "n_eff": 4, "block_size": 24, "significant": True,
    }


# ---------------------------------------------------------------------------
# stationary_block_bootstrap_ic_significance
# ---------------------------------------------------------------------------

def _bootstrap_fixture():
    n = 60
    return {
        "BTCUSDT": [
            {"forecast": ((-1) ** i) * (5 + i % 5), "next_return_bps": (i % 7) - 3}
            for i in range(n)
        ],
        "ETHUSDT": [
            {"forecast": ((-1) ** (i + 1)) * (3 + i % 4), "next_return_bps": (i % 5) - 2}
            for i in range(n)
        ],
    }


def test_stationary_block_bootstrap_default_args_structure():
    """seed=None by default -- p_value/n_bootstrap_valid are resample-dependent
    and not pinned exactly (see the seeded test below for an exact pin).
    pooled_ic is computed from the real, unresampled data so it IS
    deterministic regardless of seed -- pinned here."""
    records_by_symbol = _bootstrap_fixture()
    result = stationary_block_bootstrap_ic_significance(records_by_symbol)
    assert result["method"] == "block_bootstrap_all_bars_v1"
    assert result["block_size"] == 20
    assert result["n_resamples"] == 1000
    assert result["pooled_ic"] == -0.002096
    assert result["n_bootstrap_valid"] == 1000
    assert 0.0 <= result["p_value"] <= 1.0
    assert isinstance(result["significant"], bool)


def test_stationary_block_bootstrap_smaller_resamples_and_seed():
    records_by_symbol = _bootstrap_fixture()
    result = stationary_block_bootstrap_ic_significance(
        records_by_symbol, block_size=10, n_resamples=50, seed=42)
    assert result == {
        "method": "block_bootstrap_all_bars_v1", "block_size": 10,
        "n_resamples": 50, "pooled_ic": -0.002096, "p_value": 0.96,
        "significant": False, "n_bootstrap_valid": 50,
    }


def test_stationary_block_bootstrap_empty_input():
    result = stationary_block_bootstrap_ic_significance({})
    assert result == {
        "method": "block_bootstrap_all_bars_v1", "block_size": 20,
        "n_resamples": 1000, "pooled_ic": None, "p_value": 1.0,
        "significant": False, "n_bootstrap_valid": 0,
    }
