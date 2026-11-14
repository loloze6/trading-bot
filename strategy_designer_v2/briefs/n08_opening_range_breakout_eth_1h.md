---
research_goal: "On ETH hourly bars, does the range of the first hours of the UTC day (or of a session) predict the direction or size of the rest of the day, in a way that pays after cost?"
venue: kraken
product: "ETH/USD spot"
strategy_domain: opening_range
bar_size: 1h
already_tried:
  - "On ETH hourly, fold B: fading stretches from a rolling VWAP or range midpoint (pending). On BTC: single-bar reversion failed; range-break continuation held."
---
# Opening range on ETH (night brief 08)
Define an opening range from the first N hours of a UTC day or of a session (Asian open at 00 UTC, European at 07 UTC, US at 13 UTC), then test what a break of that range, or a failure to break it, means for the hours that follow. Ideas should cover both direction (continuation or reversal) and size (volatility after the break). Fees 0.15% per round trip. ETH only.
