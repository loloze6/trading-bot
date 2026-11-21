---
idea: 018-01_hourly-breakout-gain-before-close
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: untestable
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: hourly close first rises above the highest price of the prior 20 days -> adapted: "first rises above" made "while above", using DistanceFromHighComponent (period 480, source high, exclude_current 1), clipped at 0.
- Comparison: distance above the 20-day high, in multiples of the 30-day average absolute daily return -> replaced: no component gives a 30-day mean absolute daily return, so standardise against its own past values would stand in.
- Outcome: price rises from that hourly close to the same day's daily close -> replaced: the horizon ends at the UTC day's close, so it runs 1 to 24 bars depending on the hour, but min_holding_bars is one fixed count.
- Verdict transfer: no: a fixed holding period and a different scaling unit would test another move than the rise into that day's close.
Reason: The outcome is a move that ends at the same day's daily close, so its length depends on the hour the breakout happens. That is a calendar-timed exit, which the guide says the config cannot express: there are no exits, and min_holding_bars is one fixed number of bars for every bet.
