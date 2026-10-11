---
# Lane 1 v2 (DECISION_LOG D-105, which supersedes D-102's setup). One of three
# runs pre-registered together: sma50_v2, sma100_v2 (BASE), sma200_v2. They
# differ ONLY in `period`. Register only after master (with the deviation gate,
# D-104) is merged into the operator's checkout and orchestrator.deviation_gate
# is on.

strategy_domain: "time_series_trend"
market_universe: [BTCUSDT, ETHUSDT, TRXUSDT, ADAUSDT, DOGEUSDT, LINKUSDT, LTCUSDT, UNIUSDT]
timeframe: "1d"
venue: "kraken"
product: "perp"
research_goal: >
  Lane 1 v2, BASE run: does slow daily time-series trend, sized by volatility
  targeting, on an equal-weight basket of 8 Kraken coins, earn more than its
  costs and beat staying flat on fold A (2022-2023)? Who pays: trend in crypto
  is attributed to slow-moving and constrained flows (retail herding, leverage
  liquidation cascades, scheduled rebalancers); a daily signal trades a few
  dozen times per coin over two years, against 1,568 to 2,471 trades per
  4-month window in the 1h runs 070-079, where fees were 61-76% of the loss
  (measured 2026-10-10 from runs/run_0NN/variants/base/trade_diagnostics.json in
  the operator's checkout; SESSION_LOG.md, 2026-10-10 step-back entry).
  Why not arbitraged: trend is a premium for bearing crash and whipsaw risk;
  its size after costs at daily frequency is what this run measures.
constraints:
  - |
    Build EXACTLY this strategy config (JSON), nothing added, nothing renamed, no `warmup` key (scaffolding is `/regime_detector` only); the deviation gate pauses the run on any deviation:
    {"regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"}, "strategies": {"regimes": {"unknown": {"components": [{"id": "trend", "class": "strategies.strategy_components.MovingAverageDistanceComponent", "params": {"period": 100, "average": "sma"}, "weight": 1.0, "transforms": [{"op": "scale", "params": {"factor": 5}}, {"op": "clip", "params": {"min": 0, "max": 10}}, {"op": "vol_target", "params": {"window": 60, "target_annual_vol": 0.4, "periods_per_year": 365}}, {"op": "clip", "params": {"min": 0, "max": 10}}]}]}, "trending": null, "mean_reversion": null, "chop": null}}}
  - "In words: the percent distance of the close from its 100-day simple moving average, times 5, limited to 0..10 (flat at or below the average, partial size up to 2% above it, full size beyond); then volatility targeting to 40% a year over 60 daily returns (periods_per_year 365); then limited to 0..10 again, so the forecast is at most 10, so allocation at most 1.0. Long or flat only, never short."
  - "Information for reading turnover, not a sizing rule of this config: the risk control min_allocation_change (threshold 0.2, trading-bot/config.json:28; no exemption for a close) rejects any rebalance smaller than 0.2 of allocation, so a target under 0.2 is never opened and a holding under 0.2 closes only at the window end."
  - "Variants: the base only. With the variant loop off for this run, only the base config is backtested; any design or asset entry in variant_patches.yaml is listed untested and gets no trial. The other two lookbacks are the separate runs `L1_daily_trend_basket_sma50_v2`, `L1_daily_trend_basket_sma200_v2`."
  - "The 100-trades-per-coin bar (trade_count_min) is expected to FAIL by construction for a daily signal; this is known before the run and is not a reason to change anything."
  - "No parameter is tuned on fold A. Lookback, the 2% full-size distance (scale 5), vol window, vol target and both clips are fixed here."
available_data:
  - "Kraken 1d OHLCV caches trading-bot/local_data/kraken_<COIN>USD_1d.csv for the 8 coins: no missing day from 2022-01-01 to 2023-12-31, every fold-A window-edge day present; at least 443 daily bars before 2022-01-01 for every coin (UNI is the shortest). The launcher's warm-up prefetch (2 x required_bars 100 = 200 days before each window, core/launcher.py) holds all 200 daily rows for every coin and window, and the strategy is ready by its end (first ready at bar 199; replayed for 8 coins x 6 windows). XRP was dropped (D-105): its 2022-05-11/12 gap left 2 rows missing in some sma100/sma200 prefetch spans, which would stop those windows at the launcher's readiness check."

criteria_from: hypothesis_generation

machine_constraints:
  protocol:
    symbols: [BTCUSDT, ETHUSDT, TRXUSDT, ADAUSDT, DOGEUSDT, LINKUSDT, LTCUSDT, UNIUSDT]
    timeframe: "1d"
    start: "2022-01-01"
    end: "2023-12-31"
    window_months: 4
---

# Lane 1 v2 -- daily trend on the distance from SMA(100), vol-targeted, 8-coin Kraken basket, fold A (BASE run)

Pre-registered 2026-10-11 in DECISION_LOG D-105 (superseding D-102's setup), before
any run of this signal. The continue rule below is word for word the one D-102
pre-registered; it is read by hand after the three runs, never re-thresholded.
Read "the sma100 run" as `L1_daily_trend_basket_sma100_v2`.

## The config (the engine's exact shape)

```json
{
  "regime_detector": {
    "mode": "threshold_rules",
    "components": [],
    "rules": [],
    "default_regime": "unknown"
  },
  "strategies": {
    "regimes": {
      "unknown": {
        "components": [
          {
            "id": "trend",
            "class": "strategies.strategy_components.MovingAverageDistanceComponent",
            "params": {
              "period": 100,
              "average": "sma"
            },
            "weight": 1.0,
            "transforms": [
              {
                "op": "scale",
                "params": {
                  "factor": 5
                }
              },
              {
                "op": "clip",
                "params": {
                  "min": 0,
                  "max": 10
                }
              },
              {
                "op": "vol_target",
                "params": {
                  "window": 60,
                  "target_annual_vol": 0.4,
                  "periods_per_year": 365
                }
              },
              {
                "op": "clip",
                "params": {
                  "min": 0,
                  "max": 10
                }
              }
            ]
          }
        ]
      },
      "trending": null,
      "mean_reversion": null,
      "chop": null
    }
  }
}
```

Proved before this brief was committed: `tools/validate_config.py` returns no
violation and the D-051 check none, for each of the three lookbacks; on synthetic
daily data the forecast equals the formula on every ready bar, 0 errors.

## Declared differences from the first pre-registration (D-102)

1. **Graded size near the average.** D-102's signal was full size as soon as the
   close was above the SMA. D-051 forbids an on/off forecast source, so v2 gives
   partial size within 2% above the SMA (linear from 0 at the average to full
   size at +2%) and the same full, vol-targeted size beyond. The 2% is fixed.
2. **The current close.** D-102's component decided on the prior bar's close
   (a one-bar lag); v2 decides on the current bar's close and the engine fills at
   that close, as it does for every strategy. No data after the bar's close is used.

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
  `PortfolioNotEvaluable` (fewer than 30 non-forced trades, a trade without
  all-cost fields, or a zero mean cost). A malformed record raises a plain
  `ValueError`: the run is broken; report it, do not judge the rule on it.

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

Distance-from-SMA sign changes counted on the cached Kraken daily closes
2022-01-01 to 2023-12-31 only (bounded reads; no later bar used; no result
computed), current-close timing, flat at each 4-month window's start, pooled
over the 8 coins: this run (lookback 100) about **138 exits by signal** and
**14 window-end forced closes**; 244 of 5,840 coin-days sit in the
partial-size zone (0-2% above the average). Expected divergence declared now:
the measured completed-trade count includes vol-target and partial-size
rebalances (lots matched LIFO, `performance/metrics.py`), so it is expected
ABOVE the exit count; entries and exits the 0.2 band blocks lower it. A count
well BELOW the exit count is a bug unless explained by blocked entries or exits,
counted from the run's own bars.

## Known biases and limits

- **Survivorship:** every coin still trades on Kraken in 2025; coins that
  collapsed in or before fold A (for example LUNA in 2022) have no cache.
- **Prior look:** run_054 tested SMA(100) daily long-only on Binance BTC and
  ETH, 15 six-month windows 2018-04 to 2025-09, which include fold A. For BTC
  and ETH this is not fresh evidence; the other 6 coins and the vol targeting are.
- **Funding not modelled:** perp costs (Kraken futures fee 5 bps per side;
  slippage BTC 2.5, ETH 4, other coins 7.5 bps per side,
  `trading-bot/config/cost_model.json`) on Kraken spot prices (D-057). A long
  perp usually pays funding in rising markets, so results are flattered.
- **Window restarts:** each coin is backtested alone per 4-month window, forced
  flat at its end; indicators are warmed up before each window (warmup_prefetch).
- **Execution:** decides on the current bar's close and fills at that close, no lag
  (MovingAverageDistanceComponent docstring; declared difference 2 above), not next-day open.
- **Run setup (operator's checkout):** variant_loop off, composition_runs off,
  analyst off, cost_bar_all_costs on, folds on. With the loop off, a
  data-gate "refine" pauses the whole run.
- **Run flag set (operator's checkout):** add `deviation_gate` on (it requires
  `nearest_build`, already on) to the D-102 set.
