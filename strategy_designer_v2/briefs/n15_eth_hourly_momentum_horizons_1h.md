---
research_goal: "On ETH hourly bars, which horizon of past return (1 to 7 days) best predicts the next 1 to 3 days, and does it survive cost as a rule?"
venue: kraken
product: "ETH/USD spot"
strategy_domain: hourly_momentum_horizons
bar_size: 1h
already_tried:
  - "On ETH hourly: stretch-from-anchor fades failed; Asia-hours stretch fade and weekend stretch continuation passed the judge but not the profit bar."
---
# Momentum horizons on ETH hourly bars (night brief 15)
Time-series momentum is horizon-specific. This brief asks which past-return horizon, measured on hourly bars over 24 to 168 bars, predicts forward returns over 24 to 72 bars, as a rank correlation first and as a rule second. Ideas should cover plain, volatility-scaled and sign-only versions. Fees 0.15% per round trip. ETH only.
