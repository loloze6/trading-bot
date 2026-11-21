---
idea: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues
brief: 022_weak-effects-combined-by-what-worked-before
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 7b01a83193f3
---
Fidelity:
- Situation: a coin's 60-day return, by its size and sign -> kept
- Comparison: larger 60-day returns against smaller ones (the larger, the more) -> kept
- Outcome: the coin moves the same way over the next 20 days -> kept
- Verdict transfer: yes: the forecast is the 60-day return itself, graded, held for 20 days, so its gains test exactly this claim.
Forecast: The 60-bar percent return of the coin (PriceEvolutionComponent, period 60), standardised against the mean absolute size of its own past 61 values. It is positive after a 60-day rise and negative after a 60-day fall. It grows in proportion to the size of the return, about ±10 at a usual size, capped at ±20, and it is 0 only when the return is 0. It has no regime and runs on every bar.
Config: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days.d2_sixty-day-trend-continues_1d_config.json
Criterion:
- Horizon: 20 bars
- Main measure: On each window's non-overlapping 20-bar grid, pooled over all coins and windows, take per case the recorded forecast / 10 x (close[t+20] / close[t] - 1 minus the coin's normal 20-bar drift over all its windows). Report the t of the mean of this value and the number of cases.
- Supporting check: Split the grid cases at the median of abs(forecast). The mean unusual move in the forecast's direction must be higher in the larger half than in the smaller half (difference larger minus smaller > 0).
- Confirm: Main-measure t >= 2 over at least 300 cases, and the supporting check passes.
- Reject: Main-measure t <= -2 over at least 300 cases.
- Inconclusive: Any t between -2 and 2. Also t >= 2 with a failed supporting check, or fewer than 300 cases.
