"""E-062 S2b-3a -- the pure partial-coverage normalisation helpers of
tools/variant_coin.py (DECISION_LOG D-047, implementing D-042;
engineering/roadmap/E-062/S2B3_FINDINGS.md Q3/Q4/Q6, G1/G2/G5/G7).

Nothing in the pipeline calls these yet (S2b-3b wires them). The table values
are the findings' own (Q3/Q4), recomputed here from the committed protocol
files -- protocol DEFINITIONS only, no market data, no run result.
"""
from __future__ import annotations

import copy
import math
import sys
from fractions import Fraction
from pathlib import Path

import pytest

SR_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SR_ROOT / "tools"))

import variant_coin as vc  # noqa: E402

PROTOCOLS = SR_ROOT / "protocols"


def _load(name: str) -> dict:
    return vc.load_protocol_file(PROTOCOLS / f"{name}.json")


def _last_k(source: dict, k: int) -> dict:
    """A late-listing asset variant: the last k windows, as 5a derives it."""
    labels = [w["label"] for w in source["windows"]][-k:]
    return vc.variant_protocol(source, symbol="XRPUSDT", windows_run=labels)


def _proto(*spans) -> dict:
    return {"symbols": ["BTCUSDT"], "timeframe": "1h",
            "windows": [{"label": f"w{i}", "test": {"start": s, "end": e}}
                        for i, (s, e) in enumerate(spans)]}


# --- the findings' table values (Q3 / Q4), from the committed protocols -------

@pytest.mark.parametrize("name, k, covered, full, f4, trades, dd", [
    ("run_053_generated", 58, 1767, 2922, 0.6047, 61, 15.55),
    ("run_053_generated", 68, 2071, 2922, 0.7088, 71, 16.84),
    ("run_053_generated", 77, 2345, 2922, 0.8025, 81, 17.92),
    ("h041c_v2_backext", 43, 1310, 2161, 0.6062, 61, 15.57),
    ("funding_mr_4h_retest_v1", 30, 915, 1493, 0.6129, 62, 15.66),
    ("ts_trend_daily_v1", 9, 1645, 2741, 0.6001, 61, 15.49),
    ("baseline_v1", 7, 215, 336, 0.6399, 64, 16.00),
])
def test_findings_table_values(name, k, covered, full, f4, trades, dd):
    src = _load(name)
    var = _last_k(src, k)
    assert vc.coverage_days(src, var) == (covered, full)
    f = vc.coverage_fraction(src, var)
    assert f == covered / full
    assert round(f, 4) == f4
    assert vc.normalised_trade_minimum(100, f, 60) == trades
    assert round(vc.scaled_drawdown_limit(20.0, f), 2) == dd


def test_run_053_58_of_96_exact():
    src = _load("run_053_generated")
    f = vc.coverage_fraction(src, _last_k(src, 58))
    assert f == pytest.approx(0.6047227926078029, abs=0, rel=1e-15)
    assert vc.normalised_trade_minimum(100, f, 60) == 61
    assert vc.scaled_drawdown_limit(20.0, f) == pytest.approx(20.0 * math.sqrt(1767 / 2922))
    # D-047 (2): the cost-ratio floor (100) uses the same function and floor.
    assert vc.normalised_trade_minimum(100, f, 60) == 61


# --- f ---------------------------------------------------------------------

@pytest.mark.parametrize("name", ["run_053_generated", "baseline_v1", "ts_trend_daily_v1",
                                  "h041c_v2_backext", "funding_mr_4h_retest_v1"])
def test_full_coverage_is_exactly_one(name):
    src = _load(name)
    var = vc.variant_protocol(src, symbol="XRPUSDT")
    f = vc.coverage_fraction(src, var)
    assert f == 1.0 and type(f) is float
    assert vc.coverage_fraction(src, copy.deepcopy(src)) == 1.0


def test_one_day_junction_counted_once():
    run = _proto(("2024-01-01", "2024-01-11"), ("2024-01-11", "2024-01-21"))
    # 11 + 11 day-inclusive spans sharing 2024-01-11: 21 days, not 22.
    assert vc.coverage_days(run, run) == (21, 21)
    first = vc.variant_protocol(run, symbol="X", windows_run=["w0"])
    assert vc.coverage_days(run, first) == (11, 21)
    assert vc.coverage_fraction(run, first) == 11 / 21


def test_non_contiguous_windows():
    run = _proto(("2024-01-01", "2024-01-10"), ("2024-02-01", "2024-02-10"),
                 ("2024-03-01", "2024-03-10"))
    assert vc.coverage_days(run, run) == (30, 30)
    gap_var = vc.variant_protocol(run, symbol="X", windows_run=["w0", "w2"])
    assert vc.coverage_days(run, gap_var) == (20, 30)
    assert vc.coverage_fraction(run, gap_var) == 20 / 30


def test_not_a_subsequence_raises():
    run = _proto(("2024-01-01", "2024-01-10"), ("2024-02-01", "2024-02-10"))
    foreign = _proto(("2023-01-01", "2023-01-10"))
    with pytest.raises(vc.VariantCoinError, match="not a subsequence"):
        vc.coverage_days(run, foreign)
    # same days, but a window dict the run protocol does not have
    relabelled = copy.deepcopy(run)
    relabelled["windows"][0]["label"] = "other"
    with pytest.raises(vc.VariantCoinError, match="not a subsequence"):
        vc.coverage_fraction(run, relabelled)
    # reordered: not the shape 5a writes
    reordered = copy.deepcopy(run)
    reordered["windows"].reverse()
    with pytest.raises(vc.VariantCoinError, match="not a subsequence"):
        vc.coverage_fraction(run, reordered)
    # a superset of the run protocol
    wider = _proto(("2024-01-01", "2024-01-10"), ("2024-02-01", "2024-02-10"),
                   ("2024-03-01", "2024-03-10"))
    with pytest.raises(vc.VariantCoinError, match="not a subsequence"):
        vc.coverage_fraction(run, wider)


@pytest.mark.parametrize("bad", [
    {"windows": []},
    {"symbols": ["X"]},
    _proto(("2024-01-10", "2024-01-01")),                  # end before start
    _proto(("2024-01-01T00:00:00", "2024-01-10")),         # not YYYY-MM-DD
    {"windows": [{"test": {"start": "2024-01-01", "end": "2024-01-02"}}]},  # no label
])
def test_malformed_variant_raises(bad):
    run = _proto(("2024-01-01", "2024-01-10"))
    with pytest.raises(vc.VariantCoinError):
        vc.coverage_fraction(run, bad)
    with pytest.raises(vc.VariantCoinError):
        vc.coverage_fraction(bad, run)


def test_non_mapping_protocol_raises():
    run = _proto(("2024-01-01", "2024-01-10"))
    with pytest.raises(vc.VariantCoinError):
        vc.coverage_fraction(run, None)
    with pytest.raises(vc.VariantCoinError):
        vc.coverage_fraction([run], run)


# --- trade minimum ------------------------------------------------------------

def test_trade_minimum_full_coverage_returns_base_exactly():
    assert vc.normalised_trade_minimum(100, 1.0, 60) == 100
    assert vc.normalised_trade_minimum(100, 1, 60) == 100
    assert vc.normalised_trade_minimum(100, Fraction(1), 60) == 100
    assert vc.normalised_trade_minimum(7, 1.0, 7) == 7


def test_trade_minimum_ceil_not_round():
    # 100 * 0.6047 = 60.47 -> 61 (round would give 60)
    assert vc.normalised_trade_minimum(100, 1767 / 2922, 1) == 61
    # 100 * 0.701 = 70.1 -> 71
    assert vc.normalised_trade_minimum(100, 0.701, 1) == 71
    # just above an integer still ceils up
    assert vc.normalised_trade_minimum(100, Fraction(7001, 10000), 1) == 71


def test_trade_minimum_exact_integer_not_bumped_by_float_noise():
    # 100 * 0.07 == 7.000000000000001 in floats; the requirement is 7, not 8.
    assert 100 * 0.07 > 7
    assert vc.normalised_trade_minimum(100, 0.07, 1) == 7
    # a day ratio whose pro-rata share is an integer: 600 * 5/6 == 500
    assert vc.normalised_trade_minimum(600, 5 / 6, 1) == 500
    assert vc.normalised_trade_minimum(100, 0.7, 1) == 70


def test_trade_minimum_floor_binds():
    assert vc.normalised_trade_minimum(100, 0.5, 60) == 60      # 50 < 60
    assert vc.normalised_trade_minimum(100, 0.59, 60) == 60     # 59 < 60
    assert vc.normalised_trade_minimum(100, 0.6, 60) == 60      # 60 == 60
    assert vc.normalised_trade_minimum(100, 0.601, 60) == 61    # 60.1 -> 61 > 60


@pytest.mark.parametrize("f", [0, 0.0, -0.1, 1.0000001, 1.5, 2, float("nan"), float("inf"),
                               float("-inf"), True, False, None, "0.6", 1e-13])
def test_trade_minimum_f_out_of_bounds_raises(f):
    with pytest.raises(vc.VariantCoinError):
        vc.normalised_trade_minimum(100, f, 60)


@pytest.mark.parametrize("base, floor", [(0, 1), (100, 0), (100.0, 60), (100, 60.0),
                                         (True, 1), (100, 101), (-5, 1)])
def test_trade_minimum_bad_base_or_floor_raises(base, floor):
    with pytest.raises(vc.VariantCoinError):
        vc.normalised_trade_minimum(base, 0.8, floor)


# --- drawdown limit -----------------------------------------------------------

def test_drawdown_full_coverage_returns_limit_exactly():
    assert vc.scaled_drawdown_limit(20.0, 1.0) == 20.0
    assert vc.scaled_drawdown_limit(20, 1) == 20
    assert vc.scaled_drawdown_limit(17.3, Fraction(1)) == 17.3


def test_drawdown_scales_by_sqrt_f():
    assert vc.scaled_drawdown_limit(20.0, 0.25) == 10.0
    assert vc.scaled_drawdown_limit(20.0, 0.6) == pytest.approx(15.491933384829668)
    assert vc.scaled_drawdown_limit(20.0, 0.8) == pytest.approx(17.88854381999832)
    # tighter than the full-period limit, looser than linear (Q4)
    f = 0.6047
    assert 20.0 * f < vc.scaled_drawdown_limit(20.0, f) < 20.0


@pytest.mark.parametrize("f", [0, -1, 1.01, float("nan"), float("inf"), True, None])
def test_drawdown_f_out_of_bounds_raises(f):
    with pytest.raises(vc.VariantCoinError):
        vc.scaled_drawdown_limit(20.0, f)


@pytest.mark.parametrize("limit", [0, -20.0, float("nan"), float("inf"), True, None, "20"])
def test_drawdown_bad_limit_raises(limit):
    with pytest.raises(vc.VariantCoinError):
        vc.scaled_drawdown_limit(limit, 0.8)


# --- represented-era count (D-047 (4)) -----------------------------------------

def test_era_count_zero_eras():
    assert vc.era_count_shortfall([]) == "single_era: none"
    assert vc.era_count_shortfall(["era_unmapped"]) == "single_era: none"


def test_era_count_one_era():
    reason = vc.era_count_shortfall(["era_2019_2023_full_feed"] * 5)
    assert reason == "single_era: era_2019_2023_full_feed"
    assert reason.startswith(vc.SINGLE_ERA_REASON_PREFIX)
    # era_unmapped is never a second era
    assert vc.era_count_shortfall(["era_2024_burned", "era_unmapped"]) == \
        "single_era: era_2024_burned"


def test_era_count_two_eras():
    assert vc.D047_MIN_REPRESENTED_ERAS == 2
    assert vc.era_count_shortfall(["era_2024_burned",
                                   "era_2024_2025_walk_forward_extension"]) is None
    assert vc.era_count_shortfall({"a": 1, "b": 2}.keys()) is None  # a reducer's by_era keys


@pytest.mark.parametrize("bad", ["era_2024_burned", [None], [""], [3]])
def test_era_count_malformed_raises(bad):
    with pytest.raises(vc.VariantCoinError):
        vc.era_count_shortfall(bad)
