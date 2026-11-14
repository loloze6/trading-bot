---
research_goal: "On BTC and ETH hourly bars, does the recent autocorrelation of returns (a momentum regime against a reversal regime, measured over days) decide whether a short-horizon continuation or reversal rule pays after cost?"
venue: kraken
product: "BTC/USD, ETH/USD spot"
strategy_domain: hourly_autocorrelation_regimes
bar_size: 1h
already_tried:
  - "On ETH hourly, fold A: momentum over 24 to 168 bars as rankings and rules, a 24h short reversal passed the judge only; on ETH daily, fold A: a 60-day lag-1 autocorrelation regime for a 20-day trend failed."
---
# Autocorrelation regimes on hourly bars (night brief 29)
Hourly returns sometimes continue and sometimes reverse, and the state lasts days. This brief asks whether the trailing autocorrelation of hourly returns (lag 1 to lag 24, over 2 to 14 days) is a readable state, and whether a continuation rule in the positive state and a reversal rule in the negative state pay after 0.15% per round trip. Ideas must say the lag, the window and the rule. Both coins must pass.
