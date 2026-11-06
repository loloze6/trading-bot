---
research_goal: "On BTC and ETH hourly bars, does a slow state computed over many days (trend, volatility level, drawdown from a high) decide when hourly entries pay, so that the hourly rule only trades with the daily state?"
venue: kraken
product: "BTC/USD, ETH/USD spot"
strategy_domain: multi_horizon_gate
bar_size: 1h
already_tried:
  - "On BTC and ETH hourly: gates built from session clocks and volume surprises did not make any direction rule pay. On BTC hourly: range-break continuation held."
---
# A slow state as the gate for fast entries (night brief 11)
Hourly rules fail mostly because they trade in every state of the market. This brief asks for a slow state, computed from several days of hourly bars (a 7 to 30 day trend, a volatility level against its own history, the distance from a multi-week high), and an hourly entry that only fires when the slow state says so. Ideas must say both parts and measure the gated rule against the ungated one where possible. Fees 0.15% per round trip. Both coins must pass.
