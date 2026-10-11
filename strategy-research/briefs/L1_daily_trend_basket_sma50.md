---
# Lane 1 of the 2026-10-10 strategic step-back (DECISION_LOG D-102). One of
# three runs pre-registered together: sma50, sma100 (BASE), sma200. They
# differ ONLY in lookback_L. Do not register before PR #381 (vol_target) is
# merged and master is merged into the operator's checkout.

strategy_domain: "time_series_trend"
market_universe: [BTCUSDT, ETHUSDT, TRXUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, LINKUSDT, LTCUSDT, UNIUSDT]
timeframe: "1d"
venue: "kraken"
product: "perp"
research_goal: >
  Lane 1, design run (shorter lookback): does slow daily time-series trend, sized by volatility
  targeting, on an equal-weight basket of 9 Kraken coins, earn more than its
  costs and beat staying flat on fold A (2022-2023)? Who pays: trend in crypto
  is attributed to slow-moving and constrained flows (retail herding, leverage
  liquidation cascades, scheduled rebalancers); a daily signal trades a few
  dozen times per coin over two years, against 1,568 to 2,471 trades per
  4-month window in the 1h runs 070-079, where fees were 61-76% of the loss.
  Why not arbitraged: trend is a premium for bearing crash and whipsaw risk;
  its size after costs at daily frequency is what this run measures.
constraints:
  - "The strategy config is exactly this, nothing added: regime_detector ungated (mode threshold_rules, no components, no rules, no vetoes, default_regime unknown); strategies.regimes.unknown has ONE component, strategies.strategy_components.SmaTrendLongOnlyComponent with params lookback_L 50 (scaling_factor default 10), weight 1.0, transforms in this order: identity; vol_target with params window 60, target_annual_vol 0.4, periods_per_year 365; clip with params min 0, max 10. trending, mean_reversion and chop are null. No history_transforms, no lookback override, no min_allocation_change override."
  - "Long or flat only, never short. Allocation = forecast / 10, so at most 100% of the coin's account (no leverage: the engine has no liquidation, D-101)."
  - "Sizing moves only in steps of at least 0.2 of allocation: the risk control min_allocation_change (threshold 0.2, trading-bot/config.json:28) rejects smaller rebalances."
  - "Variants: the base only. With the variant loop off for this run, only the base config is backtested; any design or asset entry stage 3 writes is listed untested and gets no trial. The other two lookbacks are the separate runs `L1_daily_trend_basket_sma100`, `L1_daily_trend_basket_sma200`."
  - "The 100-trades-per-coin bar (trade_count_min) is expected to FAIL by construction for a daily signal; this is known before the run and is not a reason to change anything."
  - "No parameter is tuned on fold A. Lookback, vol window, vol target and clip are fixed here."
available_data:
  - "Kraken 1d OHLCV caches trading-bot/local_data/kraken_<COIN>USD_1d.csv for the 9 coins: every fold-A window-edge day present; no missing day in fold A except XRP 2022-05-11/12 (2 days, inside the engine's 3-bar ignore tier); at least 402 daily bars before 2022-01-01 for every coin (warm-up prefetch 2 x required_bars; required_bars 61 / 101 / 201 for lookback 50 / 100 / 200)."

criteria_from: hypothesis_generation

machine_constraints:
  protocol:
    symbols: [BTCUSDT, ETHUSDT, TRXUSDT, XRPUSDT, ADAUSDT, DOGEUSDT, LINKUSDT, LTCUSDT, UNIUSDT]
    timeframe: "1d"
    start: "2022-01-01"
    end: "2023-12-31"
    window_months: 4
---

# Lane 1 -- daily SMA(50) trend, vol-targeted, 9-coin Kraken basket, fold A (design run (shorter lookback))

Pre-registered 2026-10-11 in DECISION_LOG D-102, before any run. The rule below
is the same text in all three briefs and in D-102; it is read by hand after the
three runs, never re-thresholded.

## Continue rule (pre-registered)

Inputs, per run:

- **Sharpe:** `artifacts/profit_bars_evaluation.yaml`, row `sharpe_min`, its
  `actual`: the equal-weight portfolio's chained daily returns, mean / sample
  stdev x sqrt(365), rf 0 (`tools/portfolio_whole_test.py` `whole_test_sharpe`),
  after fees and slippage (funding is not modelled). Flat = 0.
- **Base ratio (sma100 run only):**
  `tools/portfolio_whole_test.pooled_edge_to_cost_ratio(trades, 30, all_costs=True)["ratio"]`
  over the `trades` list of the run's `trade_diagnostics.json` (run folder):
  min(ratio over all trades, ratio without window-end forced closes), gross edge
  before costs / fees + slippage; NOT EVALUABLE when it raises
  `PortfolioNotEvaluable` (fewer than 30 non-forced trades, or a trade without
  all-cost fields).

**CONTINUE** iff Sharpe > 0 on at least 2 of the 3 runs AND the base ratio is
>= 1 or not evaluable. Next: lane 1's fold-B confirmation.

**FAIL, cost binds:** the base ratio is < 1 on >= 30 trades. Next: cost
engineering (an off-by-default rebalance band or minimum hold).

**FAIL, the signal does not carry:** the Sharpe condition fails and the base
ratio is >= 1 or not evaluable. Next: the lane order (funding carry after
E-053), not cost engineering.

Reported, never decided on: trade counts per run, the forced-close count, the
fees-only ratio beside the all-costs one, buy-and-hold excess.

## Predictions (two-phase: a measured count far from these is a bug to explain)

SMA crossings counted on the cached Kraken daily closes 2022-01-01 to
2023-12-31 only (bounded reads; no later bar used; no result computed), long/flat
with the component's one-bar lag, flat at each 4-month window's start:
this run (lookback 50) about **224 completed
trades ending by signal** and **16 window-end forced closes**, pooled over
the 9 coins (continuous count without windows: 226). Expected divergence
declared now: vol targeting also rebalances inside a trend whenever the size
moves by 0.2 or more, and the engine matches fills lot by lot (LIFO,
`performance/metrics.py`), so the measured completed-trade count is expected
ABOVE the crossing count; a count BELOW it is a bug.

## Known biases and limits

- **Survivorship:** every coin still trades on Kraken in 2025; coins that
  collapsed in or before fold A (for example LUNA in 2022) have no cache.
- **Prior look:** run_054 tested SMA(100) daily long-only on Binance BTC and
  ETH, 15 six-month windows 2018-04 to 2025-09, which include fold A. For BTC
  and ETH this is not fresh evidence; the other 7 coins and the vol targeting are.
- **Funding not modelled:** perp costs (Kraken futures fee 5 bps per side;
  slippage BTC 2.5, ETH 4, other coins 7.5 bps per side,
  `trading-bot/config/cost_model.json`) on Kraken spot prices (D-057). A long
  perp usually pays funding in rising markets, so results are flattered.
- **Window restarts:** each coin is backtested alone per 4-month window, forced
  flat at its end; indicators are warmed up before each window (warmup_prefetch).
- **Execution:** fills at the signal bar's close with a one-bar lag, not
  next-day open (SmaTrendLongOnlyComponent docstring).
- **Run setup (operator's checkout):** variant_loop off, composition_runs off,
  analyst off, cost_bar_all_costs on, folds on. With the loop off, a
  data-gate "refine" pauses the whole run.
