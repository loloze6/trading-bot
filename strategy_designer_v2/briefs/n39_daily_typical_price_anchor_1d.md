---
research_goal: "On BTC, ETH and LTC daily bars, does the close's distance from a volume-weighted typical-price anchor over 5 to 30 days predict the next days after cost?"
venue: kraken
product: "BTC/USD, ETH/USD, LTC/USD spot"
strategy_domain: daily_vwap_anchor
bar_size: 1d
already_tried:
  - "On ETH hourly, fold B: stretches from a rolling 24h volume-weighted price and from a range midpoint did not revert in a way that pays. On LTC and XRP hourly: a volume-burst stretch with a pullback bar continued."
---
# A volume-weighted anchor on daily bars (night brief 39)
The volume-weighted typical price over a window is where the money traded. This brief asks whether the close's distance from it, in units of recent volatility, predicts reversion or continuation over the next 2 to 10 days on three coins. Ideas must define the anchor window and the stretch unit. Fees 0.15% per round trip. All three coins must pass.
