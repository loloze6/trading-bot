---
research_goal: "On LTC and XRP hourly bars, does a stretch from a rolling anchor (volume-weighted price, range midpoint, slow mean) revert within hours by more than cost?"
venue: kraken
product: "LTC/USD, XRP/USD spot"
strategy_domain: hourly_stretch_older_coins
bar_size: 1h
already_tried:
  - "On ETH hourly, fold B: twelve stretch-and-revert claims; two passed the judge (Asia hours, weekend) and failed the engine; the rest failed. On BTC hourly: single-bar fades failed in every form."
---
# Stretch and reversion on older coins, hourly (night brief 28)
ETH did not revert from its anchors in a way that pays. This brief asks the same question on two older, differently traded coins, with freedom on the anchor, the stretch unit (recent volatility), the horizon and any condition on the hour or the volume. Fees 0.15% per round trip. Both coins must pass.
