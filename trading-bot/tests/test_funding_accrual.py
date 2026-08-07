"""
Tests for the off-by-default funding-accrual mechanism (design 2026-07-24 §5,
strategy-research/engineering/sessions/session_reports/20260724_funding_cashflow_model_design.md).

Covers:
  * The 8 worked numeric examples in design §5(d) — CommonPortfolioDef.apply_funding
    and the daily-summed funding series builder.
  * TIMING / LOOK-AHEAD — funding is charged on the position held INTO the bar (not the
    one rebalanced into), and the 00:00 UTC settlement lands on exactly ONE bar.
  * FLAG-OFF BYTE-IDENTITY — a bar-level total_portfolio_value series with
    model_funding=False is identical whether or not a funding feed is present, proving
    the default path is untouched; flag-on rises by exactly the funding credit.

All tests are fast (no full launcher backtest): the byte-identity / integration cases
drive TradingBot._process_symbol_candle_completion directly over lightweight stubs.
"""
import logging
import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from execution.portfolio_info import MockPortfolioInfo
from data.feed_registry import build_daily_funding_series
from core.trading_bot import TradingBot

SYMBOL = "BTCUSDT"


# ---------------------------------------------------------------------------
# §5(d) examples 1-4, 7 — apply_funding accrual mechanics
# ---------------------------------------------------------------------------

def _portfolio(free_qty=0.0, locked_qty=0.0, usdt_free=100000.0):
    p = MockPortfolioInfo(initial_balance={
        "USDT": {"free": usdt_free, "locked": 0.0},
        SYMBOL: {"free": free_qty, "locked": locked_qty},
    })
    return p


def test_example1_long_pays_on_positive_funding():
    """+1.0 BTC @ 20,000, f_bar=+0.0003 → USDT.free Δ = -6.00 (long pays)."""
    p = _portfolio(free_qty=1.0)
    before = p.local_balance["USDT"]["free"]
    cf = p.apply_funding(SYMBOL, 20000.0, 0.0003)
    assert cf == pytest.approx(-6.00)
    assert p.local_balance["USDT"]["free"] - before == pytest.approx(-6.00)


def test_example2_short_receives_on_positive_funding():
    """-1.0 BTC @ 20,000, f_bar=+0.0003 → Δ = +6.00 (short receives)."""
    p = _portfolio(locked_qty=1.0)
    before = p.local_balance["USDT"]["free"]
    cf = p.apply_funding(SYMBOL, 20000.0, 0.0003)
    assert cf == pytest.approx(+6.00)
    assert p.local_balance["USDT"]["free"] - before == pytest.approx(+6.00)


def test_example3_sign_flip_short_pays_when_funding_negative():
    """-1.0 BTC @ 20,000, f_bar=-0.0002 → Δ = -4.00 (short pays)."""
    p = _portfolio(locked_qty=1.0)
    cf = p.apply_funding(SYMBOL, 20000.0, -0.0002)
    assert cf == pytest.approx(-4.00)


def test_example4_flat_position_zero():
    """No open position → Δ = 0 regardless of f_bar."""
    p = _portfolio()
    before = p.local_balance["USDT"]["free"]
    for f in (0.0003, -0.0002, 0.0):
        assert p.apply_funding(SYMBOL, 20000.0, f) == 0.0
    assert p.local_balance["USDT"]["free"] == before


def test_example7_fee_funding_orthogonality():
    """A bar with an open position and NO trade applies funding but zero commission;
    a trade event applies commission on the trade and funding is a separate additive
    cash flow on held notional — the two adjust independently."""
    # No-trade bar: funding only, commission untouched.
    p = _portfolio(locked_qty=1.0)
    usdt_before = p.local_balance["USDT"]["free"]
    p.apply_funding(SYMBOL, 20000.0, 0.0003)
    assert p.local_balance["USDT"]["free"] - usdt_before == pytest.approx(+6.00)

    # Trade event uses commission; funding is orthogonal (different code path, no
    # interaction term). Apply a LONG trade then funding on the resulting held notional.
    q = _portfolio(usdt_free=100000.0)
    q.apply_funding  # no-op reference; ensure the two paths don't share state
    q.update_local_balance(SYMBOL, price=20000.0, quantity=1.0, trade_type="LONG")
    # commission haircut applied at the trade: received qty < 1.0
    held = q.local_balance[SYMBOL]["free"]
    assert held == pytest.approx(1.0 * (1 - q.commission_rate))
    usdt_after_trade = q.local_balance["USDT"]["free"]
    cf = q.apply_funding(SYMBOL, 20000.0, 0.0003)
    # funding is on the held notional only, independent of the commission just paid
    assert cf == pytest.approx(-held * 20000.0 * 0.0003)
    assert q.local_balance["USDT"]["free"] - usdt_after_trade == pytest.approx(cf)


# ---------------------------------------------------------------------------
# §5(d) examples 5-6 + settlement-boundary timing — the daily series builder
# ---------------------------------------------------------------------------

def _write_funding_csv(data_dir, rows):
    """rows: list of (timestamp_str, funding_rate)."""
    df = pd.DataFrame(rows, columns=["timestamp", "funding_rate"])
    df["mark_price"] = ""
    path = Path(data_dir) / f"{SYMBOL}_funding_8h.csv"
    df.to_csv(path, index=False)
    return path


def test_example5_daily_aggregation_by_sum(tmp_path):
    """8h rates [+0.0001, +0.0001, -0.0002] for a day → f_bar = 0.0 (SUM, not
    forward-fill-last which would wrongly use -0.0002)."""
    _write_funding_csv(tmp_path, [
        ("2024-01-01 00:00:00", 0.0001),
        ("2024-01-01 08:00:00", 0.0001),
        ("2024-01-01 16:00:00", -0.0002),
    ])
    series = build_daily_funding_series([SYMBOL], str(tmp_path))
    day = pd.Timestamp("2024-01-01")
    assert series[SYMBOL][day] == pytest.approx(0.0)
    # long accrual on a 0.0 daily funding is exactly 0
    p = _portfolio(free_qty=1.0)
    assert p.apply_funding(SYMBOL, 20000.0, series[SYMBOL][day]) == 0.0


def test_example6_partial_day_no_imputation(tmp_path):
    """Only two settlements present → f_bar sums the two; no third is imputed."""
    _write_funding_csv(tmp_path, [
        ("2024-01-02 00:00:00", 0.0001),
        ("2024-01-02 08:00:00", 0.0004),
        # 16:00 missing
    ])
    series = build_daily_funding_series([SYMBOL], str(tmp_path))
    assert series[SYMBOL][pd.Timestamp("2024-01-02")] == pytest.approx(0.0005)


def test_settlement_boundary_00utc_lands_on_exactly_one_bar(tmp_path):
    """The 00:00 UTC settlement is dated to its OWN day, counted once — no double-count
    or leak across the daily boundary."""
    _write_funding_csv(tmp_path, [
        ("2024-01-03 00:00:00", 0.0001),
        ("2024-01-03 08:00:00", 0.0002),
        ("2024-01-03 16:00:00", 0.0003),
        ("2024-01-04 00:00:00", 0.0007),   # belongs to Jan-04, not Jan-03
        ("2024-01-04 08:00:00", 0.0001),
    ])
    series = build_daily_funding_series([SYMBOL], str(tmp_path))[SYMBOL]
    d3, d4 = pd.Timestamp("2024-01-03"), pd.Timestamp("2024-01-04")
    assert series[d3] == pytest.approx(0.0001 + 0.0002 + 0.0003)   # only Jan-03's three
    assert series[d4] == pytest.approx(0.0007 + 0.0001)            # Jan-04's 00:00 counted here
    # total across days equals sum of every settlement exactly once (no leak/dup)
    assert sum(series.values()) == pytest.approx(0.0001 + 0.0002 + 0.0003 + 0.0007 + 0.0001)


# ---------------------------------------------------------------------------
# Lightweight stub stack to drive _process_symbol_candle_completion
# ---------------------------------------------------------------------------

class _FakeSignal:
    def __init__(self, forecast=0.0):
        self.forecast = forecast


class _FakeStrategy:
    def update(self, data):
        pass

    def generate_signals(self):
        return _FakeSignal(0.0)


class _NoRebalanceForecastManager:
    def forecast_to_allocation(self, forecast):
        return 0.0

    def calculate_allocation_change(self, target, previous):
        return 0.0   # never rebalance → isolate the funding accrual


class _AlwaysRebalanceForecastManager:
    def forecast_to_allocation(self, forecast):
        return 1.0

    def calculate_allocation_change(self, target, previous):
        return 1.0   # always enter the rebalance branch


class _ApproveAllRisk:
    def approve_allocation_change(self, symbol, allocation_change, data):
        return True, {}


class _FlipExec:
    """On rebalance, replace the held position with a fixed long (proves funding is
    charged on the PRE-trade held position, not the rebalanced-into one)."""
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def _execute_portfolio_rebalance(self, **kwargs):
        self.portfolio.local_balance[SYMBOL]["locked"] = 0.0
        self.portfolio.local_balance[SYMBOL]["free"] = 2.0
        return True, {}


class _FakeDataManager:
    def __init__(self):
        self.candle_builder = object()
        self._bar = None

    def set_bar(self, bar_df):
        self._bar = bar_df

    def get_data_history(self, symbol, count=1):
        return self._bar


class _CaptureTracker:
    def __init__(self):
        self.total_values = []

    def record_state(self, data=None, total_portfolio_value=None, **kwargs):
        self.total_values.append(total_portfolio_value)


class _SpyPortfolio(MockPortfolioInfo):
    """Records the net position quantity seen at each apply_funding call."""
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.funding_qty_seen = []

    def apply_funding(self, symbol, mark_price, f_bar):
        free = self.local_balance[symbol].get("free", 0.0)
        locked = self.local_balance[symbol].get("locked", 0.0)
        self.funding_qty_seen.append(free - locked)
        return super().apply_funding(symbol, mark_price, f_bar)


def _bar(ts, close):
    return pd.DataFrame({"timestamp": [pd.Timestamp(ts)], "close": [close]})


def _build_bot(portfolio, forecast_manager, tracker,
               data_manager, execution_handler=None, risk_manager=None):
    return TradingBot(
        data_manager=data_manager,
        strategy=_FakeStrategy(),
        execution_handler=execution_handler,
        logger=logging.getLogger("test_funding"),
        portfolio_info=portfolio,
        portfolio_state_tracker=tracker,
        forecast_manager=forecast_manager,
        risk_manager=risk_manager,
        performance_tracker=None,
        symbols=[SYMBOL],
    )


def _run_two_flat_bars(model_funding, funding_daily):
    """Held short across two flat-price bars; return the recorded bar-level
    total_portfolio_value series. USDT free 20,000; short 0.5 BTC @ 20,000
    (total = 20,000 - 10,000 = 10,000)."""
    portfolio = MockPortfolioInfo(initial_balance={
        "USDT": {"free": 20000.0, "locked": 0.0},
        SYMBOL: {"free": 0.0, "locked": 0.5},
    })
    tracker = _CaptureTracker()
    dm = _FakeDataManager()
    bot = _build_bot(portfolio, _NoRebalanceForecastManager(), tracker, dm)
    bot.model_funding = model_funding
    bot.funding_daily = funding_daily

    for ts in ("2024-01-01 00:00:00", "2024-01-02 00:00:00"):
        dm.set_bar(_bar(ts, 20000.0))
        bot._process_symbol_candle_completion(SYMBOL)
    return tracker.total_values


def test_flag_off_byte_identity_regardless_of_feed():
    """FLAG-OFF BYTE-IDENTITY: with model_funding=False the bar-level
    total_portfolio_value series is identical whether or not a funding feed is
    present — the default path is untouched by the new mechanism."""
    feed = {SYMBOL: {
        pd.Timestamp("2024-01-01"): 0.0003,
        pd.Timestamp("2024-01-02"): 0.0003,
    }}
    baseline_no_feed = _run_two_flat_bars(model_funding=False, funding_daily=None)
    off_with_feed = _run_two_flat_bars(model_funding=False, funding_daily=feed)

    assert baseline_no_feed == [10000.0, 10000.0]
    assert off_with_feed == baseline_no_feed   # feed presence makes no difference when off


def test_example8_bar_level_integration_short_earns_credit():
    """§5(d).8: a held short earns funding across flat-price bars; the recorded
    bar-level total_portfolio_value rises by exactly the credit each bar — confirming
    funding reaches the metrics series. Short 0.5 BTC @ 20,000, f_bar=+0.0003 →
    +3.00/bar credit."""
    feed = {SYMBOL: {
        pd.Timestamp("2024-01-01"): 0.0003,
        pd.Timestamp("2024-01-02"): 0.0003,
    }}
    on = _run_two_flat_bars(model_funding=True, funding_daily=feed)
    # credit per bar = -(-1) * (0.5*20000) * 0.0003 = +3.00, cumulative in USDT.free
    assert on == [pytest.approx(10003.0), pytest.approx(10006.0)]

    baseline = _run_two_flat_bars(model_funding=False, funding_daily=None)
    assert on[0] - baseline[0] == pytest.approx(3.00)
    assert on[1] - baseline[1] == pytest.approx(6.00)


def test_funding_charged_on_position_held_into_bar_not_rebalanced_into():
    """TIMING: funding is charged on the position HELD INTO the bar (the pre-rebalance
    balances), never the one the bar rebalances into. Bar 1 holds a short 0.5 then
    rebalances to long 2.0; bar 2 holds that long 2.0. apply_funding must see the
    held-into quantity each bar."""
    portfolio = _SpyPortfolio(initial_balance={
        "USDT": {"free": 20000.0, "locked": 0.0},
        SYMBOL: {"free": 0.0, "locked": 0.5},
    })
    tracker = _CaptureTracker()
    dm = _FakeDataManager()
    execn = _FlipExec(portfolio)
    bot = _build_bot(portfolio, _AlwaysRebalanceForecastManager(), tracker, dm,
                     execution_handler=execn, risk_manager=_ApproveAllRisk())
    bot.model_funding = True
    bot.funding_daily = {SYMBOL: {
        pd.Timestamp("2024-01-01"): 0.0003,
        pd.Timestamp("2024-01-02"): 0.0003,
    }}

    for ts in ("2024-01-01 00:00:00", "2024-01-02 00:00:00"):
        dm.set_bar(_bar(ts, 20000.0))
        bot._process_symbol_candle_completion(SYMBOL)

    # Bar 1: held short (net -0.5) into the bar, before the flip to +2.0.
    # Bar 2: held the +2.0 that bar 1 rebalanced INTO.
    assert portfolio.funding_qty_seen == [pytest.approx(-0.5), pytest.approx(2.0)]
