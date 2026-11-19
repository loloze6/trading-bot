"""The warm-up check (2026-11-18): at the first bar after the warm-up, a copy of the real strategy must be ready, else
the backtest stops (AssertionError, as the replaying probe it replaces did). Real data: SOL is listed on Kraken in
2021-06, so a 2021-09 window whose warm-up needs 912 days cannot be ready; a 2023 window is."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core.launcher import run_backtest  # noqa: E402

CONFIG = {"regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"},
          "strategies": {"regimes": {"unknown": {"components": [
              {"id": "r", "class": "strategies.strategy_components.PriceEvolutionComponent", "params": {"period": 456},
               "weight": 1.0, "transforms": []}]},
              "trending": None, "mean_reversion": None, "chop": None}}}


def run(tmp_path, start, end):
    cfg = tmp_path / "cfg.json"
    cfg.write_text(json.dumps(CONFIG))
    return run_backtest(str(cfg), "SOLUSD", start, end, str(tmp_path), runs_root=str(tmp_path), interval_seconds=86400,
                        warmup_prefetch=True, exchange="kraken", market_type="futures", commission_rate=0.0005)


def test_a_warm_up_too_short_stops_the_backtest(tmp_path):
    with pytest.raises(AssertionError, match="strategy not ready after"):
        run(tmp_path, "2021-09-01", "2021-09-30")


def test_a_warm_up_long_enough_runs(tmp_path):
    assert (Path(run(tmp_path, "2024-09-01", "2024-09-30")) / "metrics.json").exists()
