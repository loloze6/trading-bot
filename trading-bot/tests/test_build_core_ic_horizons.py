"""
D-186 (direction 2026-10-24, PR-4): build_core writes the all-bars forecast / forward-return
Pearson correlation at horizons 1, 6, 24, 72, 168 beside the one-bar field
forecast_return_corr_all_bars, only when asked (keyword `forecast_ic_horizons` or the
process-wide set_forecast_ic_horizons()); default off writes no new key at all.

Forward return at horizon h = close[t+h] / close[t] - 1. Bars whose t+h lies past the last
row are dropped (never padded); a pair whose span holds a timestamp hole is dropped (the same
successor rule the one-bar field has). Below 5 pairs the field is None, never 0.0.
"""
import json
import sys
from pathlib import Path

import pandas as pd
import pytest

TRADING_BOT_ROOT = Path(__file__).parent.parent
if str(TRADING_BOT_ROOT) not in sys.path:
    sys.path.insert(0, str(TRADING_BOT_ROOT))

from reporting import run_artifact
from reporting.run_artifact import (
    FORECAST_IC_HORIZONS, build_core, forecast_ic_horizon_field, set_forecast_ic_horizons,
)
from performance.signal_statistics import pearson_correlation

STEP = 3600


@pytest.fixture(autouse=True)
def _reset_process_default():
    set_forecast_ic_horizons(None)
    yield
    set_forecast_ic_horizons(None)


def _series(n=400):
    # deterministic, non-degenerate forecast and a price path that is not a pure function of it
    forecasts = [((i * 7) % 11) - 5 + 0.25 * ((i * 3) % 5) for i in range(n)]
    closes = [100.0]
    for i in range(1, n):
        closes.append(closes[-1] * (1 + 0.002 * (((i * 13) % 17) - 8) / 8.0))
    return forecasts, closes


def _bars(forecasts, closes, drop=()):
    df = pd.DataFrame({
        "timestamp": pd.date_range("2020-01-01", periods=len(forecasts), freq="h"),
        "forecast": forecasts,
        "close": closes,
    })
    return df.drop(index=list(drop)).reset_index(drop=True) if drop else df


def _hand(forecasts, closes, h, keep=None):
    """The reference: loop over the bars that have a close h bars later."""
    xs, ys = [], []
    for t in range(len(closes) - h):
        if keep is not None and not keep(t):
            continue
        xs.append(float(forecasts[t]))
        ys.append(closes[t + h] / closes[t] - 1)
    if len(xs) < 5:
        return None
    c = pearson_correlation(xs, ys)
    return round(c, 6) if c is not None else None


def _core(bars, **kw):
    return build_core({}, [], bars, candle_interval_seconds=STEP, **kw)


# -- values ---------------------------------------------------------------------------------

@pytest.mark.parametrize("h", FORECAST_IC_HORIZONS)
def test_each_horizon_equals_the_hand_computed_correlation(h):
    f, c = _series()
    core = _core(_bars(f, c), forecast_ic_horizons=FORECAST_IC_HORIZONS)
    expected = _hand(f, c, h)
    assert expected is not None
    assert core[forecast_ic_horizon_field(h)] == expected


def test_horizon_one_equals_the_existing_one_bar_field_exactly():
    f, c = _series()
    core = _core(_bars(f, c), forecast_ic_horizons=FORECAST_IC_HORIZONS)
    assert core["forecast_return_corr_all_bars_h1"] == core["forecast_return_corr_all_bars"]
    assert core["forecast_return_corr_all_bars"] is not None


def test_horizon_one_equals_the_existing_field_with_a_gap_and_a_zero_forecast_gate():
    f, c = _series(120)
    f = [0.0 if i % 3 == 0 else v for i, v in enumerate(f)]   # a gated strategy
    core = _core(_bars(f, c, drop=[50]), forecast_ic_horizons=(1,))
    assert core["forecast_return_corr_all_bars_h1"] == core["forecast_return_corr_all_bars"]


def test_tail_bars_without_a_forward_return_are_dropped_never_padded():
    f, c = _series(60)
    h = 6
    # The last h bars' forecasts are poisoned: if they were used (padded with anything) the
    # correlation would move; with them dropped it equals the correlation over bars 0..n-h-1.
    f_poison = f[:-h] + [1e6] * h
    core = _core(_bars(f_poison, c), forecast_ic_horizons=(h,))
    assert core[forecast_ic_horizon_field(h)] == _hand(f_poison, c, h)
    assert core[forecast_ic_horizon_field(h)] == _hand(f, c, h)   # poison made no difference


def test_a_window_shorter_than_the_horizon_gives_none_not_zero():
    f, c = _series(60)
    core = _core(_bars(f, c), forecast_ic_horizons=FORECAST_IC_HORIZONS)
    assert core["forecast_return_corr_all_bars_h72"] is None     # 60 bars, 72 ahead: no pair
    assert core["forecast_return_corr_all_bars_h168"] is None
    assert core["forecast_return_corr_all_bars_h24"] is not None


def test_fewer_than_five_pairs_is_none_and_exactly_five_is_a_number():
    f, c = _series(77)                                           # 77 - 72 = 5 pairs
    assert _core(_bars(f, c), forecast_ic_horizons=(72,))["forecast_return_corr_all_bars_h72"] \
        == _hand(f, c, 72)
    assert _hand(f, c, 72) is not None
    f4, c4 = _series(76)                                         # 4 pairs
    assert _core(_bars(f4, c4), forecast_ic_horizons=(72,))["forecast_return_corr_all_bars_h72"] is None


def test_a_hole_inside_the_span_drops_the_pair():
    f, c = _series(200)
    hole = 100                                                   # row 100 missing: timestamps jump
    bars = _bars(f, c, drop=[hole])
    f2 = [v for i, v in enumerate(f) if i != hole]
    c2 = [v for i, v in enumerate(c) if i != hole]
    h = 24
    # row r of the thinned frame is original bar r (r < hole) or r+1 (r >= hole); the span of
    # row r to row r+h is contiguous only if it does not straddle the hole
    keep = lambda r: not (r < hole <= r + h)
    expected = _hand(f2, c2, h, keep=keep)
    assert expected is not None
    assert _core(bars, forecast_ic_horizons=(h,))[forecast_ic_horizon_field(h)] == expected


def test_undefined_correlation_is_none():
    f = [3.0] * 50                                               # constant forecast
    _, c = _series(50)
    core = _core(_bars(f, c), forecast_ic_horizons=(6,))
    assert core["forecast_return_corr_all_bars_h6"] is None


# -- off: byte-identical --------------------------------------------------------------------

def test_default_off_adds_no_key_and_equals_the_flag_on_output_minus_the_new_keys():
    f, c = _series()
    bars = _bars(f, c)
    off = _core(bars)
    on = _core(bars, forecast_ic_horizons=FORECAST_IC_HORIZONS)
    new_keys = {forecast_ic_horizon_field(h) for h in FORECAST_IC_HORIZONS}
    assert not new_keys & set(off)
    assert set(on) - set(off) == new_keys
    assert {k: v for k, v in on.items() if k not in new_keys} == off
    # key ORDER and serialisation are untouched too
    assert list(off) == [k for k in on if k not in new_keys]
    assert json.dumps(off, default=str) == json.dumps(
        {k: v for k, v in on.items() if k not in new_keys}, default=str)


def test_process_wide_setting_is_the_default_and_none_turns_it_off():
    f, c = _series()
    bars = _bars(f, c)
    set_forecast_ic_horizons(FORECAST_IC_HORIZONS)
    assert forecast_ic_horizon_field(6) in _core(bars)
    set_forecast_ic_horizons(None)
    assert forecast_ic_horizon_field(6) not in _core(bars)


def test_the_keyword_wins_over_the_process_setting():
    f, c = _series()
    set_forecast_ic_horizons(FORECAST_IC_HORIZONS)
    core = _core(_bars(f, c), forecast_ic_horizons=(6,))
    assert forecast_ic_horizon_field(6) in core and forecast_ic_horizon_field(24) not in core



# -- bad horizons ---------------------------------------------------------------------------

@pytest.mark.parametrize("bad", [("6",), (6.0,), (True,), (0,), (-1,), "6", 6])
def test_a_horizon_that_is_not_a_positive_int_raises(bad):
    f, c = _series(40)
    with pytest.raises(ValueError):
        _core(_bars(f, c), forecast_ic_horizons=bad)
    with pytest.raises(ValueError):
        set_forecast_ic_horizons(bad)


def test_no_name_collision_the_new_fields_are_only_defined_here():
    names = {forecast_ic_horizon_field(h) for h in FORECAST_IC_HORIZONS}
    src = Path(run_artifact.__file__).read_text(encoding="utf-8")
    # the existing field names never end in _h<digits>
    for old in ("forecast_return_corr", "forecast_return_corr_all_bars", "forecast_return_corr_n_eff"):
        assert old not in names
    assert src.count("def forecast_ic_horizon_field") == 1
