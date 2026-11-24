---
idea: 031-03_up-streak-length-continuation
brief: 031_daily-close-streak-reversal-or-continuation
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 31f1a8c6c7f6
---
Fidelity:
- Situation: a coin has closed higher several days in a row -> kept: a regime keeps up-close streaks only (MovingAverageAgeComponent, period 2, is +n after n higher closes).
- Comparison: the streak length against the coin's own up-close streak lengths over the past 365 days -> replaced: no component ranks the current up-streak length among the coin's past up-streak lengths.
- Outcome: the coin keeps rising over the next 5 days, more after longer streaks -> kept: long, held 5 bars on 1d bars.
- Verdict transfer: no: without the 365-day up-streak comparison, the position cannot grow with how unusual the streak is, so neither verdict would carry over.
Reason: The streak length is in the coin's own closes, and a regime plus one graded component could hold the idea. No component, alone or combined, grades the current up-close streak length against the coin's own up-streak lengths over the past 365 days. MovingAverageAgeComponent is a regime measure, not a forecast source. Standardised over 365 bars, it would divide by a per-bar mean that mixes in down-streaks, which is not the comparison the idea states.
