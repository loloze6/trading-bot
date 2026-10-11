---
# Lane 1 v3 (DECISION_LOG D-107, D-108): fold B, the same three configs as v2
# (D-105). One of three runs pre-registered together: sma50_v3, sma100_v3
# (BASE), sma200_v3. They differ ONLY in `period`. Register only after this
# brief's PR is merged and master is merged into the operator's checkout.

strategy_domain: "time_series_trend"
market_universe: [BTCUSDT, ETHUSDT, LTCUSDT]
timeframe: "1d"
venue: "kraken"
product: "perp"
research_goal: >
  Lane 1 v3, BASE run: does the v2 daily trend signal (distance from SMA(100),
  vol-targeted, long or flat) earn more than its costs on unseen data, fold B
  (six 4-month blocks of 2018-2021), on an equal-weight basket of 3 Kraken
  coins? Fold A (2022-2023, runs 081-083) FAILED its pre-registered rule; the
  failure's label "cost binds" was an artefact of the lot-based ratio, and at
  position size costs were 13-26% of gross (D-107). Who pays: trend in crypto is
  attributed to slow-moving and constrained flows (retail herding, leverage
  liquidation cascades, scheduled rebalancers). Why not arbitraged: trend is a
  premium for bearing crash and whipsaw risk; whether it shows on bars this
  signal has never been run on is what this run measures.
constraints:
  - |
    Build EXACTLY this strategy config (JSON), nothing added, nothing renamed, no `warmup` key (scaffolding is `/regime_detector` only); the deviation gate pauses the run on any deviation:
    {"regime_detector": {"mode": "threshold_rules", "components": [], "rules": [], "default_regime": "unknown"}, "strategies": {"regimes": {"unknown": {"components": [{"id": "trend", "class": "strategies.strategy_components.MovingAverageDistanceComponent", "params": {"period": 100, "average": "sma"}, "weight": 1.0, "transforms": [{"op": "scale", "params": {"factor": 5}}, {"op": "clip", "params": {"min": 0, "max": 10}}, {"op": "vol_target", "params": {"window": 60, "target_annual_vol": 0.4, "periods_per_year": 365}}, {"op": "clip", "params": {"min": 0, "max": 10}}]}]}, "trending": null, "mean_reversion": null, "chop": null}}}
  - "In words: the percent distance of the close from its 100-day simple moving average, times 5, limited to 0..10 (flat at or below the average, partial size up to 2% above it, full size beyond); then volatility targeting to 40% a year over 60 daily returns (periods_per_year 365); then limited to 0..10 again, so the forecast is at most 10, so allocation at most 1.0. Long or flat only, never short. Identical to v2 (D-105) except the coins and the fold."
  - "Information for reading turnover, not a sizing rule of this config: the risk control min_allocation_change (threshold 0.2, trading-bot/config.json:28; no exemption for a close) rejects any rebalance smaller than 0.2 of allocation, so a target under 0.2 is never opened and a holding under 0.2 closes only at the window end."
  - "Variants: the base only. With the variant loop off for this run, only the base config is backtested; any design or asset entry in variant_patches.yaml is listed untested and gets no trial. The other two lookbacks are the separate runs `L1_daily_trend_basket_sma50_v3`, `L1_daily_trend_basket_sma200_v3`."
  - "The 100-trades-per-coin bar (trade_count_min) and the lot-based cost bar (cost_edge_ratio_min) are expected to FAIL by construction for a daily signal (D-107); this is known before the run and is not a reason to change anything."
  - "No parameter is tuned. Lookback, the 2% full-size distance (scale 5), vol window, vol target and both clips are v2's, unchanged after fold A."
available_data:
  - "Kraken 1d OHLCV caches trading-bot/local_data/kraken_<COIN>USD_1d.csv for BTC, ETH, LTC (first rows 2013-10-06, 2015-08-07, 2013-10-24). The data-availability gate's own check (tools/data_availability_gate.py check_price_window) grades all six fold-B windows `validate` for each coin. Warm-up: the launcher fetches 2 x required_bars days before each window (core/launcher.py:948-952; 400 days for sma200, so from 2017-03-27 for the 2018-05 window) and asserts readiness (core/launcher.py:1012-1025); replayed for 3 coins x 6 windows x 3 lookbacks, the strategy is ready at every window start. One day, 2018-01-12 (Kraken's outage), is missing for ETH and LTC: the 2018-05 prefetch spans hold 121/122, 199/200 and 399/400 rows and the 2019-01 sma200 span 399/400; one missing bar is in the engine's ignore tier (core/launcher.py:602, ignore_max_bars 3). BTC has no missing day."

criteria_from: hypothesis_generation

machine_constraints:
  protocol:
    symbols: [BTCUSDT, ETHUSDT, LTCUSDT]
    timeframe: "1d"
    fold: "B"
    start: "2018-05-01"
    end: "2021-12-31"
    window_months: 4
---

# Lane 1 v3 -- daily trend on the distance from SMA(100), vol-targeted, 3-coin Kraken basket, fold B (BASE run)

Pre-registered 2026-10-12 in DECISION_LOG D-108, before any run of this signal on
fold B, following the advisor ruling D-107 (fold A FAIL stands; go to fold B with
the same three configs). The continue rule below is read by hand after the three
runs, never re-thresholded. Read "the sma100 run" as `L1_daily_trend_basket_sma100_v3`.

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

Byte-identical to v2's config for the same lookback (D-105). Validity of the
run's authored config: the forecast replay (D-106,
`engineering/lane1_replay/replay_config.py <this brief> <run>/artifacts/backtest_spec.yaml`)
after each run, before the next launch; a VOID run still counts as a trial.

## Fold B and the basket

- **Windows:** `fold: "B"` in `machine_constraints.protocol` makes the protocol
  generator write config/folds.yaml's six fold-B blocks
  (`run_phase1_research._protocol_windows_from_constraints`, D-085): 2018-05,
  2019-01, 2019-09, 2020-05, 2021-01, 2021-09, each 4 months. No window is
  written by hand.
- **Basket: 3 coins (BTC, ETH, LTC), identical in the three runs, set by the
  sma200 warm-up** (every coin needs daily bars from 2017-03-27 or earlier).
  Dropped from v2's 8: TRX (first daily bar 2020-03-05), ADA (2018-09-28),
  DOGE (2019-12-19), LINK (2019-09-25), UNI (2020-10-15) start after it; XRP
  (2017-05-18) leaves the 2018-05 sma200 prefetch at 347/400 rows and the
  readiness probe fails. XMR and ZEC have the history but stay excluded by the
  operator's universe rule: [OPERATOR: the rule's reason]. **Limit:** 3 coins,
  two of them (BTC, ETH) already looked at by run_054 (below); a result here
  is about 3 large coins, not a breadth basket. The warm-up is not relaxed to
  add coins.

## Continue rule (pre-registered)

Inputs, per run:

- **Sharpe:** `artifacts/profit_bars_evaluation.yaml`, row `sharpe_min`, its
  `actual`: the equal-weight portfolio's chained daily returns, mean / sample
  stdev x sqrt(365), rf 0 (`tools/portfolio_whole_test.py` `whole_test_sharpe`),
  after fees and slippage (funding is not modelled). Flat = 0.
- **Base curve-based gross/cost (sma100 run only):** CUL-431's figure,
  `tools/curve_cost_ratio.curve_gross_to_cost(list(tools/curve_cost_ratio.load_run_accounts(<run folder>).values()))["ratio"]`:
  per coin-window account, in currency / starting capital, gross = equity
  change + fees + slippage; ratio = sum of gross / sum of fees + slippage over
  all accounts; no min(). If PR #390 is not merged at launch, the same function
  is run offline from PR #390's commit `0cf0f687` (file
  `strategy-research/tools/curve_cost_ratio.py`), never the lot-based ratio
  (`pooled_edge_to_cost_ratio`). A `ValueError` from it (lot net P&L not equal
  to an account's equity change) means the figure cannot be read: report it,
  do not judge the rule on it.

**CONTINUE** iff whole-test Sharpe after fees and slippage > 0 on at least 2 of
3 runs AND the base run's curve-based gross/cost (item B) >= 2.

**Outcomes, written in advance:**

- **Holds:** a registry entry with the fold-A and fold-B numbers (Sharpe of the
  three runs on each fold, the base run's curve-based gross/cost on each);
  lineage folds A and B used. A fold-B confirmation makes a registry block, not
  a tradeable strategy: the profit bars stay the gate.
- **Fails:** refuted on unseen data. Next: the lane order (funding carry after
  E-053).

Reported, never decided on: trade counts, window-end closes and their share of
costs, the lot-based ratio, buy-and-hold excess.

## Predictions (two-phase: a measured count far from these is a bug to explain)

Distance-from-SMA sign changes counted on the cached Kraken daily closes, read
only up to 2021-12-31 (no return computed), current-close timing, flat at each
4-month window's start, pooled over the 3 coins; the same method reproduces v2's
fold-A predictions exactly (195 / 138 / 86 exits, 12 / 14 / 15 window-end
closes). This run (lookback 100): about **32 exits by signal** and **10
window-end forced closes**; 49 of 2,190 coin-days sit in the partial-size zone
(0-2% above the average). The measured completed-trade count is expected ABOVE
the exit count (vol-target and partial-size rebalances, lots matched LIFO,
`performance/metrics.py`); entries and exits the 0.2 band blocks lower it.

## Known biases and limits

- **Execution:** decides on the current bar's close and fills at that close, no
  lag; accepted for an automated bot on a 24-hour market.
- **Funding not charged:** perp costs (Kraken futures fee 5 bps per side;
  slippage BTC 2.5, ETH 4, LTC 7.5 bps per side,
  `trading-bot/config/cost_model.json`) on Kraken spot prices (D-057). A long
  perp usually pays funding in rising markets, so results are flattered.
- **Survivorship:** BTC, ETH and LTC all still trade in 2025; the basket is
  chosen by data history, which favours survivors.
- **Prior looks:** run_054 tested SMA(100) daily long-only on Binance BTC and
  ETH over windows reported as 2018-04..2025-09, which cover fold B: for BTC and
  ETH this is not fresh evidence; LTC and the vol targeting are. Fold A's
  results (runs 081-083) are known.
- **Window restarts:** each coin is backtested alone per 4-month window, forced
  flat at its end; indicators are warmed up before each window (warmup_prefetch).
- **Whole-test chain (CUL-431 finding, not fixed):** the chain anchors a window
  at its first day's close after that day's rebalance, so a first-day fill's
  fees and slippage are not in the Sharpe (run_081: 7e-5 to 3e-4 of the
  portfolio in 4 of 6 windows).
- **Run flag set (operator's checkout):** variant_loop off, composition_runs
  off, analyst off, cost_bar_all_costs on, folds on, nearest_build on,
  deviation_gate on (the v2 set, D-105). With the loop off, a data-gate
  "refine" pauses the whole run.
