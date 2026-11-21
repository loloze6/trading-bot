---
idea: 022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: a coin's 28-day rise -> kept: the 28-bar return, long side only.
- Comparison: its size against the coin's own usual 28-day moves -> kept: `standardise` divides it by the mean absolute 28-bar return of the 60 prior bars.
- Outcome: the coin rises more over the next 5 days, the larger that rise -> kept: graded long position, held 5 bars.
- Verdict transfer: yes: the forecast is the 28-day rise in units of the coin's usual 28-day move, and the test is whether 5-day gains grow with it.
Forecast: Take the coin's 28-bar percent return (PriceEvolutionComponent, period 28). Standardise it against the mean absolute size of its 60 previous values (min 20). This gives about +10 for a rise of usual size, more for larger rises, capped at +20. Then clip at 0, so the forecast is long only. It is positive and grows with the rise's size relative to usual 28-day moves. It is 0 when the coin fell over 28 days. It is never negative.
Config: 022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The OLS slope of the coin's 5-bar return minus its normal 5-bar drift on the forecast at the cell's first bar. Cells are the non-overlapping 5-bar grid of each window, pooled over coins and windows. The normal drift is the coin's mean 5-bar return over all its windows.
- Supporting check: The mean drift-adjusted 5-bar return over cells with forecast > 0 is above 0.
- Confirm: The slope's t is 2 or more and the supporting check passes.
- Reject: The slope's t is -2 or less.
- Inconclusive: Any slope t between -2 and 2, or a t of 2 or more with the check failing. At least 300 grid cells are needed, at least 100 of them with forecast > 0; with fewer, the result is inconclusive.
