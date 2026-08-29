"""
Aux-feed causality canary (dispatch W8 step 3; guard added dispatch W9 step 3).

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

WHAT W8 FOUND, AND WHAT W9 FIXED
----------------------------------
`own_ret[T] = (close[T] - close[T-1]) / close[T-1]` is bar T's OWN
already-realized return — exactly analogous to what a correctly-bounded
fetcher computes from window T's own data, timestamped T. A maximally
aggressive strategy trading on its sign shows ~zero edge below, because in an
i.i.d. synthetic price path bar T's own past return has no bearing on bar
(T+1)'s independent draw. This is the HONEST case; it passes, declaring its
true window (`window_seconds=interval_seconds` — the value is only final once
bar T's own close is known, i.e. at bar T's own end).

`fwd_ret[T] = (close[T+1] - close[T]) / close[T]` — literally "a perfect copy
of that bar's NEXT return" per the W8 dispatch's instruction — is NOT
computable by any fetcher bounded to window T's own data (it needs
close[T+1], which does not exist until bar T+1 itself completes: its TRUE
declared window is `2 * interval_seconds`, ending at bar T+1's own close).
W8 found that attaching it at row T through the real pipeline was
dramatically, unmistakably profitable (~15x over 119 bars), proving the
merge/execution path applied NO independent safeguard against a mistimed
feed — filed as a STOP-level finding, not fixed at the time (shared-code
change, out of that dispatch's scope).

W9 added exactly that defense: `DataManager.register_feed()` now REQUIRES a
`window_seconds` declaration, and `_merge_asof_with_causality_guard`
(data_manager.py) refuses — raises `AuxFeedCausalityError` — to attach any
value whose declared window ends after the bar it would be merged onto. The
guard TRUSTS the declaration; it does not re-derive it from how the value was
actually computed. So the honest fwd_ret feed (correctly declaring
`window_seconds=2*interval_seconds`) is now REJECTED at merge time, below —
this is the defense-in-depth W8 found missing. What the guard still cannot
catch — a feed that lies about its own window (declares 0 while internally
depending on future data) — is exactly the residual trust boundary documented
in `AuxFeedCausalityError`'s docstring and `data/ADDING_A_FEED.md`; causality
for THAT case still rests on the fetcher's own correctness (true today for
the whale fetcher, verified separately by `tests/test_whale_footprint_fetcher.py`).

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

from data.data_manager import AuxFeedCausalityError, DataManager  # noqa: E402
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
            forecast=forecast,
            confidence=1.0,
            regime="CANARY",
            strategy=None,
            debug_info=debug,
        )


def _price_series(n=N_BARS, sigma=SIGMA, seed=SEED) -> pd.DataFrame:
    rng = np.random.RandomState(seed)
    log_rets = rng.normal(loc=0.0, scale=sigma, size=n)
    close = 100.0 * np.exp(np.cumsum(log_rets))
    ts = pd.date_range("2024-01-01", periods=n, freq="h")
    return pd.DataFrame(
        {
            "timestamp": ts,
            "open": close,
            "high": close,
            "low": close,
            "close": close,
            "volume": 1.0,
        }
    )


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


def _run_canary(
    price_df: pd.DataFrame, canary_values: pd.Series, window_seconds: float
) -> float:
    """Registers `canary_values` (indexed like price_df, aligned to
    price_df['timestamp']) as an aux feed declaring `window_seconds`, through
    the REAL DataManager merge (raises AuxFeedCausalityError there if the
    declared window violates causality — the caller decides whether that's
    expected), drives TradingBot._process_symbol_candle_completion bar-by-bar
    through the REAL forecast/risk/execution/portfolio path, and returns the
    total return (final / initial - 1) over the run."""
    feed_df = pd.DataFrame(
        {
            "timestamp": price_df["timestamp"],
            "canary": canary_values.values,
        }
    ).dropna(subset=["canary"])

    dm = DataManager(symbols=[SYMBOL], interval_seconds=3600, mode="backtest")
    dm.register_feed(
        "canary", _CanaryFetcher(feed_df), window_seconds=window_seconds, agg="last"
    )
    # REAL merge_asof + causality-guard code path (data_manager.py's
    # _premerge_aux_feeds / _merge_asof_with_causality_guard), not a stand-in.
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


INTERVAL_SECONDS = 3600  # matches _run_canary's DataManager(interval_seconds=3600)


def test_own_realized_return_feature_shows_no_exploitable_edge():
    """HONEST case: canary[T] = bar T's OWN already-realized return -- exactly
    analogous to a correctly-bounded fetcher (like the real whale fetcher).
    Declares its true window (ends at bar T's own close, i.e.
    window_seconds=interval_seconds — the same convention whale features use
    on their own grid), so the guard passes it through. Total return must
    stay in a noise band, nowhere near the dramatic blowup the dishonestly-
    timed fixture below would produce if the guard let it through."""
    price_df = _price_series()
    own = _own_returns(price_df)
    total_return = _run_canary(price_df, own, window_seconds=INTERVAL_SECONDS)
    assert abs(total_return) < 2.0, (
        f"own-realized-return canary produced total_return={total_return!r}, "
        "outside random-walk noise for a correctly-bounded feature — "
        "investigate before trusting the merge."
    )


def test_next_bar_return_feature_is_rejected_by_causality_guard():
    """THE GUARD CATCHES THE LEAKING CANARY (dispatch W9 step 3; see module
    docstring for the W8 finding this fixes). canary[T] = bar T's NEXT
    return, literally "a perfect copy of that bar's NEXT return" per the W8
    dispatch instruction — not computable by any fetcher bounded to window
    T's own data; its TRUE window ends at bar T+1's own close, i.e.
    window_seconds=2*interval_seconds. Declaring that honestly must now make
    `_premerge_aux_feeds` REFUSE to attach it, before the simulation loop
    (and any profit) ever runs — this is the defense-in-depth W8 found
    missing. Today's real whale fetcher never needs to declare a window this
    large (separately audited and unit-tested), so this is exercising the
    guard's rejection path, not a live feed."""
    price_df = _price_series()
    nxt = _next_returns(price_df)
    with pytest.raises(AuxFeedCausalityError, match="ends after bar"):
        _run_canary(price_df, nxt, window_seconds=2 * INTERVAL_SECONDS)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
