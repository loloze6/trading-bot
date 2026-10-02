---
# C4 Kraken-perp brief (operator, 2026-10-02; Linear CUL-375, epic E-065).
# SUPERSEDES briefs/C4_donchian_daily_trend.md, registered before the brief's
# venue reached the backtest (O-12, D-057); its run_063 never reached a
# backtest. Same idea; only the venue product and the test period change.
#
# END-TO-END WORKFLOW RUN, NOT AN EDGE TEST: two years (2022-2023) in six
# 4-month windows (D-059, RUNBOOK 1f). Too short for the 100-trades-per-coin
# and era-stability bars -- a "not evaluable" verdict is the expected outcome.
#
# Venue: Kraken futures costs (5 bps fee, per-coin slippage) with Kraken SPOT
# prices as a declared proxy; funding not modelled (D-057, option A).
# No promotion block and no pass_rule: criteria come from step 1a.

strategy_domain: "trend_following_breakout"
market_universe: [BTCUSDT, ETHUSDT]
timeframe: "1d"
venue: "kraken"
product: "perp"
research_goal: >
  Test whether a slow channel-breakout trend signal on daily BTC and ETH bars --
  long when the close sits near the top of its recent N-day high-low range, short
  when it sits near the bottom -- earns a return after fees and slippage that
  beats buy-and-hold. The other side: slow-reacting holders and flows that keep
  a multi-week move going after a range breaks; daily bars and multi-day holding
  keep costs a small share of each move. It must still reach 100 trades per coin
  over the whole test.
constraints:
  - "End-to-end workflow run on 2022-2023 only (six 4-month windows): not an edge test. The 100-trades-per-coin and era-stability bars are not expected to be met; design the idea as you would for the full history."
  - "Funding is not modelled on this venue (Kraken spot prices as a proxy for futures): do not use the funding_rate feed."
available_data: []

criteria_from: hypothesis_generation

machine_constraints:
  protocol:
    symbols: [BTCUSDT, ETHUSDT]
    timeframe: "1d"
    start: "2022-01-01"
    end: "2023-12-31"
    window_months: 4
---

# Donchian channel breakout on BTC/ETH daily bars, Kraken perp (C4, end-to-end run)

Same idea as the second C4 brief, re-registered on Kraken futures costs for the
first end-to-end run of the new pipeline on the venue the team will trade (epic
E-065). Families already tried on this campaign and not repeated here: RSI,
Keltner, MACD, moving-average crossover, fear & greed contrarian, funding-rate
extremes.
