"""
Aux-feed causality canary (dispatch W8 step 3).

WHY A CANARY INSTEAD OF JUST THE STATIC AUDIT
----------------------------------------------
The static read of data_manager.py / whale_features.py (SESSION_LOG 2026-07-27)
found: a bar timestamped T covers the FORWARD window [T, T+1) and is delivered
to the strategy only once a later tick confirms T+1 has begun
(CandleBuilder, data_manager.py:236-276); the whale fetcher assigns bar T's
features from exactly that same window, bounded so the aggregation loop never
reads past `bar_end` (whale_features.py:419-422); `merge_asof(direction=
'backward')` then attaches bar T's OWN value to bar T (data_manager.py:
547-552, 642-647). Conclusion: today's whale feature has no lookahead, PROVIDED
every fetcher individually respects its own window boundary. An argument is
not a proof of what the *pipeline* would do if that provision were ever
violated — this test empirically probes exactly that, through the REAL merge
code and the REAL strategy/execution/portfolio path
(TradingBot._process_symbol_candle_completion -> ForecastManager ->
RiskManager -> MockExecutionHandler -> MockPortfolioInfo).

THE TWO FIXTURES, AND A FINDING THAT UPGRADES THE AUDIT'S CONCLUSION
---------------------------------------------------------------------
`own_ret[T] = (close[T] - close[T-1]) / close[T-1]` is bar T's OWN
already-realized return — exactly analogous to what a correctly-bounded
fetcher computes from window T's own data, timestamped T. A maximally
aggressive strategy trading on its sign shows ~zero edge below, because in an
i.i.d. synthetic price path bar T's own past return has no bearing on bar
(T+1)'s independent draw. This is the HONEST case and it passes.

`fwd_ret[T] = (close[T+1] - close[T]) / close[T]` — literally "a perfect copy
of that bar's NEXT return" per the W8 dispatch's instruction — is NOT
computable by any fetcher bounded to window T's own data (it needs
close[T+1], which does not exist until bar T+1 itself completes). Attaching
it at row T and running it through the real pipeline is dramatically,
unmistakably profitable (~15x over 119 bars in the fixture below, vs. a noise
band under 2x for the honest case) — proving the merge/execution path applies
NO independent safeguard against a mistimed feed. Causality currently rests
ENTIRELY on each fetcher individually respecting its own window boundary
(true today for the whale fetcher, verified separately by inspection and by
`tests/test_whale_footprint_fetcher.py`); nothing in `data_manager.py`'s
shared merge path or in `TradingBot._process_symbol_candle_completion` would
catch a future fetcher that got this wrong.

**This is a STOP-level finding by the dispatch's own criterion ("If it can
[profit], there is lookahead — report it as a STOP-level finding"), but the
leak location is NOT the whale fetcher (independently audited as correctly
bounded) — it is the absence of any defense-in-depth in the SHARED merge
path.** Per the same dispatch's constraint ("Do NOT restructure the shared
merge path in this commit; if the leak is in shared code, STOP and report"),
no fix is attempted here. See SESSION_LOG.md 2026-07-27 and the W8 final
report.

Keep this test whenever a new feed is added to FEED_REGISTRY /
RESERVED_FEED_REGISTRY: swap in that feed's real fetcher output shape and
re-run both fixtures.
"""
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from data.data_manager import DataManager  # noqa: E402
from strategies.strategy_base import MainStrategy, StrategyOutput  # noqa: E402
from execution.execution_handler import MockExecutionHandler  # noqa: E402
from execution.portfolio_info import MockPortfolioInfo  # noqa: E402
from execution.forecast_manager import ForecastManager  # noqa: E402
from risk.risk_manager import RiskManager  # noqa: E402
from core.trading_bot import TradingBot  # noqa: E402

SYMBOL = "BTCUSDT"
N_BARS = 120
SIGMA = 0.015  # per-bar synthetic volatility
SEED = 20260727


class _CanaryFetcher:
    """Matches the `feed.fetcher.get_data(symbol)` contract DataManager expects
    (data_manager.py:604) — the minimal real interface, not a reimplementation
    of BaseFetcher."""

    def __init__(self, feed_df: pd.DataFrame):
        self._df = feed_df

    def get_data(self, symbol=None):
        return self._df


class _NullTracker:
    def record_state(self, **kwargs):
        pass


class _CanaryStrategy(MainStrategy):
    """Maximally aggressive: full +-200% allocation on the sign of the aux
    column alone. Worst-case sensitivity -- if ANY future information reaches
    this column early, this strategy extracts the maximum possible edge from
    it, which is the point of a canary."""

    def __init__(self, column: str):
        self.column = column
        self._data = None

    def update(self, data: pd.DataFrame):
        self._data = data

    def is_ready(self) -> bool:
        return True

    def get_required_periods(self) -> int:
        return 1

    def generate_forecast(self):
        val = self._data[self.column].iloc[-1]
        if pd.isna(val):
            forecast = 0.0
        else:
            forecast = 20.0 if val > 0 else (-20.0 if val < 0 else 0.0)
        return forecast, None, {"canary_value": val}

    def generate_signals(self) -> StrategyOutput:
        forecast, _active, debug = self.generate_forecast()
        return StrategyOutput(
            forecast=forecast, confidence=1.0, regime="CANARY",
            strategy=None, debug_info=debug,
        )


def _price_series(n=N_BARS, sigma=SIGMA, seed=SEED) -> pd.DataFrame:
    rng = np.random.RandomState(seed)
    log_rets = rng.normal(loc=0.0, scale=sigma, size=n)
    close = 100.0 * np.exp(np.cumsum(log_rets))
    ts = pd.date_range("2024-01-01", periods=n, freq="h")
    return pd.DataFrame({
        "timestamp": ts, "open": close, "high": close, "low": close,
        "close": close, "volume": 1.0,
    })


def _own_returns(price_df: pd.DataFrame) -> pd.Series:
    """own_ret[T] = (close[T] - close[T-1]) / close[T-1] -- bar T's OWN
    already-realized return, known once bar T is delivered. First bar is NaN
    (no prior bar)."""
    close = price_df["close"]
    return (close - close.shift(1)) / close.shift(1)


def _next_returns(price_df: pd.DataFrame) -> pd.Series:
    """fwd_ret[T] = (close[T+1] - close[T]) / close[T] -- "that bar's NEXT
    return" per the W8 dispatch's canary instruction. Requires close[T+1],
    which does not exist at bar T's delivery time; no correctly-bounded
    fetcher can compute this. Last bar is NaN (no bar T+1 exists)."""
    close = price_df["close"]
    return (close.shift(-1) - close) / close


def _run_canary(price_df: pd.DataFrame, canary_values: pd.Series) -> float:
    """Registers `canary_values` (indexed like price_df, aligned to
    price_df['timestamp']) as an aux feed through the REAL DataManager merge,
    drives TradingBot._process_symbol_candle_completion bar-by-bar through the
    REAL forecast/risk/execution/portfolio path, and returns the total return
    (final / initial - 1) over the run."""
    feed_df = pd.DataFrame({
        "timestamp": price_df["timestamp"], "canary": canary_values.values,
    }).dropna(subset=["canary"])

    dm = DataManager(symbols=[SYMBOL], interval_seconds=3600, mode="backtest")
    dm.register_feed("canary", _CanaryFetcher(feed_df), agg="last")
    # REAL merge_asof code path (data_manager.py:642-647), not a stand-in.
    dm._premerge_aux_feeds(SYMBOL, price_df[["timestamp", "close"]].copy())

    # Only the candle-DELIVERY mechanism is stubbed (CandleBuilder's own
    # forward-window/completion-timing convention is audited separately in
    # SESSION_LOG 2026-07-27 and is not what this canary targets). The merge
    # that attaches the aux column (`_attach_aux_columns`, data_manager.py:
    # 547-552) is the real DataManager method, called unmodified below.
    state = {"t": 0}

    def _get_candle_history(symbol, count=1):
        row = price_df.iloc[[state["t"]]]
        return row

    dm.candle_builder = SimpleNamespace(get_candle_history=_get_candle_history)

    portfolio = MockPortfolioInfo(
        initial_balance={
            "USDT": {"free": 100_000.0, "locked": 0.0},
            SYMBOL: {"free": 0.0, "locked": 0.0},
        },
        commission_rate=0.0,  # isolate causality from cost modelling
    )
    execn = MockExecutionHandler(portfolio_info=portfolio)
    bot = TradingBot(
        data_manager=dm,
        strategy=_CanaryStrategy("canary"),
        execution_handler=execn,
        portfolio_info=portfolio,
        portfolio_state_tracker=_NullTracker(),
        forecast_manager=ForecastManager(),
        risk_manager=RiskManager({}),  # no controls configured -> always approves
        symbols=[SYMBOL],
    )

    initial_value = 100_000.0
    # Only rows with a defined canary value are usable; iterate the matching
    # integer positions in price_df so index alignment survives the dropna.
    usable_positions = feed_df.index.tolist()
    for t in usable_positions:
        state["t"] = t
        bot._process_symbol_candle_completion(SYMBOL)

    balances = portfolio.get_account_balance()
    final_close = price_df["close"].iloc[usable_positions[-1]]
    final_value = portfolio._calculate_total_portfolio_value(balances, final_close)
    return final_value / initial_value - 1.0


# ---------------------------------------------------------------------------


def test_own_realized_return_feature_shows_no_exploitable_edge():
    """HONEST case: canary[T] = bar T's OWN already-realized return -- exactly
    analogous to a correctly-bounded fetcher (like the real whale fetcher).
    Total return must stay in a noise band, nowhere near the dramatic blowup
    of the next-bar-return fixture below."""
    price_df = _price_series()
    own = _own_returns(price_df)
    total_return = _run_canary(price_df, own)
    assert abs(total_return) < 2.0, (
        f"own-realized-return canary produced total_return={total_return!r}, "
        "outside random-walk noise for a correctly-bounded feature — "
        "investigate before trusting the merge."
    )


def test_next_bar_return_feature_is_dramatically_profitable_no_pipeline_safeguard():
    """STOP-LEVEL FINDING (see module docstring): canary[T] = bar T's NEXT
    return, literally "a perfect copy of that bar's NEXT return" per the W8
    dispatch instruction. No correctly-bounded fetcher can compute this at
    bar T's delivery time. This test PASSING (i.e. dramatic profit) is not a
    bug in this test — it demonstrates that the shared merge/execution path
    provides no independent defense against a mistimed feed; causality
    depends entirely on each fetcher's own window discipline. Today's real
    whale fetcher IS correctly bounded (separately audited and unit-tested),
    so this is a defense-in-depth gap in shared code, not a live leak — per
    dispatch instructions, not fixed here (shared-code fix requires its own
    dispatch)."""
    price_df = _price_series()
    nxt = _next_returns(price_df)
    total_return = _run_canary(price_df, nxt)
    assert total_return > 5.0, (
        f"next-bar-return canary only produced total_return={total_return!r}; "
        "expected dramatic profit confirming the pipeline has no independent "
        "timing safeguard — if this now fails, re-examine whether something "
        "changed in the merge/execution path (which would be good news, but "
        "unexpected) before assuming the canary itself regressed."
    )


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
