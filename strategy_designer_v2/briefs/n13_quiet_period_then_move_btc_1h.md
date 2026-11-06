---
research_goal: "On BTC hourly bars, does the length of a quiet period (bars since the last large move, or a narrow multi-hour range) predict the size or direction of the next move?"
venue: kraken
product: "BTC/USD spot"
strategy_domain: quiet_period
bar_size: 1h
already_tried:
  - "On BTC hourly: single-bar reversion failed; range-break continuation held; a spike raises the next 6h volatility by 1.2x (asked 1.5x)."
---
# Quiet periods on BTC hourly bars (night brief 13)
Markets alternate between quiet and loud. This brief asks what the quiet tells: after N hours without a large bar, or after the narrowest 12-hour range in a week, is the next move larger (a volatility claim) and is its direction readable from the drift inside the quiet period (a return claim)? Ideas must define quiet from the bars and name the horizon. Fees 0.15% per round trip. BTC only.
