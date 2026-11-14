---
research_goal: "On BTC and ETH daily bars, do multi-bar price patterns (inside bars, engulfing bars, three-bar reversals, wick rejections at range edges) carry a return edge after cost?"
venue: kraken
product: "BTC/USD, ETH/USD spot"
strategy_domain: daily_price_patterns
bar_size: 1d
already_tried:
  - "On BTC and ADA daily, fold A: a lower-wick rejection claim failed with few events; close-location-in-range claims failed on ETH daily and ETH hourly."
---
# Price patterns on daily bars (night brief 21)
Traders name bar shapes. This brief asks whether any of them, defined exactly from open, high, low and close of two to three consecutive bars, predicts the next days on BTC and ETH. Ideas must state the pattern as code and the horizon, and should expect few events, so the pattern must be common enough to count. Fees 0.15% per round trip. Both coins must pass.
