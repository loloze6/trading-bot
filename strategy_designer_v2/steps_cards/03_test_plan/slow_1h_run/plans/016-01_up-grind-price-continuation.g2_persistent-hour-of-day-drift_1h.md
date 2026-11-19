---
idea: 016-01_up-grind-price-continuation.g2_persistent-hour-of-day-drift
brief: 016_grind-versus-jump-moves
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: missing-components
catalogue: c83038e7c6a3
---
Fidelity:
- Situation: the coin's average return in one UTC hour of day over its past 30 days -> replaced: no catalogue component averages the past 30 same-hour one-bar returns; the closest build is 30 lagged volatility-scaled returns.
- Comparison: higher versus lower same-hour average return, across hours of the day -> kept: a graded forecast that grows with that average.
- Outcome: the coin rises in that same hour over the next day (the coming 1h bar) -> kept: the position is held over the next bar.
- Verdict transfer: no: a forecast built from volatility-scaled, separately standardised lagged returns measures a volatility-weighted drift, not the coin's average hourly return.
Reason: The idea needs the mean of the one-bar returns ending at the same UTC hour on each of the past 30 days, which uses only the coin's own closes. `VolatilityScaledReturnComponent` with `lag` divides each return by its own volatility, and no other component gives a lagged raw one-bar return. So averaging 30 of them changes what is measured, and no catalogue combination computes the plain same-hour mean.
