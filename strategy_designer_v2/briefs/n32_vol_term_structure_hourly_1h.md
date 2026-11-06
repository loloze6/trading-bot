---
research_goal: "On BTC and ETH hourly bars, does the ratio of short-horizon to long-horizon realised volatility (the volatility term structure) predict direction or the success of trend and reversal rules after cost?"
venue: kraken
product: "BTC/USD, ETH/USD spot"
strategy_domain: vol_term_structure
bar_size: 1h
already_tried:
  - "On ETH daily: a 20-day over 60-day volatility expansion gate on a 50-day trend failed. On BTC daily: momentum in a low-volatility regime passed the engine at a volatility target. On BTC and ETH hourly: weekday-gated cross passed the engine on BTC only."
---
# The volatility term structure on hourly bars (night brief 32)
When short volatility runs above long volatility something is happening; when below, the market is asleep. This brief asks whether that ratio on hourly bars (24h against 168h, 6h against 72h, and others) predicts the next bars' direction, or decides whether a momentum or a reversal rule pays. Ideas must state both windows. Fees 0.15% per round trip. Both coins must pass.
