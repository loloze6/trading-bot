---
idea: 014-04_post-settlement-rebound-after-selloff
brief: 014_funding-settlement-hour-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: untestable
catalogue: 791f9c660ae8
---
Fidelity:
- Situation: risen over the past 3 days, then fallen in the 2 hours before a funding settlement -> replaced: daily bars cannot show a 2-hour pre-settlement move.
- Comparison: the larger the pre-settlement fall, the larger the post-settlement gain -> replaced: the fall's size inside the day is not in daily bars.
- Outcome: positive return over the 2 hours after settlement -> replaced: a 2-hour horizon is shorter than one 1d bar.
- Verdict transfer: no: no test on daily bars can confirm or reject a move inside 2-hour windows around settlement times.
Reason: The idea's situation and outcome are 2-hour windows around funding settlement times, and its horizon of 2 hours is shorter than one bar on the 1d bars the test runs on. The config sees only whole daily bars, so it cannot isolate pre- or post-settlement moves.
