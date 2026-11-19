---
idea: 017-05_settlement-move-reverses-after
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: 4e6cc97f57e5
---
Fidelity:
- Situation: the 2-hour return just before each funding settlement time (00, 08, 16 UTC) -> replaced: no catalogue component reads the bar's clock hour, so settlement bars cannot be singled out.
- Comparison: the post-settlement return judged against the pre-settlement return, opposite in sign -> kept: a negated 2-bar scaled return, `VolatilityScaledReturnComponent` with period 2, sets the side.
- Outcome: over the 2 hours after settlement, price moves back against the pre-settlement move, more after a larger move -> adapted: "after settlement" becomes "while on the 2 bars after a settlement hour", which also needs the clock hour.
- Verdict transfer: no: without the settlement clock, any test spreads the bet over every hour, so it tests reversal in general, not the settlement effect.
Reason: The idea's situation and its 2-hour window depend on the UTC hour of the bar. The hour is in the bars' own `timestamp`, and a regime rule could hold it ("hour between 7.5 and 9.5"). But no catalogue component outputs the hour of day: `WeekdayComponent` gives only the weekday, and the funding components fire on/off or carry the print forward. Combining components does not recover it.
