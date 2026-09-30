---
# C4 second brief (operator: "proceed with 3", 2026-09-30), filled from
# workflow_artifacts/templates/research_brief_new_pipeline.md (E-061 C1.7).
# Chosen so a first real run can reach a backtest: the family is untried on this
# campaign (exclusion digest), an existing long/short component covers it
# (DonchianBreakoutComponent), and daily holding periods weaken the per-trade cost
# veto step 1a applied to 1h momentum on run_062 (OBSERVATIONS_QUEUE O-3).
# No promotion block and no pass_rule: criteria come from step 1a.

strategy_domain: "trend_following_breakout"
market_universe: [BTCUSDT, ETHUSDT]
timeframe: "1d"
venue: "kraken"
product: "spot"
research_goal: >
  Test whether a slow channel-breakout trend signal on daily BTC and ETH bars --
  long when the close sits near the top of its recent N-day high-low range, short
  when it sits near the bottom -- earns a return after fees and slippage that
  beats buy-and-hold. The other side: slow-reacting holders and flows that keep
  a multi-week move going after a range breaks; daily bars and multi-day holding
  keep costs a small share of each move. It must still reach 100 trades per coin
  over the whole test.
constraints: []
available_data: []

criteria_from: hypothesis_generation

machine_constraints:
  protocol:
    symbols: [BTCUSDT, ETHUSDT]
    timeframe: "1d"
    start: "2018-02-01"
    end: "2025-12-31"
---

# Donchian channel breakout on BTC/ETH daily bars (C4 second brief)

Second brief of continuation step C4. The first brief (C4_vol_managed_trend) parked
on a missing long/short SMA component (run_061) and was then declared exhausted
(run_062). Families already tried on this campaign and not repeated here: RSI,
Keltner, MACD, moving-average crossover, fear & greed contrarian, funding-rate
extremes.
