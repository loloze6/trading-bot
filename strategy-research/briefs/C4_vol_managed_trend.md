---
# C4 first brief (D-050), filled from
# workflow_artifacts/templates/research_brief_new_pipeline.md (E-061 C1.7).
# Only the four prose fields differ from the template; the protocol block is
# the template's own (see its header for why it is generated, not pinned).
# No promotion block and no pass_rule: criteria come from step 1a.

strategy_domain: "volatility_managed_trend"
market_universe: [BTCUSDT, ETHUSDT]
timeframe: "1h"
venue: "kraken"
product: "spot"
research_goal: >
  Test whether multi-week time-series momentum on BTC and ETH, with position
  size scaled inversely to recent realised volatility, earns a return after
  fees and slippage that beats buy-and-hold. The other side: slow-reacting
  flows that keep trending after large re-pricings; vol scaling is there to
  cut exposure in the high-volatility crash regimes where plain trend
  following loses most. It must trade slowly enough that costs stay a small
  share of the edge, yet reach 100 trades per coin over the whole test.
constraints: []
available_data: []

criteria_from: hypothesis_generation

machine_constraints:
  protocol:
    symbols: [BTCUSDT, ETHUSDT]
    timeframe: "1h"
    start: "2018-02-01"
    end: "2025-12-31"
---

# Volatility-managed trend on BTC/ETH 1h (C4 first brief)

First brief of continuation step C4 (two real runs on the new pipeline).
Decision D-050 (operator, 2026-09-29): idea A from engineering/C4_PREP.md §3.
Already tried on this campaign and not repeated here: RSI, Keltner, plain SMA
trend, funding-rate mean reversion. Funding carry is out until the engine
models funding cash flows (model_funding off, E-014).
