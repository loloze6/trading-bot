"""
E-039 step 5 follow-up (2026-09-12): forecast_return_corr is measured on
ACTIVE bars only (forecast != 0) -- the "gated" IC docs/USER_GUIDE.md and
verdict-interpreter's SKILL.md both warn is NOT admissible for the A2.1
ungated-escape criterion, which needs IC over ALL bars, no activity filter.

That "ic_all_bars" quantity used to be computed only inside the now-removed
signal_prescreen stage's own _resolve_ungated_escape (deleted, E-039 step 5
Phase 3, along with the rest of that stage). Relocated here into build_core
as a new additive field, forecast_return_corr_all_bars (+ its block-adjusted
p-value/n_eff counterpart), reusing df_all -- the same all-bars, gap-filtered
population sigma_bar_bps already measures a few lines above -- rather than
loading anything separately.

Three properties pinned:
1. Always-active strategy: forecast_return_corr_all_bars == forecast_return_corr
   exactly (df_all == df when forecast is never 0), the expected degenerate case.
2. Regime-gated strategy (forecast == 0 on some bars): the two values DIVERGE,
   and forecast_return_corr_all_bars is computed over strictly more rows.
3. None-handling matches the existing active-bar fields' convention (not
   measured yet, never a fabricated 0.0): absent below 5 all-bars rows, or
   when candle_interval_seconds isn't supplied for the p-value/n_eff pair.
"""
import sys
from pathlib import Path

import pandas as pd

TRADING_BOT_ROOT = Path(__file__).parent.parent
if str(TRADING_BOT_ROOT) not in sys.path:
    sys.path.insert(0, str(TRADING_BOT_ROOT))

from reporting.run_artifact import build_core
from performance.signal_statistics import pearson_correlation


def _bars(forecasts, closes, freq="h", start="2020-01-01"):
    return pd.DataFrame({
        "timestamp": pd.date_range(start, periods=len(forecasts), freq=freq),
        "forecast": forecasts,
        "close": closes,
    })


def _varying_series(n=60):
    forecasts = [((-1) ** i) * (5 + i % 5) for i in range(n)]
    closes = [100 + sum(forecasts[:i + 1]) * 0.01 for i in range(n)]
    return forecasts, closes


def test_always_active_strategy_all_bars_equals_active_only():
    """No bar has forecast == 0, so df_all == df -- the two corr fields must
    be identical, not just close."""
    forecasts, closes = _varying_series(n=80)
    bars = _bars(forecasts, closes)
    core = build_core({}, [], bars, candle_interval_seconds=3600)

    assert core["forecast_return_corr"] is not None
    assert core["forecast_return_corr_all_bars"] == core["forecast_return_corr"]
    assert (core["forecast_return_corr_all_bars_pvalue_block_adjusted"]
            == core["forecast_return_corr_pvalue_block_adjusted"])
    assert core["forecast_return_corr_all_bars_n_eff"] == core["forecast_return_corr_n_eff"]


def test_regime_gated_strategy_all_bars_diverges_from_active_only():
    """Half the bars carry forecast == 0 (simulating a regime gate). The
    active-only corr must ignore them; the all-bars corr must not.

    Price motion is driven independently of the forecast-gating pattern (a
    plain incrementing walk), not by cumulative-summing the (partly-zeroed)
    forecast itself -- doing the latter makes every active bar's own
    forward_return come out identically 0 (each active/even bar is always
    followed by a zero-forecast/odd bar, so price never moves on the very
    step being measured), a zero-variance fixture artifact that would make
    forecast_return_corr None for the wrong reason."""
    n = 80
    walk = [((-1) ** i) * (i % 7) for i in range(n)]  # independent of the gating below
    closes = [100 + sum(walk[:i + 1]) * 0.01 for i in range(n)]
    forecasts = [((-1) ** (i // 2)) * (5 + i % 5) if i % 2 == 0 else 0 for i in range(n)]
    bars = _bars(forecasts, closes)

    core = build_core({}, [], bars, candle_interval_seconds=3600)

    assert core["forecast_return_corr"] is not None
    assert core["forecast_return_corr_all_bars"] is not None
    # Reproduce the populations directly to prove the divergence is exactly
    # "gated vs ungated," not an unrelated numerical accident.
    df_all = bars[["forecast", "close"]].copy()
    df_all["forward_return"] = df_all["close"].shift(-1) / df_all["close"] - 1
    df_all = df_all.dropna()
    df_active = df_all[df_all["forecast"] != 0]

    assert len(df_all) > len(df_active), (
        "the gated fixture must leave strictly more rows in the all-bars "
        "population than the active-only one, or this test proves nothing"
    )
    expected_all = pearson_correlation(
        df_all["forecast"].values.astype(float), df_all["forward_return"].values.astype(float)
    )
    assert core["forecast_return_corr_all_bars"] == round(expected_all, 6)
    assert core["forecast_return_corr_all_bars"] != core["forecast_return_corr"], (
        "gated (active-only) and ungated (all-bars) IC must be measured over "
        "different populations for a regime-gated config -- if they're equal "
        "here, the all-bars field isn't actually using df_all"
    )


def test_all_bars_corr_none_when_fewer_than_5_rows():
    forecasts, closes = _varying_series(n=4)
    bars = _bars(forecasts, closes)
    core = build_core({}, [], bars, candle_interval_seconds=3600)
    assert core["forecast_return_corr_all_bars"] is None
    assert core["forecast_return_corr_all_bars_pvalue_block_adjusted"] is None
    assert core["forecast_return_corr_all_bars_n_eff"] is None


def test_all_bars_pvalue_and_n_eff_none_without_candle_interval():
    """Matches the active-bar fields' own convention: the raw corr can still
    be computed, but the block-adjusted significance needs a block size."""
    forecasts, closes = _varying_series(n=80)
    bars = _bars(forecasts, closes)
    core = build_core({}, [], bars)  # no candle_interval_seconds

    assert core["forecast_return_corr_all_bars"] is not None
    assert core["forecast_return_corr_all_bars_pvalue_block_adjusted"] is None
    assert core["forecast_return_corr_all_bars_n_eff"] is None


def test_default_call_signature_still_byte_identical():
    """The old 3-positional-arg call (no candle_interval_seconds, no symbol)
    must still produce every pre-existing field unchanged; the new fields
    just default to None like every other additive field in this function."""
    forecasts, closes = _varying_series(n=60)
    bars = _bars(forecasts, closes)
    core = build_core({}, [], bars)

    assert core["forecast_return_corr"] is not None
    assert core["forecast_return_corr_all_bars"] is not None
    assert core["forecast_return_corr_all_bars_pvalue_block_adjusted"] is None
    assert core["forecast_return_corr_all_bars_n_eff"] is None
