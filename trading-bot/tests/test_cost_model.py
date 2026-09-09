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
        "binance": {"margin": {"fee_bps": 10, "slippage_bps": {"default": 1.5, "BTCUSDT": 1.0}}},
        "kraken": {"futures": {"fee_bps": 5, "slippage_bps": {"default": 7.5, "BTCUSD": 2.5}}},
    }))
    return str(path)


def test_resolves_configured_combination_raw_table(cost_model_path):
    """symbol=None returns the raw per-symbol slippage table, unresolved."""
    assert resolve_cost_model("binance", "margin", path=cost_model_path) == (
        10.0, {"default": 1.5, "BTCUSDT": 1.0},
    )
    assert resolve_cost_model("kraken", "futures", path=cost_model_path) == (
        5.0, {"default": 7.5, "BTCUSD": 2.5},
    )


def test_resolves_per_symbol_slippage_no_fallback(cost_model_path):
    """A symbol with an explicit table entry resolves to it exactly, with
    used_fallback=False."""
    assert resolve_cost_model("binance", "margin", symbol="BTCUSDT", path=cost_model_path) == (
        10.0, 1.0, False,
    )
    assert resolve_cost_model("kraken", "futures", symbol="BTCUSD", path=cost_model_path) == (
        5.0, 2.5, False,
    )


def test_resolves_per_symbol_slippage_uses_default_fallback(cost_model_path):
    """A symbol absent from the table resolves to "default" with
    used_fallback=True -- the conservative, loudly-logged path (S3)."""
    assert resolve_cost_model("binance", "margin", symbol="ETHUSDT", path=cost_model_path) == (
        10.0, 1.5, True,
    )
    assert resolve_cost_model("kraken", "futures", symbol="AVAXUSD", path=cost_model_path) == (
        5.0, 7.5, True,
    )


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
    2026-09-10 ratified S3 real-calibration ship-time values so an accidental
    edit is caught here, not only by the slow bit-identity backtest."""
    assert resolve_cost_model("binance", "margin", symbol="BTCUSDT") == (10.0, 1.0, False)
    assert resolve_cost_model("binance", "margin", symbol="ETHUSDT") == (10.0, 1.5, False)
    assert resolve_cost_model("binance", "margin", symbol="SOMECOIN") == (10.0, 1.5, True)
    assert resolve_cost_model("kraken", "futures", symbol="BTCUSD") == (5.0, 2.5, False)
    assert resolve_cost_model("kraken", "futures", symbol="ETHUSD") == (5.0, 4.0, False)
    assert resolve_cost_model("kraken", "futures", symbol="AVAXUSD") == (5.0, 7.5, False)
    assert resolve_cost_model("kraken", "futures", symbol="SOLUSD") == (5.0, 7.5, False)
    assert resolve_cost_model("kraken", "futures", symbol="SOMECOIN") == (5.0, 7.5, True)


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
    handler = MockExecutionHandler(slippage_override=SLIPPAGE_BPS)
    success, debug = handler.open_long_position(
        symbol="BTCUSDT", quantity=1.0, trade_type="LONG", data=_bar(),
    )
    assert success
    assert debug["price"] == pytest.approx(CLOSE + _ADJ) == pytest.approx(50025.0)


def test_open_short_fills_below_close():
    """A SELL: seller receives LESS."""
    handler = MockExecutionHandler(slippage_override=SLIPPAGE_BPS)
    success, debug = handler.open_short_position(
        symbol="BTCUSDT", quantity=-1.0, trade_type="SHORT", data=_bar(),
    )
    assert success
    assert debug["price"] == pytest.approx(CLOSE - _ADJ) == pytest.approx(49975.0)


def test_close_long_position_fills_below_close():
    """Closing a LONG (free > locked, position > 0) is economically a SELL."""
    handler = MockExecutionHandler(slippage_override=SLIPPAGE_BPS)
    balances = {"BTCUSDT": {"free": 1.0, "locked": 0.0}}
    success, debug = handler.close_position(symbol="BTCUSDT", data=_bar(), balances=balances)
    assert success
    assert debug["price"] == pytest.approx(CLOSE - _ADJ) == pytest.approx(49975.0)


def test_close_short_position_fills_above_close():
    """Closing a SHORT (locked > free, position < 0) is a buy-to-cover."""
    handler = MockExecutionHandler(slippage_override=SLIPPAGE_BPS)
    balances = {"BTCUSDT": {"free": 0.0, "locked": 1.0}}
    success, debug = handler.close_position(symbol="BTCUSDT", data=_bar(), balances=balances)
    assert success
    assert debug["price"] == pytest.approx(CLOSE + _ADJ) == pytest.approx(50025.0)


def test_zero_slippage_override_is_byte_identical_to_bare_close():
    """slippage_override=0.0 (an explicit override, not the default -- see S3
    below) must reproduce price == close exactly, not merely approximately --
    proves the price-adjustment formula itself is a true no-op at zero."""
    handler = MockExecutionHandler(slippage_override=0.0)
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
# S3 (2026-09-10): real per-symbol slippage is now the DEFAULT (no override
# given) -- resolved from the real committed config/cost_model.json.
# ---------------------------------------------------------------------------

def test_default_construction_resolves_real_btcusdt_slippage():
    """No override given: BTCUSDT (binance/margin, this handler's own
    defaults) resolves to the real committed 1 bps -- NOT zero. This is the
    declared default-behavior change (S3): a bare MockExecutionHandler() no
    longer reproduces price == close."""
    handler = MockExecutionHandler()
    _, debug = handler.open_long_position(
        symbol="BTCUSDT", quantity=1.0, trade_type="LONG", data=_bar(),
    )
    expected_adj = CLOSE * 1.0 / 10000
    assert debug["price"] == pytest.approx(CLOSE + expected_adj)
    assert debug["price"] != CLOSE


def test_unlisted_symbol_falls_back_and_logs_warning(caplog):
    """A symbol with no cost_model.json entry for this (exchange, market_type)
    resolves to the "default" fallback AND logs a warning naming the symbol --
    per S3's explicit requirement that a fallback never silently read as a
    calibrated number."""
    import logging as _logging
    handler = MockExecutionHandler()  # binance/margin
    with caplog.at_level(_logging.WARNING, logger="trading_bot"):
        _, debug = handler.open_long_position(
            symbol="DOGEUSDT", quantity=1.0, trade_type="LONG", data=_bar(),
        )
    expected_adj = CLOSE * 1.5 / 10000  # binance/margin's "default" = 1.5
    assert debug["price"] == pytest.approx(CLOSE + expected_adj)
    fallback_warnings = [r for r in caplog.records if "FALLBACK" in r.message and "DOGEUSDT" in r.message]
    assert fallback_warnings, (
        f"Expected a fallback warning naming DOGEUSDT; got log messages: "
        f"{[r.message for r in caplog.records]}"
    )


def test_calibrated_symbol_does_not_log_fallback_warning(caplog):
    """A symbol WITH a cost_model.json entry (BTCUSDT) must not trigger the
    fallback warning -- only a genuine gap in calibration logs."""
    import logging as _logging
    handler = MockExecutionHandler()  # binance/margin
    with caplog.at_level(_logging.WARNING, logger="trading_bot"):
        handler.open_long_position(
            symbol="BTCUSDT", quantity=1.0, trade_type="LONG", data=_bar(),
        )
    fallback_warnings = [r for r in caplog.records if "FALLBACK" in r.message]
    assert not fallback_warnings, f"Unexpected fallback warning(s): {[r.message for r in fallback_warnings]}"


def test_slippage_override_dict_resolves_per_symbol_with_fallback_logging(caplog):
    """slippage_override as a dict (not a flat float) replaces cost_model.json's
    table wholesale, with the same per-symbol + fallback-logging behavior."""
    import logging as _logging
    handler = MockExecutionHandler(slippage_override={"default": 9.0, "BTCUSDT": 2.0})
    _, btc_debug = handler.open_long_position(
        symbol="BTCUSDT", quantity=1.0, trade_type="LONG", data=_bar(),
    )
    assert btc_debug["price"] == pytest.approx(CLOSE * 1.0002)

    with caplog.at_level(_logging.WARNING, logger="trading_bot"):
        _, eth_debug = handler.open_long_position(
            symbol="ETHUSDT", quantity=1.0, trade_type="LONG", data=_bar(),
        )
    assert eth_debug["price"] == pytest.approx(CLOSE * 1.0009)
    fallback_warnings = [r for r in caplog.records if "FALLBACK" in r.message and "ETHUSDT" in r.message]
    assert fallback_warnings


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
    handler = MockExecutionHandler(slippage_override=SLIPPAGE_BPS)
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
    # slippage_override is threaded into MockExecutionHandler and resolved per
    # SYMBOL at fill time (S3), not upfront as a flat attribute -- verify via
    # the stored override value and via an actual fill.
    handler = _RecordingEngine.kwargs["execution_handler"]
    assert handler.slippage_override == 7.0
    assert handler._resolve_slippage_bps("BTCUSDT") == 7.0
    assert handler._resolve_slippage_bps("ANY_OTHER_SYMBOL") == 7.0  # uniform override, no fallback needed
    from performance.metrics import DEFAULT_COMMISSION_RATE
    assert _RecordingEngine.kwargs["performance_tracker"].commission_rate == DEFAULT_COMMISSION_RATE


def test_cost_model_override_manifest_provenance_reflects_the_override(tmp_path, monkeypatch):
    """The cost_model_provenance folded into the run manifest must reflect the
    OVERRIDE value actually used for fills, not the real committed
    cost_model.json table it bypassed -- provenance must describe what
    actually drove the run's economics (same principle as CUL-55/#54)."""
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
    provenance = _RecordingEngine.kwargs["cost_model_provenance"]
    assert provenance["slippage_bps"] == 7.0
    assert provenance["fee_bps"] == 10.0
    assert provenance["exchange"] == "binance"
    assert provenance["market_type"] == "margin"
