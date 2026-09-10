"""
E-016 (fee-reduction autopsy field) regression tests.

Covers:
  1. The 8 diagnostic metric formulas (2 per lever x 4 levers), each on small,
     hand-computable synthetic trade/bar data -- expected values are derived
     by hand in the test itself (in comments), not snapshotted from a run.
  2. The verdict_interpretation.schema.json candidate_system enum: the new
     4-value set validates, the deleted 5-value set is rejected.

No network, no engine, no live caches -- pure in-memory fixtures and a
hand-written bars.csv/trades.json pair (same fixture style as
test_run_protocol_exit_reason.py).
"""
import csv
import json
import math
import sys
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).parent.parent
TOOLS_PATH = ROOT / "tools"
if str(TOOLS_PATH) not in sys.path:
    sys.path.insert(0, str(TOOLS_PATH))

import run_protocol as rp  # noqa: E402 -- also puts trading-bot/ on sys.path

SCHEMAS_DIR = ROOT / "workflow_artifacts" / "schemas"


# ---------------------------------------------------------------------------
# 1a/1b -- combine_nearby_trades (tested via _compute_window_fee_reduction_diagnostics,
# since the re-entry pairing is inherently a multi-trade, window-scoped computation)
# ---------------------------------------------------------------------------

_BAR_FIELDS = ["timestamp", "open", "high", "low", "close", "forecast"]


def _write_bars(tmp_path, timestamps, closes, forecasts):
    run_dir = tmp_path / "run"
    run_dir.mkdir(exist_ok=True)
    rows = [
        {"timestamp": ts, "open": c, "high": c, "low": c, "close": c, "forecast": f}
        for ts, c, f in zip(timestamps, closes, forecasts)
    ]
    with open(run_dir / "bars.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=_BAR_FIELDS)
        w.writeheader()
        w.writerows(rows)
    return run_dir


def test_combine_nearby_trades_reentry_rate_and_gap(tmp_path):
    """
    5 daily bars, 2 trades sharing the window:
      trade1: direction=long, entry_idx=0, exit_idx=1
      trade2: direction=long, entry_idx=2, exit_idx=3
    Only ONE adjacent trade pair exists (trade1 -> trade2). It is same
    direction and its gap = entry_idx(2) - exit_idx(1) = 1 bar, which is
    <= _FEE_REDUCTION_LOOKAHEAD_BARS (6) -- so it counts as a re-entry.
      same_direction_reentry_rate (this window) = 1/1 = 1.0
      avg_reentry_gap_bars (this window)        = 1
    """
    timestamps = [f"2024-01-0{d} 00:00:00" for d in range(1, 6)]
    closes     = [100, 110, 99, 108.9, 98.01]  # unused for this assertion, kept realistic
    forecasts  = [5, 5, 5, 5, 5]                # no crossings -- isolates this metric
    run_dir = _write_bars(tmp_path, timestamps, closes, forecasts)

    trade_records = [
        {"direction": "long", "entry_idx": 0, "exit_idx": 1},
        {"direction": "long", "entry_idx": 2, "exit_idx": 3},
    ]
    diag = rp._compute_window_fee_reduction_diagnostics(
        run_dir, "BTCUSDT", "2024-01", trade_records, boundary_level=0.0,
    )
    assert diag["total_pair_count"] == 1
    assert diag["reentry_pair_count"] == 1
    assert diag["reentry_gaps"] == [1]


def test_combine_nearby_trades_different_direction_not_counted(tmp_path):
    """Same setup, but trade2 flips direction -- the pair must NOT count as a
    re-entry (it still counts toward total_pair_count)."""
    timestamps = [f"2024-01-0{d} 00:00:00" for d in range(1, 6)]
    closes     = [100, 110, 99, 108.9, 98.01]
    forecasts  = [5, 5, 5, 5, 5]
    run_dir = _write_bars(tmp_path, timestamps, closes, forecasts)

    trade_records = [
        {"direction": "long",  "entry_idx": 0, "exit_idx": 1},
        {"direction": "short", "entry_idx": 2, "exit_idx": 3},
    ]
    diag = rp._compute_window_fee_reduction_diagnostics(
        run_dir, "BTCUSDT", "2024-01", trade_records, boundary_level=0.0,
    )
    assert diag["total_pair_count"] == 1
    assert diag["reentry_pair_count"] == 0
    assert diag["reentry_gaps"] == []


def test_combine_nearby_trades_gap_beyond_lookahead_not_counted(tmp_path):
    """A same-direction pair whose gap exceeds the lookback window must not count."""
    timestamps = [f"2024-01-{d:02d} 00:00:00" for d in range(1, 11)]
    closes     = [100] * 10
    forecasts  = [5] * 10
    run_dir = _write_bars(tmp_path, timestamps, closes, forecasts)

    gap = rp._FEE_REDUCTION_LOOKAHEAD_BARS + 1
    trade_records = [
        {"direction": "long", "entry_idx": 0, "exit_idx": 1},
        {"direction": "long", "entry_idx": 1 + gap, "exit_idx": 2 + gap},
    ]
    diag = rp._compute_window_fee_reduction_diagnostics(
        run_dir, "BTCUSDT", "2024-01", trade_records, boundary_level=0.0,
    )
    assert diag["total_pair_count"] == 1
    assert diag["reentry_pair_count"] == 0


# ---------------------------------------------------------------------------
# 2a/2b -- exit_later: _compute_post_exit_drift / _compute_held_longer_better
# ---------------------------------------------------------------------------

def test_post_exit_drift_long_favorable():
    """
    LONG, exit_idx=3, exit_price=100, n=2 -> target bar is idx 5, close=108.
    raw = (108 - 100) / 100 * 100 = 8.0 (no sign flip for LONG).
    """
    bars = [{"close": None}] * 4 + [{"close": 999}, {"close": 108}]
    assert rp._compute_post_exit_drift("LONG", 100.0, bars, exit_idx=3, n=2) == 8.0


def test_post_exit_drift_short_sign_flipped():
    """
    SHORT, exit_idx=3, exit_price=100, n=2 -> target bar idx 5, close=92.
    raw = (92 - 100) / 100 * 100 = -8.0; SHORT flips sign -> +8.0 (favorable:
    price kept falling after covering the short).
    """
    bars = [{"close": None}] * 4 + [{"close": 999}, {"close": 92}]
    assert rp._compute_post_exit_drift("SHORT", 100.0, bars, exit_idx=3, n=2) == 8.0


def test_post_exit_drift_out_of_range_is_none():
    bars = [{"close": 100}, {"close": 101}]
    assert rp._compute_post_exit_drift("LONG", 100.0, bars, exit_idx=1, n=2) is None


def test_held_longer_better_long_true_and_false():
    bars_better = [{"close": 100}, {"close": 105}]  # next bar close 105 > exit_price 100
    assert rp._compute_held_longer_better("LONG", 100.0, bars_better, exit_idx=0) is True
    bars_worse = [{"close": 100}, {"close": 95}]
    assert rp._compute_held_longer_better("LONG", 100.0, bars_worse, exit_idx=0) is False


def test_held_longer_better_short_true_and_false():
    bars_better = [{"close": 100}, {"close": 95}]  # next bar close 95 < exit_price 100
    assert rp._compute_held_longer_better("SHORT", 100.0, bars_better, exit_idx=0) is True
    bars_worse = [{"close": 100}, {"close": 105}]
    assert rp._compute_held_longer_better("SHORT", 100.0, bars_worse, exit_idx=0) is False


def test_held_longer_better_no_next_bar_is_none():
    bars = [{"close": 100}]
    assert rp._compute_held_longer_better("LONG", 100.0, bars, exit_idx=0) is None


# ---------------------------------------------------------------------------
# 3a/3b -- enter_earlier: _compute_pre_entry_drift / _compute_entered_earlier_better
# ---------------------------------------------------------------------------

def test_pre_entry_drift_long_favorable():
    """
    LONG, entry_idx=5, entry_price=110, n=2 -> price 2 bars before entry is
    bars[3].close=100. raw = (110-100)/100*100 = 10.0 (no flip for LONG:
    price was already rising into the entry, the direction the trade profits from).
    """
    bars = [{"close": None}] * 3 + [{"close": 100}, {"close": None}, {"close": None}]
    assert rp._compute_pre_entry_drift("LONG", 110.0, bars, entry_idx=5, n=2) == 10.0


def test_pre_entry_drift_short_sign_flipped():
    """
    SHORT, entry_idx=5, entry_price=90, n=2 -> price 2 bars before = 100.
    raw = (90-100)/100*100 = -10.0; SHORT flips sign -> +10.0 (favorable:
    price was already falling into the short entry).
    """
    bars = [{"close": None}] * 3 + [{"close": 100}, {"close": None}, {"close": None}]
    assert rp._compute_pre_entry_drift("SHORT", 90.0, bars, entry_idx=5, n=2) == 10.0


def test_pre_entry_drift_before_start_is_none():
    bars = [{"close": 100}, {"close": 101}]
    assert rp._compute_pre_entry_drift("LONG", 110.0, bars, entry_idx=1, n=2) is None


def test_entered_earlier_better_long_true_and_false():
    bars_better = [{"close": 105}, {"close": 110}]  # prior bar 105 < entry_price 110
    assert rp._compute_entered_earlier_better("LONG", 110.0, bars_better, entry_idx=1) is True
    bars_worse = [{"close": 115}, {"close": 110}]
    assert rp._compute_entered_earlier_better("LONG", 110.0, bars_worse, entry_idx=1) is False


def test_entered_earlier_better_short_true_and_false():
    bars_better = [{"close": 95}, {"close": 90}]  # prior bar 95 > entry_price 90
    assert rp._compute_entered_earlier_better("SHORT", 90.0, bars_better, entry_idx=1) is True
    bars_worse = [{"close": 85}, {"close": 90}]
    assert rp._compute_entered_earlier_better("SHORT", 90.0, bars_worse, entry_idx=1) is False


def test_entered_earlier_better_no_prior_bar_is_none():
    bars = [{"close": 100}]
    assert rp._compute_entered_earlier_better("LONG", 100.0, bars, entry_idx=0) is None


# ---------------------------------------------------------------------------
# 4a/4b -- trade_less_often: boundary re-cross rate + frequency-vs-volatility
# ---------------------------------------------------------------------------

def test_boundary_recross_rate_and_gap(tmp_path):
    """
    5 bars, forecast = [5, -3, 4, -2, 6], boundary_level = 0.0.
    Signs relative to level (>=0 -> +1, else -1): [+1, -1, +1, -1, +1].
    Crossings (sign differs from previous bar's sign) at idx 1, 2, 3, 4.
    Gaps between consecutive crossings: 2-1=1, 3-2=1, 4-3=1 -> all <= lookback.
    boundary_recross_rate = 3/3 = 1.0; avg_boundary_recross_gap_bars = 1.0.
    """
    timestamps = [f"2024-01-0{d} 00:00:00" for d in range(1, 6)]
    closes     = [100, 110, 99, 108.9, 98.01]
    forecasts  = [5, -3, 4, -2, 6]
    run_dir = _write_bars(tmp_path, timestamps, closes, forecasts)

    diag = rp._compute_window_fee_reduction_diagnostics(
        run_dir, "BTCUSDT", "2024-01", trade_records=[], boundary_level=0.0,
    )
    assert diag["n_crossings"] == 4
    assert diag["boundary_recross_rate"] == 1.0
    assert diag["avg_boundary_recross_gap_bars"] == 1.0


def test_frequency_vs_volatility_ratio(tmp_path):
    """
    5 daily bars, closes = [100, 110, 99, 108.9, 98.01] -> bar-to-bar pct
    returns = [+0.1, -0.1, +0.1, -0.1] EXACTLY (each close is the prior
    times 1.1 or 0.9). Sample stdev of [0.1,-0.1,0.1,-0.1]:
      mean = 0; sum((x-mean)^2) = 4 * 0.01 = 0.04; /(n-1=3) = 0.013333...
      stdev = sqrt(0.013333...) = 0.11547005383792515
    Window span: 2024-01-01 00:00 -> 2024-01-05 00:00 = 4 days.
    2 trades in this window -> trades_per_day = 2/4 = 0.5.
    frequency_vs_volatility_ratio = 0.5 / 0.11547005383792515 = 4.330127018922194
    """
    timestamps = [f"2024-01-0{d} 00:00:00" for d in range(1, 6)]
    closes     = [100, 110, 99, 108.9, 98.01]
    forecasts  = [5, 5, 5, 5, 5]  # no crossings -- isolates this metric
    run_dir = _write_bars(tmp_path, timestamps, closes, forecasts)

    trade_records = [
        {"direction": "long", "entry_idx": 0, "exit_idx": 1},
        {"direction": "long", "entry_idx": 2, "exit_idx": 3},
    ]
    diag = rp._compute_window_fee_reduction_diagnostics(
        run_dir, "BTCUSDT", "2024-01", trade_records, boundary_level=0.0,
    )
    # realized_volatility/frequency_vs_volatility_ratio are rounded to 6dp by
    # the function under test, so compare at 6dp precision, not full float precision.
    expected_vol = math.sqrt(0.04 / 3)
    assert diag["realized_volatility"] == pytest.approx(expected_vol, abs=1e-6)
    assert diag["trades_per_day"] == pytest.approx(0.5, abs=1e-9)
    assert diag["frequency_vs_volatility_ratio"] == pytest.approx(0.5 / expected_vol, abs=1e-5)


# ---------------------------------------------------------------------------
# _resolve_boundary_level
# ---------------------------------------------------------------------------

def test_resolve_boundary_level_finds_nested_threshold_filter():
    config = {
        "strategies": [
            {"name": "rsi", "transforms": [
                {"op": "clip", "params": {"lo": -1, "hi": 1}},
                {"op": "threshold_filter", "params": {"min_abs": 15.0}},
            ]},
        ]
    }
    assert rp._resolve_boundary_level(config) == 15.0


def test_resolve_boundary_level_defaults_to_zero_when_absent():
    config = {"strategies": [{"name": "rsi", "transforms": [{"op": "clip"}]}]}
    assert rp._resolve_boundary_level(config) == 0.0


def test_resolve_boundary_level_handles_none_config():
    assert rp._resolve_boundary_level(None) == 0.0


# ---------------------------------------------------------------------------
# _aggregate_fee_reduction_diagnostics
# ---------------------------------------------------------------------------

def test_aggregate_fee_reduction_diagnostics_hand_computed():
    """
    2 trade records:
      post_exit_drift_pct: [8.0, -2.0]  -> mean = 3.0
      held_longer_better:  [True, False] -> 1/2 = 50.0%
      pre_entry_drift_pct: [10.0, -4.0] -> mean = 3.0
      entered_earlier_better: [False, True] -> 1/2 = 50.0%

    2 window diagnostics:
      total_pair_count: [2, 3] -> sum 5
      reentry_pair_count: [1, 2] -> sum 3 -> rate = 3/5 = 0.6
      reentry_gaps: [1] + [2, 3] -> mean([1,2,3]) = 2.0
      boundary_recross_rate: [1.0, 0.5] -> mean = 0.75
      frequency_vs_volatility_ratio: [4.0, 2.0] -> mean = 3.0
    """
    all_records = [
        {"post_exit_drift_pct": 8.0, "held_longer_better": True,
         "pre_entry_drift_pct": 10.0, "entered_earlier_better": False},
        {"post_exit_drift_pct": -2.0, "held_longer_better": False,
         "pre_entry_drift_pct": -4.0, "entered_earlier_better": True},
    ]
    all_window_diagnostics = [
        {"total_pair_count": 2, "reentry_pair_count": 1, "reentry_gaps": [1],
         "boundary_recross_rate": 1.0, "frequency_vs_volatility_ratio": 4.0},
        {"total_pair_count": 3, "reentry_pair_count": 2, "reentry_gaps": [2, 3],
         "boundary_recross_rate": 0.5, "frequency_vs_volatility_ratio": 2.0},
    ]

    out = rp._aggregate_fee_reduction_diagnostics(all_records, all_window_diagnostics)

    assert out["lookback_bars"] == rp._FEE_REDUCTION_LOOKAHEAD_BARS
    assert out["combine_nearby_trades"]["same_direction_reentry_rate"] == 0.6
    assert out["combine_nearby_trades"]["avg_reentry_gap_bars"] == 2.0
    assert out["exit_later"]["avg_post_exit_drift_pct"] == 3.0
    assert out["exit_later"]["pct_better_exit_1bar_later"] == 50.0
    assert out["enter_earlier"]["avg_pre_entry_drift_pct"] == 3.0
    assert out["enter_earlier"]["pct_better_entry_1bar_earlier"] == 50.0
    assert out["trade_less_often"]["boundary_recross_rate"] == 0.75
    assert out["trade_less_often"]["frequency_vs_volatility_ratio"] == 3.0


def test_aggregate_fee_reduction_diagnostics_empty_input():
    assert rp._aggregate_fee_reduction_diagnostics([], []) == {}


# ---------------------------------------------------------------------------
# verdict_interpretation.schema.json candidate_system enum
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def candidate_system_subschema():
    schema = json.loads(
        (SCHEMAS_DIR / "verdict_interpretation.schema.json").read_text(encoding="utf-8")
    )
    return (
        schema["properties"]["root_cause"]["properties"]
        ["fee_reduction_assessment"]["properties"]["candidate_system"]
    )


@pytest.mark.parametrize("value", [
    "trade_less_often", "combine_nearby_trades", "exit_later", "enter_earlier",
])
def test_candidate_system_new_enum_values_valid(candidate_system_subschema, value):
    jsonschema.validate(value, candidate_system_subschema)


@pytest.mark.parametrize("value", [
    "maker_only_execution", "lower_frequency_variant", "different_product",
    "venue_tier", "batching",
])
def test_candidate_system_old_enum_values_rejected(candidate_system_subschema, value):
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(value, candidate_system_subschema)
