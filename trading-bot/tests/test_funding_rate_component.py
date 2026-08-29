"""
F5a (P1a shakedown, 2026-07-04) regression test.

FundingRateMeanReversionComponent's confidence calculation
(`abs(funding_rate) / (self.threshold * 3.0)`) divided by zero whenever
threshold=0.0 — the exact, intentional "continuous mode" design (fire at every
settlement regardless of magnitude, not just extremes). The exception was silently
swallowed by main_strategy.update()'s broad exception handler, so the component's
computed signal never reached history — run_044's real config (threshold=0.0)
produced active_n_bars=0 in prescreen, which read as "no signal" when the actual
cause was this crash on every single settlement bar.

Fixture: run_044's actual candidate_strategy_config.json + real cached BTC bars,
reproducing the exact failure end-to-end (not just unit-testing the component in
isolation) via AdvancedStrategy directly, the same path prescreen_signal.py uses.
"""

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).parent.parent
REPO_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(REPO_ROOT / "strategy-research" / "tools"))

from strategies.strategy_components import FundingRateMeanReversionComponent
from strategies.main_strategy import AdvancedStrategy

_RUN_044_CONFIG = (
    REPO_ROOT
    / "strategy-research"
    / "runs"
    / "run_044"
    / "artifacts"
    / "candidate_strategy_config.json"
)
_FUNDING_CSV = PROJECT_ROOT / "local_data" / "BTCUSDT_funding_8h.csv"
_OHLCV_CSV = PROJECT_ROOT / "local_data" / "BTCUSDT_1h.csv"


def test_threshold_zero_no_longer_raises_directly():
    """Unit-level: the component itself, called with threshold=0.0 and a nonzero
    funding rate at a settlement bar, must not raise."""
    comp = FundingRateMeanReversionComponent(
        parameters={"threshold": 0.0, "scaling_factor": 10.0}
    )
    bars = pd.DataFrame(
        {
            # Last row must land on a settlement boundary (UTC hour % 8 == 0).
            "timestamp": [
                pd.Timestamp("2023-12-31 23:00:00"),
                pd.Timestamp("2024-01-01 00:00:00"),
            ],
            "close": [100.0, 100.1],
            "funding_rate": [0.000374, 0.000374],
        }
    )
    comp.update(bars)  # must not raise ZeroDivisionError
    assert comp.raw_value() != 0.0, (
        "component should fire: nonzero funding rate at a settlement bar (hour=0)"
    )
    assert comp.confidence == 1.0, (
        "continuous mode (threshold=0) should report full confidence"
    )


@pytest.mark.skipif(
    not _RUN_044_CONFIG.exists(), reason="run_044 config not present on disk"
)
@pytest.mark.skipif(
    not _FUNDING_CSV.exists() or not _OHLCV_CSV.exists(),
    reason="local_data fixtures not present",
)
def test_run_044_config_now_produces_real_active_bars():
    """THE regression: this exact config previously produced active_n_bars=0 (silent
    ZeroDivisionError on every settlement bar). Must now fire."""
    sys.path.insert(0, str(REPO_ROOT / "strategy-research" / "tools"))
    import prescreen_signal as ps

    bars = ps._load_ohlcv("BTCUSDT", "2024-01-01", "2024-01-08")
    merged = ps._merge_aux_feeds(
        bars, ["funding_rate"], "BTCUSDT", "2024-01-01", "2024-01-08"
    )

    with open(_RUN_044_CONFIG) as f:
        config = json.load(f)
    tmp_path = Path(REPO_ROOT / "trading-bot" / "_tmp_test_run044_config.json")
    tmp_path.write_text(json.dumps(config), encoding="utf-8")
    try:
        strat = AdvancedStrategy(config_path=str(tmp_path))
        active_count = 0
        for i in range(len(merged)):
            bar_row = merged.iloc[i : i + 1]
            strat.update(
                bar_row
            )  # must not silently swallow a ZeroDivisionError anymore
            if strat.is_ready():
                forecast, *_ = strat.generate_forecast()
                if abs(forecast) > 1e-6:
                    active_count += 1
        assert active_count > 0, (
            "run_044's config produced zero active bars again — the threshold=0 fix "
            "did not resolve the original failure, or a new regression was introduced"
        )
    finally:
        tmp_path.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# run_059 (2026-07-18) regression: CandleBuilder._align() used naive
# datetime.timestamp()/datetime.fromtimestamp(), which silently round-trips
# through the LOCAL system timezone instead of UTC. This is a no-op for
# interval_seconds that are an exact multiple of the local UTC offset (e.g.
# 3600s -- any whole-hour offset cancels through the floor), but shifted
# every 86400s/1d candle's start_time to a fixed non-zero hour (never 0),
# which made FundingRateMeanReversionComponent's settlement-boundary check
# (hour % 8 == 0) fail on every single daily bar -- a silent, total
# zero-forecast with no exception anywhere. Confirmed via in-process repro
# driving the real DataManager/CandleBuilder chain before any fix; see the
# implementation-agent session log for the repro output. Fixed in
# CandleBuilder._align() (data/data_manager.py) by making the UTC
# interpretation explicit.
# ---------------------------------------------------------------------------

_FUNDING_CSV_1D = PROJECT_ROOT / "local_data" / "BTCUSDT_funding_8h.csv"
_OHLCV_CSV_1D = PROJECT_ROOT / "local_data" / "BTCUSDT_1d.csv"


@pytest.mark.skipif(
    not _FUNDING_CSV_1D.exists() or not _OHLCV_CSV_1D.exists(),
    reason="local_data fixtures not present",
)
def test_daily_bars_with_merged_funding_produce_nonzero_forecasts():
    """Component-level: FundingRateMeanReversionComponent on DAILY (86400s-
    aligned, hour=00:00) bars with real merged funding data over a small
    2019-12 window must fire (nonzero forecast) on every settlement day --
    daily bars ARE settlement bars (hour%8==0 whenever hour==0)."""
    sys.path.insert(0, str(REPO_ROOT / "strategy-research" / "tools"))
    import prescreen_signal as ps

    bars = ps._load_ohlcv("BTCUSDT", "2019-12-01", "2019-12-06", timeframe="1d")
    merged = ps._merge_aux_feeds(
        bars, ["funding_rate"], "BTCUSDT", "2019-12-01", "2019-12-06"
    )

    assert len(merged) >= 3, (
        "fixture window too small to be a meaningful regression test"
    )
    assert all(pd.Timestamp(t).hour == 0 for t in merged["timestamp"]), (
        "fixture bars must be at hour=00:00 (the whole point of a DAILY bar)"
    )

    comp = FundingRateMeanReversionComponent(
        parameters={"threshold": 0.0, "scaling_factor": 10.0}
    )
    fired_days = 0
    for i in range(1, len(merged) + 1):
        window = merged.iloc[:i]
        comp.update(window)
        if comp.is_ready() and abs(comp.raw_value()) > 1e-9:
            fired_days += 1

    assert fired_days > 0, (
        "no daily bar fired -- the 1d silent-zero-forecast regression (run_059) "
        "has recurred"
    )
    assert fired_days == len(merged) - 1, (
        f"expected every ready bar to fire (continuous mode, threshold=0, real "
        f"funding rate never exactly 0.0 in this fixture) -- got {fired_days}/{len(merged) - 1}"
    )


@pytest.mark.skipif(
    not _FUNDING_CSV_1D.exists() or not _OHLCV_CSV_1D.exists(),
    reason="local_data fixtures not present",
)
def test_data_manager_merge_attach_chain_yields_funding_column_at_1d():
    """Chain-level: the REAL DataManager merge/attach path (register_feed ->
    initialize -> _premerge_aux_feeds -> CandleBuilder.add_row -> _align ->
    get_data_history -> _attach_aux_columns), driven exactly as protocol
    execution does, at interval_seconds=86400, must yield completed candles
    at hour=00:00 with a fully non-null funding_rate column for the same
    fixture window."""
    from data.data_manager import DataManager
    from data.fetchers.funding_rate_fetcher import FundingRateFetcher

    start = pd.Timestamp("2019-12-01").to_pydatetime()
    end = pd.Timestamp("2019-12-06").to_pydatetime()
    symbol = "BTCUSDT"

    dm = DataManager([symbol], interval_seconds=86400, mode="backtest")
    dm.register_feed(
        name="funding_rate",
        fetcher=FundingRateFetcher(
            start,
            end,
            symbols=[symbol],
            localStorage=True,
            data_dir=str(PROJECT_ROOT / "local_data"),
        ),
        window_seconds=0,  # published instantaneously — no forward window
        agg="last",
    )
    dm.historical_data[symbol] = dm.fetch_historical_data(symbol, start, end)
    dm.initialize()
    dm.candle_builder.candle_completion_callback = (
        None  # bypass default callback wiring (see repro note)
    )

    n_rows = len(dm.historical_data[symbol])
    assert n_rows >= 3, "fixture window too small to be a meaningful regression test"

    completed_timestamps = []
    for idx in range(n_rows):
        row = dm.historical_data[symbol].iloc[idx]
        candle = dm.candle_builder.add_row(row, symbol)
        if candle is not None:
            completed_timestamps.append(candle.start_time)

    assert completed_timestamps, "no candle completed -- fixture window too small"
    assert all(t.hour == 0 for t in completed_timestamps), (
        f"CandleBuilder produced misaligned daily candle(s) (hour != 0): "
        f"{[t for t in completed_timestamps if t.hour != 0]} -- the run_059 "
        f"local-timezone alignment bug has recurred"
    )

    data = dm.get_data_history(symbol, count=n_rows)
    assert "funding_rate" in data.columns
    assert data["funding_rate"].notna().all(), (
        f"expected full non-null funding_rate coverage over this fixture window, "
        f"got {data['funding_rate'].notna().sum()}/{len(data)}"
    )
