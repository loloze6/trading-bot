"""E12 (2026-11-27): the degenerate-signal fallback of the wrapper's per-symbol summary on gapped hourly bars.

The case: an hourly book whose every window has an undefined forecast/return correlation (fewer than 5 active
bars), pooled over 32 windows, on a coin whose first window starts with a hole. The pooled bootstrap read the bar
step from that first pair (3 h), so nearly every hourly bar became its own segment, and its 1,000 resamples each
scanned the segment list once per bar: one call ran for more than a day. Only the observed pooled IC and the method
label are read from that call, so it now asks for those alone (`ic_only`).
"""
import random
import time

import pandas as pd

from backtest.run_protocol import _pooled_ic_with_bootstrap_fallback
from performance.signal_statistics import stationary_block_bootstrap_ic_significance


def _gapped_records(n, seed=7):
    rng = random.Random(seed)
    t0 = pd.Timestamp("2000-01-01")
    out, t = [], t0
    for i in range(n):
        t += pd.Timedelta(hours=3 if i == 1 else (2 if rng.random() < 0.02 else 1))
        out.append({"forecast": rng.choice([0.0, 0.0, 0.0, 1.0, -1.0]), "next_return_bps": rng.gauss(0, 50),
                    "timestamp": t})
    return out


def test_ic_only_gives_the_full_calls_ic_and_method():
    recs = _gapped_records(400)
    for step in (pd.Timedelta(hours=1), pd.Timedelta(hours=3), None):
        steps = {"X": step} if step is not None else None
        full = stationary_block_bootstrap_ic_significance({"X": recs}, expected_step_by_symbol=steps, n_resamples=50)
        short = stationary_block_bootstrap_ic_significance({"X": recs}, expected_step_by_symbol=steps, n_resamples=50,
                                                       ic_only=True)
        assert short == {"method": full["method"], "block_size": full["block_size"],
                         "n_resamples": full["n_resamples"], "pooled_ic": full["pooled_ic"]}


def test_ic_only_on_an_undefined_ic_is_the_full_calls_answer():
    recs = [{"forecast": 1.0, "next_return_bps": float(i), "timestamp": pd.Timestamp("2000-01-01") + pd.Timedelta(hours=i)}
            for i in range(30)]
    full = stationary_block_bootstrap_ic_significance({"X": recs}, n_resamples=10)
    assert stationary_block_bootstrap_ic_significance({"X": recs}, n_resamples=10, ic_only=True) == full


def test_gapped_hourly_symbol_pooled_over_many_windows_finishes(tmp_path):
    """The stalled case at the size it stalled: 93,000 hourly bars in 32 windows, every window's correlation
    undefined, the first window's first pair spanning a 3 h hole. Before the fix this call did not finish."""
    rng = random.Random(11)
    rows, t = [], pd.Timestamp("2000-01-01")
    for w in range(32):
        n = 2905
        ts, closes, forecasts = [], [], []
        price = 100.0
        for i in range(n):
            t += pd.Timedelta(hours=3 if (w == 0 and i == 1) else (2 if rng.random() < 0.02 else 1))
            price *= 1 + rng.gauss(0, 0.01)
            ts.append(t.strftime("%Y-%m-%d %H:%M:%S")); closes.append(round(price, 6))
            forecasts.append(1.0 if i % 700 == 0 else 0.0)
        run_id = f"r{w:02d}"
        (tmp_path / run_id).mkdir()
        pd.DataFrame({"timestamp": ts, "close": closes, "forecast": forecasts}).to_csv(tmp_path / run_id / "bars.csv",
                                                                                        index=False)
        rows.append({"symbol": "XUSD", "window": f"w{w:02d}", "run_id": run_id, "core": {"forecast_return_corr": None}})
    t0 = time.time()
    corr, method = _pooled_ic_with_bootstrap_fallback(rows, tmp_path)
    assert time.time() - t0 < 20
    assert method == "block_bootstrap_all_bars_v1"
    assert corr is not None and -1.0 <= corr <= 1.0
