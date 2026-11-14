---
research_goal: "Does a big hourly bar that closes beyond the prior day's range continue, on coins other than BTC, and does the inside-range bar fail to revert there too?"
venue: kraken
product: "SOL/USD, LINK/USD spot"
strategy_domain: range_break_continuation
bar_size: 1h
already_tried:
  - "On BTC hourly, fold A: a big bar (3x weekly volatility) closing beyond the prior 24h high or low continued over 12 bars (+0.6% against inside-range big bars, 6 of 6 windows); fading any big bar failed."
---
# Range-break continuation on other coins (night brief 06)
A mechanism found on BTC is a claim about BTC until it is found elsewhere. This brief asks the same family of questions on two other coins (LINK replaces AVAX, whose history before fold A is too short for the engine's warm-up), with freedom on the definitions: what counts as a big bar, what counts as the range, what horizon, and whether volume or time of day sharpens it. Ideas that contradict the BTC finding are welcome. Fees 0.15% per round trip. Both coins must pass.
