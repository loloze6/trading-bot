---
research_goal: "After a stretched intraday move on ETH, measured against the day's own volume-weighted price or range, does price revert within hours by more than cost?"
venue: kraken
product: "ETH/USD spot"
strategy_domain: intraday_stretch_reversion
bar_size: 1h
already_tried:
  - "On BTC hourly: fading a large single bar in any form (low volume, counter-trend, close at extreme, thin hours, cascade) failed; a big bar beyond the prior 24h range continues rather than reverts."
---
# Stretch and reversion on ETH hourly bars (night brief 03)
The BTC overreaction brief showed that a single large bar does not revert. This brief looks at a different stretch: distance from an anchor built over many bars, such as the rolling volume-weighted average price of the last day, the midpoint of the last day's range, or a slow moving mean, in units of recent volatility. Ideas should state the anchor, the stretch unit, the horizon and the comparison bars. Costs 0.15% per round trip. ETH only.
