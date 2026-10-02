---
# C4 Kraken-perp brief (operator, 2026-10-02; Linear CUL-375, epic E-065).
# SUPERSEDES briefs/C4_vol_managed_trend.md, whose trials (run_061, run_064)
# ran on Binance spot data and costs before the brief's venue reached the
# backtest (O-12, D-057). Same idea; only the venue product and the test
# period change, so the old trials stay counted under the old brief.
#
# END-TO-END WORKFLOW RUN, NOT AN EDGE TEST: two years (2022-2023) in six
# 4-month windows (D-059, RUNBOOK 1f). Too short for the 100-trades-per-coin
# and era-stability bars -- a "not evaluable" verdict is the expected outcome.
#
# Venue: Kraken futures costs (5 bps fee, per-coin slippage) with Kraken SPOT
# prices as a declared proxy; funding not modelled (D-057, option A).
# No promotion block and no pass_rule: criteria come from step 1a.

strategy_domain: "volatility_managed_trend"
market_universe: [BTCUSDT, ETHUSDT]
timeframe: "1h"
venue: "kraken"
product: "perp"
research_goal: >
  Test whether multi-week time-series momentum on BTC and ETH, with position
  size scaled inversely to recent realised volatility, earns a return after
  fees and slippage that beats buy-and-hold. The other side: slow-reacting
  flows that keep trending after large re-pricings; vol scaling is there to
  cut exposure in the high-volatility crash regimes where plain trend
  following loses most. It must trade slowly enough that costs stay a small
  share of the edge, yet reach 100 trades per coin over the whole test.
constraints:
  - "End-to-end workflow run on 2022-2023 only (six 4-month windows): not an edge test. The 100-trades-per-coin and era-stability bars are not expected to be met; design the idea as you would for the full history."
  - "Funding is not modelled on this venue (Kraken spot prices as a proxy for futures): do not use the funding_rate feed."
available_data: []

criteria_from: hypothesis_generation

machine_constraints:
  protocol:
    symbols: [BTCUSDT, ETHUSDT]
    timeframe: "1h"
    start: "2022-01-01"
    end: "2023-12-31"
    window_months: 4
---

# Volatility-managed trend on BTC/ETH 1h, Kraken perp (C4, end-to-end run)

Same idea as the first C4 brief (D-050, idea A from engineering/C4_PREP.md §3),
re-registered on Kraken futures costs for the first end-to-end run of the new
pipeline on the venue the team will trade (epic E-065). Already tried on this
campaign and not repeated here: RSI, Keltner, plain SMA trend, funding-rate
mean reversion.
