---
idea: 010-04_rsi-below-streak-continuation
brief: 010_rsi-midline-regime-direction
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 70a362722b07
---
Fidelity:
- Situation: the 14-day RSI has stayed below 50 without a break, counted in days up to the current close -> kept: RsiMidlineAgeComponent (period 14) counts the current run below 50, capped at its default 60 bars.
- Comparison: longer unbroken stretches against shorter ones (graded, "the longer ... the lower") -> kept: the short position grows with the run length.
- Outcome: the coin's return over the next 14 days is lower -> kept: 14-bar forward return, judged against the coin's average return.
- Verdict transfer: yes: the test measures the same run length and the same 14-day return relation, so a confirm or a reject carries over to the idea.
Forecast: RsiMidlineAgeComponent (RSI period 14, max_bars 60, rsi_window 100) gives -n while RSI has been below 50 for n bars and +n while above. It is standardised over its past 160 values (min_periods 40) and then clipped at a maximum of 0. The forecast is zero whenever RSI is above 50. Below 50 it is short, starting near 0 on the first day of a run and growing steadily more negative as the run lengthens, to its cap of -20.
Config: 010-04_rsi-below-streak-continuation_1d_config.json
Criterion:
- Horizon: 14 bars
- Main measure: Use the non-overlapping 14-bar grid of each window, keeping only grid bars with forecast < 0 (RSI below 50). On these bars, regress the coin's 14-bar forward return minus that coin's mean 14-bar return over all windows on the run length (-last_history_value). Read the t of the slope, pooled across the three coins.
- Supporting check: On the same grid bars, the mean 14-bar gain before costs of the position must be above 0. The gain is postRebalance_current_allocation × (14-bar return minus the coin's mean 14-bar return).
- Confirm: The slope is negative with t ≤ -2, and the supporting check's mean gain is above 0.
- Reject: The slope is positive with t ≥ +2: longer runs below 50 are followed by higher excess returns.
- Inconclusive: Any slope with -2 < t < +2, or t ≤ -2 with the check failing. A minimum of 100 independent grid cases with forecast < 0 is required; fewer is inconclusive.
