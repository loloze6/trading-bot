---
idea: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e1_thirty-day-trend-continuation-graded
brief: 024_exhaustion-after-an-extended-run
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 9111077ea370
---
Fidelity:
- Situation: the coin's plain 30-day return, larger rise means a stronger situation -> kept: 180-bar percent return, graded, long only.
- Comparison: beyond the coin's normal drift -> kept: forward returns are measured minus the coin's mean 18-bar return over all windows.
- Outcome: the coin rises over the next three days, more after larger rises -> kept: 18-bar forward return; the position is held 18 bars.
- Verdict transfer: yes: the forecast is the idea's own 30-day return and the measure is its own 3-day excess rise.
Forecast: The forecast uses one indicator, the 180-bar (30-day) percent return of the close (PriceEvolutionComponent, period 180). Standardise divides it by the mean absolute value of its previous 180 values (min_periods 45). That scales it to about 10 on a typical rise, capped at 20. A clip at 0 removes the short side. The forecast is positive and grows in proportion to the 30-day rise. It is near 0 for a weak rise and exactly 0 for a flat or negative 30-day return. There is no regime: it is active on every bar.
Config: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e1_thirty-day-trend-continuation-graded_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: Use the non-overlapping 18-bar grid of each window, all coins pooled. Regress each cell's 18-bar forward return from the cell's bar, minus that coin's normal drift (mean 18-bar return over all its windows), on the forecast at that bar. Report the slope's t. Judge before costs.
- Supporting check: none
- Confirm: The slope is positive with t >= 2: excess 3-day returns grow with the forecast's size.
- Reject: The slope is negative with t <= -2: larger 30-day rises are followed by smaller-than-drift 3-day returns.
- Inconclusive: A t between -2 and 2 is inconclusive, including a slope near zero. At least 100 grid cells with forecast > 0 are required, and at least 500 cells in total; with fewer, the result is inconclusive.
