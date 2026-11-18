---
idea: 014-02_pre-settlement-drop-after-rise
brief: 014_funding-settlement-hour-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: untestable
catalogue: 791f9c660ae8
---
Fidelity:
- Situation: the coin has risen over the past 3 days -> kept: 3-bar price change on daily bars
- Comparison: the larger the 3-day rise, the larger the decline -> kept: a graded forecast sized by the rise
- Outcome: negative return over the 2 hours before each 00:00, 08:00 and 16:00 UTC settlement -> replaced: a 2-hour intraday window cannot be seen on daily bars, only the whole day's return
- Verdict transfer: no: a test of next-day returns would say nothing about the 2-hour pre-settlement windows the idea names
Reason: The outcome's horizon is 2 hours before each settlement time, shorter than one 1d bar, so it does not fit the bar size. Daily bars also cannot isolate the 08:00 and 16:00 UTC settlements from the rest of the day, and the config has no time-of-day logic below the bar size.
