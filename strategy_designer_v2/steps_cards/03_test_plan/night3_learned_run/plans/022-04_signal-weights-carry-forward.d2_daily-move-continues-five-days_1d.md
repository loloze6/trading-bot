---
idea: 022-04_signal-weights-carry-forward.d2_daily-move-continues-five-days
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: the size and sign of the coin's move over the last day -> kept
- Comparison: larger daily moves against smaller ones -> kept
- Outcome: a move in the same direction over the next 5 days, larger after a larger day -> kept
- Verdict transfer: yes: the forecast is the last day's return, signed and graded, held for 5 days, so its 5-day result answers the idea directly.
Forecast: One indicator, the last bar's percent close-to-close return (PriceEvolutionComponent, period 1 bar). It is standardised against the mean absolute size of its previous 60 daily values (min_periods 20), so a usual day reads about ±10 and a day twice the usual size reads ±20, the cap. It runs on every bar with no regime condition. The forecast is positive after an up day and negative after a down day. It is zero only on a flat day. Its size grows in proportion to the size of the day's move.
Config: 022-04_signal-weights-carry-forward.d2_daily-move-continues-five-days_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Use the non-overlapping 5-bar grid of each window, pooled over coins. Regress the coin's 5-bar forward return from the grid bar's close, minus that coin's mean 5-bar return over all its windows, on the forecast at that bar. Report the slope's t.
- Supporting check: The book's mean daily return, before costs, minus its gain from the market's own rise, is above 0.
- Confirm: The slope's t is 2 or more and the supporting check passes.
- Reject: The slope's t is -2 or less, meaning large days are followed by reversals.
- Inconclusive: The slope's t lies between -2 and 2, or the t is 2 or more but the supporting check fails. The test also needs at least 300 grid cases with a non-zero forecast; the expected count is about 3400.
