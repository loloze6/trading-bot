---
research_goal: "On BTC and ETH hourly bars, which trend-following rules (moving-average cross, breakout, time-series momentum) pay after cost, and does a volatility or volume gate change the answer?"
venue: kraken
product: "BTC/USD, ETH/USD spot"
strategy_domain: hourly_trend
bar_size: 1h
already_tried:
  - "On ETH daily: moving-average and breakout trends with volatility gates failed. On BTC and ETH hourly: gated rules in the US-open and volume-surprise hours all failed (continuation, reversal, range break, volume sign)."
---
# Hourly trend following with gates (night brief 10)
Trend rules on hourly bars trade often and pay fees often. This brief asks whether any pays after 0.15% per round trip, with or without a gate that stands aside in quiet hours or whipsaw. Ideas should state the trend rule, the horizon the position is held, and the gate if any; a rule without a gate is a fair idea too. Both coins must pass.
