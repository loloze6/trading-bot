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

_RUN_044_CONFIG = REPO_ROOT / "strategy-research" / "runs" / "run_044" / "artifacts" / "candidate_strategy_config.json"
_FUNDING_CSV = PROJECT_ROOT / "local_data" / "BTCUSDT_funding_8h.csv"
_OHLCV_CSV = PROJECT_ROOT / "local_data" / "BTCUSDT_1h.csv"


def test_threshold_zero_no_longer_raises_directly():
    """Unit-level: the component itself, called with threshold=0.0 and a nonzero
    funding rate at a settlement bar, must not raise."""
    comp = FundingRateMeanReversionComponent(parameters={"threshold": 0.0, "scaling_factor": 10.0})
    bars = pd.DataFrame({
        # Last row must land on a settlement boundary (UTC hour % 8 == 0).
        "timestamp": [pd.Timestamp("2023-12-31 23:00:00"), pd.Timestamp("2024-01-01 00:00:00")],
        "close": [100.0, 100.1],
        "funding_rate": [0.000374, 0.000374],
    })
    comp.update(bars)  # must not raise ZeroDivisionError
    assert comp.raw_value() != 0.0, "component should fire: nonzero funding rate at a settlement bar (hour=0)"
    assert comp.confidence == 1.0, "continuous mode (threshold=0) should report full confidence"


@pytest.mark.skipif(not _RUN_044_CONFIG.exists(), reason="run_044 config not present on disk")
@pytest.mark.skipif(not _FUNDING_CSV.exists() or not _OHLCV_CSV.exists(), reason="local_data fixtures not present")
def test_run_044_config_now_produces_real_active_bars():
    """THE regression: this exact config previously produced active_n_bars=0 (silent
    ZeroDivisionError on every settlement bar). Must now fire."""
    sys.path.insert(0, str(REPO_ROOT / "strategy-research" / "tools"))
    import prescreen_signal as ps

    bars = ps._load_ohlcv("BTCUSDT", "2024-01-01", "2024-01-08")
    merged = ps._merge_aux_feeds(bars, ["funding_rate"], "BTCUSDT", "2024-01-01", "2024-01-08")

    with open(_RUN_044_CONFIG) as f:
        config = json.load(f)
    tmp_path = Path(REPO_ROOT / "trading-bot" / "_tmp_test_run044_config.json")
    tmp_path.write_text(json.dumps(config), encoding="utf-8")
    try:
        strat = AdvancedStrategy(config_path=str(tmp_path))
        active_count = 0
        for i in range(len(merged)):
            bar_row = merged.iloc[i : i + 1]
            strat.update(bar_row)  # must not silently swallow a ZeroDivisionError anymore
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
