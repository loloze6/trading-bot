"""strategies.min_holding_bars (2026-11-20, strategy_designer_v2 topics 30 and 34; the rule: common/forecast.md, point 7;
the code: core/holding_period.py): each bet of the idea is held for its horizon. A bet is a rise of the forecast itself,
on its own side, of at least the band (min_allocation_change), measured from its lowest level on that side since its
last bet; a long book does not go below the sum of its long bets still within their horizon (at most its position), a
short book symmetrically. Absent (every earlier config): nothing changes (proof: fixed backtests rerun, files identical;
topics/30). The bet-by-bet cases are in tests/test_holding_period.py.

Fast tests: the key is read and validated. Slow test: on real bars, a held book trades no more than the same book
without the key.
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
def test_a_held_book_trades_no_more_than_a_free_one(tmp_path):
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
    assert len(held) <= len(free)
