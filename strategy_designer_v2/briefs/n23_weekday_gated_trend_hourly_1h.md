---
research_goal: "On BTC and ETH hourly bars, does a trend rule that trades only on weekdays, or only outside the weekend compression, pay where the ungated rule does not?"
venue: kraken
product: "BTC/USD, ETH/USD spot"
strategy_domain: weekday_gated_trend
bar_size: 1h
already_tried:
  - "On BTC and ETH hourly, fold C: hourly trend rules with volatility gates (pending in brief 10). On BTC, ETH, SOL hourly: weekend volatility is 0.64 to 0.78 of weekday, 6 of 6 windows."
---
# Weekday-gated trend on hourly bars (night brief 23)
Weekends are quiet and trend rules bleed in quiet markets. This brief asks whether a trend rule (moving-average cross, breakout, time-series momentum over 24 to 168 bars) that is flat from Friday evening to Monday morning, or flat whenever the trailing 24h volatility is in its bottom part, pays where the same rule without the gate does not. Ideas must measure both versions. Fees 0.15% per round trip. Both coins must pass.
