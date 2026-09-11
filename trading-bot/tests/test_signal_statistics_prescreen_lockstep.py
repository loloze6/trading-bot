"""
E-039 step 5 (2026-09-12): performance.signal_statistics's newly-ported
contiguous_segments/pooled_block_adjusted_significance/
stationary_block_bootstrap_ic_significance must agree EXACTLY with
prescreen_signal.py's originals on identical input -- proving the port is
algorithmically faithful before prescreen_signal.py is removed and its
dependents (episode_significance.py, run_protocol.py,
whale_footprint_evaluation.py) are repointed here. Same lockstep-test
discipline CUL-262/264 already established for block_adjusted_pvalue/
cost_check/determine_route.
"""
import sys
from pathlib import Path

TRADING_BOT_ROOT = Path(__file__).parent.parent
if str(TRADING_BOT_ROOT) not in sys.path:
    sys.path.insert(0, str(TRADING_BOT_ROOT))

TOOLS_PATH = TRADING_BOT_ROOT.parent / "strategy-research" / "tools"
if str(TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(TOOLS_PATH))

from performance.signal_statistics import (
    contiguous_segments,
    pooled_block_adjusted_significance,
    stationary_block_bootstrap_ic_significance,
)
import prescreen_signal as ps


# ---------------------------------------------------------------------------
# contiguous_segments vs prescreen_signal.py::_contiguous_segments
# ---------------------------------------------------------------------------

def _recs_with_gap():
    """5 bars, hourly step, with a 3-hour hole between index 2 and 3."""
    import pandas as pd
    ts = [pd.Timestamp("2024-01-01 00:00"), pd.Timestamp("2024-01-01 01:00"),
          pd.Timestamp("2024-01-01 02:00"), pd.Timestamp("2024-01-01 05:00"),
          pd.Timestamp("2024-01-01 06:00")]
    return [{"timestamp": t} for t in ts], pd.Timedelta(hours=1)


def test_contiguous_segments_matches_prescreen_with_gap():
    recs, step = _recs_with_gap()
    assert contiguous_segments(recs, step) == ps._contiguous_segments(recs, step)
    assert contiguous_segments(recs, step) == [(0, 3), (3, 5)]


def test_contiguous_segments_matches_prescreen_no_expected_step():
    recs, _ = _recs_with_gap()
    assert contiguous_segments(recs, None) == ps._contiguous_segments(recs, None)
    assert contiguous_segments(recs, None) == [(0, 5)]


def test_contiguous_segments_matches_prescreen_empty():
    assert contiguous_segments([], None) == ps._contiguous_segments([], None)


def test_contiguous_segments_missing_timestamp_raises_same_as_prescreen():
    recs = [{"no_timestamp": True}]
    import pandas as pd
    step = pd.Timedelta(hours=1)
    raised_new = raised_old = False
    try:
        contiguous_segments(recs, step)
    except KeyError:
        raised_new = True
    try:
        ps._contiguous_segments(recs, step)
    except KeyError:
        raised_old = True
    assert raised_new and raised_old


# ---------------------------------------------------------------------------
# pooled_block_adjusted_significance vs prescreen_signal.py::_block_adjusted_significance
# ---------------------------------------------------------------------------

def test_pooled_block_adjusted_significance_matches_prescreen_typical():
    ic_values = [0.15]
    n_active = 400
    block_size = 24
    new = pooled_block_adjusted_significance(ic_values, n_active, block_size)
    old = ps._block_adjusted_significance(ic_values, n_active, block_size)
    assert new == old


def test_pooled_block_adjusted_significance_matches_prescreen_empty_ic_values():
    new = pooled_block_adjusted_significance([], 400, 24)
    old = ps._block_adjusted_significance([], 400, 24)
    assert new == old


def test_pooled_block_adjusted_significance_matches_prescreen_placeable_blocks():
    ic_values = [0.05, None, -0.02]
    new = pooled_block_adjusted_significance(ic_values, 500, 24, placeable_blocks=15)
    old = ps._block_adjusted_significance(ic_values, 500, 24, placeable_blocks=15)
    assert new == old


def test_pooled_block_adjusted_significance_matches_prescreen_saturated_ic():
    new = pooled_block_adjusted_significance([1.0], 100, 24)
    old = ps._block_adjusted_significance([1.0], 100, 24)
    assert new == old


# ---------------------------------------------------------------------------
# stationary_block_bootstrap_ic_significance vs prescreen_signal.py's original
# ---------------------------------------------------------------------------

def _bootstrap_fixture():
    n = 60
    records_by_symbol = {
        "BTCUSDT": [
            {"forecast": ((-1) ** i) * (5 + i % 5), "next_return_bps": (i % 7) - 3}
            for i in range(n)
        ],
        "ETHUSDT": [
            {"forecast": ((-1) ** (i + 1)) * (3 + i % 4), "next_return_bps": (i % 5) - 2}
            for i in range(n)
        ],
    }
    return records_by_symbol


def test_stationary_block_bootstrap_matches_prescreen_default_args():
    records_by_symbol = _bootstrap_fixture()
    new = stationary_block_bootstrap_ic_significance(records_by_symbol)
    old = ps._stationary_block_bootstrap_ic_significance(records_by_symbol)
    assert new == old


def test_stationary_block_bootstrap_matches_prescreen_smaller_resamples_and_seed():
    records_by_symbol = _bootstrap_fixture()
    new = stationary_block_bootstrap_ic_significance(
        records_by_symbol, block_size=10, n_resamples=50, seed=42)
    old = ps._stationary_block_bootstrap_ic_significance(
        records_by_symbol, block_size=10, n_resamples=50, seed=42)
    assert new == old


def test_stationary_block_bootstrap_matches_prescreen_empty_input():
    new = stationary_block_bootstrap_ic_significance({})
    old = ps._stationary_block_bootstrap_ic_significance({})
    assert new == old
