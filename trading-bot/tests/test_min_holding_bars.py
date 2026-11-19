"""strategies.min_holding_bars (2026-11-19, strategy_designer_v2 topics/30): a trade that leaves a position starts a
hold of that many bars, renewed when the forecast asks the held position again; a close to flat starts none. So a
position is held over the horizon its idea claims. Absent (every earlier config):
nothing changes (proof: fixed backtests rerun, files identical; topics/30).

Fast tests: the key is read and validated. Slow test: on real bars, no trade within the hold after a trade that
leaves a position.
  pytest tests/test_min_holding_bars.py -m slow --timeout=0
"""
import json
import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from strategies.main_strategy import AdvancedStrategy
from tools.validate_config import validate


def _base():
    return json.loads((PROJECT_ROOT / "strategy_config.json").read_text())


def test_absent_by_default():
    assert AdvancedStrategy().min_holding_bars is None


def test_read_from_the_config(tmp_path):
    base = _base()
    base["strategies"]["min_holding_bars"] = 24
    (tmp_path / "strategy_config.json").write_text(json.dumps(base))
    assert AdvancedStrategy(config_path=str(tmp_path / "strategy_config.json")).min_holding_bars == 24


@pytest.mark.parametrize("bad", [0, -3, 2.5, "24", True, None])
def test_validate_refuses_a_bad_value(bad):
    base = _base()
    base["strategies"]["min_holding_bars"] = bad
    assert any("V20" in e for e in validate(base))


def test_validate_accepts_an_integer_and_absence():
    base = _base()
    assert not any("V20" in e for e in validate(base))
    base["strategies"]["min_holding_bars"] = 24
    assert not any("V20" in e for e in validate(base))


START, END, SYMBOL = "2024-04-01", "2024-05-30", "BTCUSD"     # Kraken hourly bars (local_data, fetched)


@pytest.mark.slow
def test_no_two_trades_closer_than_the_holding_time(tmp_path):
    from _cache_guard import cache_skip_reason
    reason = cache_skip_reason(PROJECT_ROOT / "local_data", ("kraken_BTCUSD_1h.csv",), START, END)
    if reason:
        pytest.skip(reason)
    from core.launcher import run_backtest

    def run(holding):
        base = _base()
        if holding is not None:
            base["strategies"]["min_holding_bars"] = holding
        d = tmp_path / str(holding)
        d.mkdir()
        (d / "strategy_config.json").write_text(json.dumps(base))
        run_dir = Path(run_backtest(config_path=str(d / "strategy_config.json"), symbol=SYMBOL, start=START, end=END,
                                    results_root=str(d), trades_log_file=str(d / "interim_trades.json"),
                                    exchange="kraken", market_type="futures", interval_seconds=3600))
        bars = pd.read_csv(run_dir / "bars.csv")
        traded = bars["approved_rebalance"].infer_objects(copy=False).fillna(False).astype(bool)
        return bars.index[traded].tolist(), bars["postRebalance_current_allocation"].tolist()

    free, _ = run(None)
    held, alloc = run(24)
    assert held, "the held book traded at least once"
    # a trade that leaves a position starts a hold: the next trade comes 24 bars later at the earliest
    # (a close to flat starts none, so the next entry may follow at once)
    for a, b in zip(held, held[1:]):
        if alloc[a] != 0.0:
            assert b - a >= 24, (a, b)
    assert len(held) <= len(free)
