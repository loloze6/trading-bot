---
research_goal: "On ZEC and LTC hourly bars, do channel breakouts or time-series momentum rules pay after cost, with or without a volatility gate?"
venue: kraken
product: "ZEC/USD, LTC/USD spot"
strategy_domain: hourly_trend_other_coins
bar_size: 1h
already_tried:
  - "On BTC and ETH hourly, fold C: a 72h channel breakout passed the engine at a volatility target; on LTC and XRP it failed the judge. On BTC: a weekday-gated cross passed the engine at the volatility target; on LTC and XRP it failed."
---
# Hourly trend rules on ZEC and LTC (night brief 37)
Trend rules that pay on the two largest coins have failed on others as replications. This brief asks for trend rules designed for these two coins from the start: channel length, momentum horizon, exit and gate chosen for their behaviour, and measured as rules after 0.15% per round trip. Both coins must pass.
