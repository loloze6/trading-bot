---
idea: 018-03_hourly-surge-gain-before-close
brief: 018_daily-condition-caught-on-the-hour
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: untestable
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: 24-hour return, read at an hourly close, first reaches several times its usual size on the upside -> adapted: PriceEvolutionComponent(24) standardised over 720 bars is the 24-hour return in multiples of its 30-day mean absolute daily return, graded instead of a threshold, and "while" instead of "first reaches".
- Comparison: several times the 30-day average absolute daily return -> kept: standardise's past mean of absolute 24-bar returns over 720 bars is that average.
- Outcome: price keeps rising from that hour to the same day's daily close, more for larger multiples -> replaced: the horizon ends at a clock time (00:00 UTC), so it runs 1 to 23 bars by the hour of entry, and a fixed holding period would measure a different span.
- Verdict transfer: no: a fixed-bar hold would judge a move past or short of the daily close, not the move to it.
Reason: The idea's horizon is "to the same day's daily close", which lasts from 1 to 23 hourly bars depending on the hour the situation first holds. The config allows only one fixed holding period (`min_holding_bars`) and has no exit at a clock time, so the book cannot hold each bet exactly until the daily close.
