---
idea: 017-03_postsettle-recovery-after-uptrend
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: a strong 3-day run up, at each funding settlement time (00:00, 08:00, 16:00 UTC) -> replaced: no component reads the hour of day; only the funding component's bars stamped 00, 08 and 16, which close one hour after settlement and depend on the funding feed.
- Comparison: the post-settlement return judged against zero, larger with a stronger 3-day rise -> adapted: the rise becomes a graded 72-bar return.
- Outcome: price rises over the 2 hours after settlement -> adapted: the 2-bar hold becomes "while within 2 hours after settlement".
- Verdict transfer: no: the funding-based clock starts one hour late and fails on coins with no funding prints, so neither a confirm nor a reject would carry over to the idea.
Reason: The idea needs the bar's UTC clock hour, which is in each bar's own timestamp, and a regime rule could select the two bars after each settlement. No catalogue component outputs the hour of day: `WeekdayComponent` gives only the weekday, and the funding components' hour check is on/off, one bar late and depends on funding data.
