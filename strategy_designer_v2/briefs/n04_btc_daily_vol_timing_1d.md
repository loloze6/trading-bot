---
research_goal: "On BTC daily bars, does the state of volatility (level, trend, compression, expansion) time entries and exits so that a simple directional rule becomes profitable after cost?"
venue: kraken
product: "BTC/USD spot"
strategy_domain: daily_volatility_timing
bar_size: 1d
already_tried:
  - "On BTC daily: none yet in v2. On ETH daily: volatility-expansion gate on a 50-day trend, compression precedes a move (abs ratio 0.96 against 1.15 asked), post-shock trend failure, all failed."
---
# Volatility timing on BTC daily bars (night brief 04)
Volatility is the one thing the clock and the bars predict well. This brief asks whether it times direction: rules that enter after compression, exit on expansion, size by volatility state, or switch between momentum and reversal by volatility regime. Measures may be profit measures. Ideas must say what the volatility state is, computed from the bars, and what the directional rule is. Fees 0.15% per round trip. BTC only.
