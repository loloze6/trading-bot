"""
Unit + fast-integration tests for E-010's cost model resolver
(config/cost_model.py::resolve_cost_model) and the slippage price-adjustment
formulas it feeds in execution/execution_handler.py::MockExecutionHandler.

Fee resolution and price-adjustment are pure functions of small, hand-computable
inputs -- these tests assert the code matches manual arithmetic exactly rather
than tolerance-comparing against a captured fixture. The one integration piece
(an unconfigured (exchange, market_type) raising through run_backtest) is fast
because config/cost_model.py's lookup happens before any data fetch -- no cache
guard, no @pytest.mark.slow needed.

See tests/test_commission_rate_param.py and tests/test_risk_layer_bit_identical.py
for the slow, full-engine bit-identity/delta tests covering the same feature at
the run-artifact level.
"""
import json
import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.cost_model import resolve_cost_model, UnknownCostModelError  # noqa: E402
from execution.execution_handler import MockExecutionHandler  # noqa: E402
from execution.portfolio_info import MockPortfolioInfo  # noqa: E402


# ---------------------------------------------------------------------------
# resolve_cost_model
# ---------------------------------------------------------------------------

@pytest.fixture
def cost_model_path(tmp_path):
    path = tmp_path / "cost_model.json"
    path.write_text(json.dumps({
        "binance": {"margin": {"fee_bps": 10, "slippage_bps": 0}},
        "kraken": {"futures": {"fee_bps": 5, "slippage_bps": 0}},
    }))
    return str(path)


def test_resolves_configured_combination(cost_model_path):
    assert resolve_cost_model("binance", "margin", path=cost_model_path) == (10.0, 0.0)
    assert resolve_cost_model("kraken", "futures", path=cost_model_path) == (5.0, 0.0)


def test_unconfigured_exchange_raises_loud(cost_model_path):
    with pytest.raises(UnknownCostModelError, match="unicorn.*margin"):
        resolve_cost_model("unicorn", "margin", path=cost_model_path)


def test_unconfigured_market_type_raises_loud(cost_model_path):
    """Exchange exists but not this market_type -- must still raise, not fall
    back to some other market_type entry for the same exchange."""
    with pytest.raises(UnknownCostModelError, match="binance.*futures"):
        resolve_cost_model("binance", "futures", path=cost_model_path)


def test_unknown_cost_model_error_is_a_key_error(cost_model_path):
    """Subclassing KeyError is deliberate (the failing lookup is a dict lookup);
    the message must still name the exact missing combination, unlike a bare
    KeyError, which would only show the innermost missing key."""
    with pytest.raises(KeyError):
        resolve_cost_model("unicorn", "margin", path=cost_model_path)


def test_committed_cost_model_json_resolves_the_ship_time_entries():
    """The real, tracked config/cost_model.json (no path override) -- pins the
    2026-09-09 ratified ship-time values so an accidental edit is caught here,
    not only by the slow bit-identity backtest."""
    assert resolve_cost_model("binance", "margin") == (10.0, 0.0)
    assert resolve_cost_model("kraken", "futures") == (5.0, 0.0)


# ---------------------------------------------------------------------------
# MockExecutionHandler slippage direction (hand-computed)
# ---------------------------------------------------------------------------

CLOSE = 50000.0
SLIPPAGE_BPS = 5.0  # 0.05%
_ADJ = CLOSE * SLIPPAGE_BPS / 10000  # 25.0


def _bar(close=CLOSE):
    return pd.DataFrame({"close": [close], "timestamp": [pd.Timestamp("2024-01-01")]})


def test_open_long_fills_above_close():
    """A BUY: buyer pays MORE."""
    handler = MockExecutionHandler(slippage_bps=SLIPPAGE_BPS)
    success, debug = handler.open_long_position(
        symbol="BTCUSDT", quantity=1.0, trade_type="LONG", data=_bar(),
    )
    assert success
    assert debug["price"] == pytest.approx(CLOSE + _ADJ) == pytest.approx(50025.0)


def test_open_short_fills_below_close():
    """A SELL: seller receives LESS."""
    handler = MockExecutionHandler(slippage_bps=SLIPPAGE_BPS)
    success, debug = handler.open_short_position(
        symbol="BTCUSDT", quantity=-1.0, trade_type="SHORT", data=_bar(),
    )
    assert success
    assert debug["price"] == pytest.approx(CLOSE - _ADJ) == pytest.approx(49975.0)


def test_close_long_position_fills_below_close():
    """Closing a LONG (free > locked, position > 0) is economically a SELL."""
    handler = MockExecutionHandler(slippage_bps=SLIPPAGE_BPS)
    balances = {"BTCUSDT": {"free": 1.0, "locked": 0.0}}
    success, debug = handler.close_position(symbol="BTCUSDT", data=_bar(), balances=balances)
    assert success
    assert debug["price"] == pytest.approx(CLOSE - _ADJ) == pytest.approx(49975.0)


def test_close_short_position_fills_above_close():
    """Closing a SHORT (locked > free, position < 0) is a buy-to-cover."""
    handler = MockExecutionHandler(slippage_bps=SLIPPAGE_BPS)
    balances = {"BTCUSDT": {"free": 0.0, "locked": 1.0}}
    success, debug = handler.close_position(symbol="BTCUSDT", data=_bar(), balances=balances)
    assert success
    assert debug["price"] == pytest.approx(CLOSE + _ADJ) == pytest.approx(50025.0)


def test_zero_slippage_is_byte_identical_to_bare_close():
    """slippage_bps=0.0 (the default) must reproduce price == close exactly,
    not merely approximately -- the bit-identity contract for this feature."""
    handler = MockExecutionHandler()  # slippage_bps defaults to 0.0
    _, long_debug = handler.open_long_position(
        symbol="BTCUSDT", quantity=1.0, trade_type="LONG", data=_bar(),
    )
    _, short_debug = handler.open_short_position(
        symbol="BTCUSDT", quantity=-1.0, trade_type="SHORT", data=_bar(),
    )
    _, close_debug = handler.close_position(
        symbol="BTCUSDT", data=_bar(), balances={"BTCUSDT": {"free": 1.0, "locked": 0.0}},
    )
    assert long_debug["price"] == CLOSE
    assert short_debug["price"] == CLOSE
    assert close_debug["price"] == CLOSE


# ---------------------------------------------------------------------------
# Fee formula (hand-computed) -- the same adjusted price flowing into the
# portfolio_info.py commission consumer
# ---------------------------------------------------------------------------

def test_fee_and_slippage_combine_as_hand_computed():
    """
    Buy 1 unit at close=$50,000 with slippage_bps=5, fee_bps=10:
      adjusted price = 50000 * 1.0005          = 50025.0
      cost            = adjusted_price * qty    = 50025.0
      commission      = fee_bps / 10000         = 0.001
      received_qty    = qty * (1 - commission)  = 0.999

    Exercises the actual single-seam price flow: MockExecutionHandler computes
    the slippage-adjusted price, and that exact value is what
    CommonPortfolioDef.update_local_balance (the portfolio_info.py fee consumer)
    receives and applies its own, independently-configured fee to.
    """
    fee_bps = 10.0
    commission_rate = fee_bps / 10000
    handler = MockExecutionHandler(slippage_bps=SLIPPAGE_BPS)
    _, debug = handler.open_long_position(
        symbol="BTCUSDT", quantity=1.0, trade_type="LONG", data=_bar(),
    )
    adjusted_price = debug["price"]
    assert adjusted_price == pytest.approx(50025.0)

    portfolio = MockPortfolioInfo(
        initial_balance={"USDT": {"free": 100000.0, "locked": 0.0}},
        commission_rate=commission_rate,
    )
    portfolio.update_local_balance(
        symbol="BTCUSDT", price=adjusted_price, quantity=1.0, trade_type="LONG",
    )

    expected_cost = adjusted_price * 1.0
    expected_received_qty = 1.0 * (1 - commission_rate)
    assert expected_cost == pytest.approx(50025.0)
    assert expected_received_qty == pytest.approx(0.999)
    assert portfolio.local_balance["USDT"]["free"] == pytest.approx(100000.0 - expected_cost)
    assert portfolio.local_balance["BTCUSDT"]["free"] == pytest.approx(expected_received_qty)


# ---------------------------------------------------------------------------
# run_backtest() fail-loud on an unconfigured (exchange, market_type) -- fast,
# fires before any data fetch (config/cost_model.py's lookup happens first).
# ---------------------------------------------------------------------------

_RUN_BACKTEST_CONFIG = PROJECT_ROOT / "tests" / "fixtures" / "warmup_prefetch_check_config.json"


def test_run_backtest_raises_loud_on_unconfigured_market_type(tmp_path):
    """binance/futures has no cost_model.json entry (only binance/margin and
    kraken/futures are configured) -- run_backtest must raise before touching
    any data, not silently fall back to DEFAULT_COMMISSION_RATE."""
    from core.launcher import run_backtest

    with pytest.raises(UnknownCostModelError):
        run_backtest(
            config_path=str(_RUN_BACKTEST_CONFIG),
            symbol="BTCUSDT", start="2024-01-01", end="2024-01-02",
            results_root=str(tmp_path / "results"),
            trades_log_file=str(tmp_path / "trades.json"),
            exchange="binance",
            market_type="futures",
        )


def test_run_backtest_default_market_type_resolves_to_margin(monkeypatch, tmp_path):
    """Omitting market_type (default None) must resolve to config's absent-default
    'margin', matching binance's real committed cost_model.json entry -- so the
    default path never raises."""
    import pandas as pd
    from typing import ClassVar
    import core.launcher as launcher_mod
    from core.launcher import run_backtest

    class _RecordingEngine:
        kwargs: ClassVar[dict] = {}

        def __init__(self, **kwargs):
            type(self).kwargs = kwargs
            self._last_run_dir = None
            self.historical_data = {}

        def load_data(self, **kwargs):
            self.historical_data["BTCUSDT"] = pd.DataFrame(
                {"timestamp": [pd.Timestamp("2024-01-01")], "close": [1.0]}
            )

        def simulate_on_loaded_data(self):
            pass

    monkeypatch.setattr(launcher_mod, "BacktestEngine", _RecordingEngine)
    run_backtest(
        config_path=str(_RUN_BACKTEST_CONFIG),
        symbol="BTCUSDT", start="2024-01-01", end="2024-01-02",
        results_root=str(tmp_path / "results"),
        trades_log_file=str(tmp_path / "trades.json"),
    )
    # binance/margin resolves to fee_bps=10 -> commission_rate=0.001, the exact
    # pre-existing DEFAULT_COMMISSION_RATE value -- the byte-identity contract.
    from performance.metrics import DEFAULT_COMMISSION_RATE
    assert _RecordingEngine.kwargs["performance_tracker"].commission_rate == DEFAULT_COMMISSION_RATE
    assert _RecordingEngine.kwargs["portfolio_info"].commission_rate == DEFAULT_COMMISSION_RATE


# ---------------------------------------------------------------------------
# cost_model_override -- test-only knob for exercising nonzero slippage
# ---------------------------------------------------------------------------

def test_cost_model_override_replaces_only_the_keys_given(tmp_path, monkeypatch):
    """cost_model_override supplies slippage_bps only; fee_bps still comes from
    the real binance/margin resolution (10 bps)."""
    import pandas as pd
    from typing import ClassVar
    import core.launcher as launcher_mod
    from core.launcher import run_backtest

    class _RecordingEngine:
        kwargs: ClassVar[dict] = {}

        def __init__(self, **kwargs):
            type(self).kwargs = kwargs
            self._last_run_dir = None
            self.historical_data = {}

        def load_data(self, **kwargs):
            self.historical_data["BTCUSDT"] = pd.DataFrame(
                {"timestamp": [pd.Timestamp("2024-01-01")], "close": [1.0]}
            )

        def simulate_on_loaded_data(self):
            pass

    monkeypatch.setattr(launcher_mod, "BacktestEngine", _RecordingEngine)
    run_backtest(
        config_path=str(_RUN_BACKTEST_CONFIG),
        symbol="BTCUSDT", start="2024-01-01", end="2024-01-02",
        results_root=str(tmp_path / "results"),
        trades_log_file=str(tmp_path / "trades.json"),
        cost_model_override={"slippage_bps": 7.0},
    )
    assert _RecordingEngine.kwargs["execution_handler"].slippage_bps == 7.0
    from performance.metrics import DEFAULT_COMMISSION_RATE
    assert _RecordingEngine.kwargs["performance_tracker"].commission_rate == DEFAULT_COMMISSION_RATE
