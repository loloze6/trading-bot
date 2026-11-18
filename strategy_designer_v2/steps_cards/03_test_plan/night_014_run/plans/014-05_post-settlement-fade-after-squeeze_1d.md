---
idea: 014-05_post-settlement-fade-after-squeeze
brief: 014_funding-settlement-hour-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: untestable
catalogue: 791f9c660ae8
---
Fidelity:
- Situation: a fall over the past 3 days, then a rise in the 2 hours before a funding settlement -> replaced: daily bars cannot see the 2 hours before a settlement time.
- Comparison: the size of the pre-settlement rise against the size of the post-settlement decline -> replaced: no intraday rise can be measured on 1d bars.
- Outcome: a negative return over the 2 hours after settlement -> replaced: a 2-hour horizon is shorter than one 1d bar.
- Verdict transfer: no: a daily-bar test cannot isolate the hours around settlement, so its result says nothing about the idea.
Reason: The idea's situation (the 2 hours before a settlement) and its horizon (2 hours after) are shorter than one bar on the 1d bars this test runs on. No config on daily bars can see or time them, and the outcome horizon does not fit the bar size.
