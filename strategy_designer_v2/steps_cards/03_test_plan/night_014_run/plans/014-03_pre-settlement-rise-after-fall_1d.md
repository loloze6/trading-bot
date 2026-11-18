---
idea: 014-03_pre-settlement-rise-after-fall
brief: 014_funding-settlement-hour-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: untestable
catalogue: 791f9c660ae8
---
Fidelity:
- Situation: the coin has fallen over the past 3 days, more fall meaning more strength -> kept: a 3-bar price change on daily bars, graded by the fall's size.
- Comparison: none -> kept
- Outcome: a positive return in the 2 hours before each funding settlement (00:00, 08:00, 16:00 UTC) -> replaced: daily bars cannot isolate a 2-hour intraday window, so only the next full day's return is measurable.
- Verdict transfer: no: a test of next-day returns after a 3-day fall measures short-term reversal, not pre-settlement pressure, so neither result would carry over to the idea.
Reason: The idea's horizon is the 2 hours before each settlement, which is shorter than the 1-day bar, so the outcome does not fit the bar size. The intraday window cannot be isolated from daily bars, and no config can address specific hours inside a bar.
