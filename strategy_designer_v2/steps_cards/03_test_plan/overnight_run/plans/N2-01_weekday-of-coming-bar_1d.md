---
idea: N2-01_weekday-of-coming-bar
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: missing-components
---
Fidelity:
- Situation: the coming daily bar is the Saturday session, after a Friday-dated bar -> replaced: no component can single out the coming Saturday; the closest, WeekdayReturnComponent, trades every weekday.
- Comparison: the coin's average day -> kept: WeekdayReturnComponent subtracts the mean of all past bar returns.
- Outcome: the Saturday bar returns more than average, so long into it -> replaced: WeekdayReturnComponent picks its side from past Saturday returns, not a fixed long on Saturday.
- Verdict transfer: no: a learned weekday-seasonality forecast on all seven days does not test the fixed claim "Saturday beats the average day".
Reason: The bar's own timestamp holds the day of the week, and the config can express the idea: a regime rule active only on Friday-dated bars, holding a graded long component. But no catalogue component outputs the coming bar's weekday as a value a rule can test, and no combination of components rebuilds it.
