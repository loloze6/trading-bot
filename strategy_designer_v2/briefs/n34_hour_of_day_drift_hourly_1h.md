---
research_goal: "On BTC, ETH and LTC hourly bars, do particular UTC hours or blocks of hours carry a return drift (not only volatility) that pays after cost when held only through those hours?"
venue: kraken
product: "BTC/USD, ETH/USD, LTC/USD spot"
strategy_domain: hour_of_day_drift
bar_size: 1h
already_tried:
  - "On BTC, ETH, SOL hourly, fold A: the US open hour and weekends are volatility effects; a US-session underperformance claim and an Asian-session continuation failed; hour-of-day persistence failed. On ETH hourly, fold B: Asia-hours stretch fade passed the judge, not the engine."
---
# Hour-of-day drift on hourly bars (night brief 34)
If some hours move more, do some hours move one way? This brief asks for blocks of UTC hours, on weekdays or on all days, where the mean return differs from the rest and a rule that is long or short only through those hours pays after 0.15% per round trip. Ideas must name the hours exactly. All three coins must pass.
