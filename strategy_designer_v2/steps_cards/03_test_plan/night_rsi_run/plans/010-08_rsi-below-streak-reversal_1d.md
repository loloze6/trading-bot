---
idea: 010-08_rsi-below-streak-reversal
brief: 010_rsi-midline-regime-direction
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 70a362722b07
---
Fidelity:
- Situation: the 14-day RSI has stayed below 50 without a break, counted in days up to the current close -> kept: RsiMidlineAgeComponent(14) gives the length of the current run below 50 (the 60-day cap is a setting).
- Comparison: longer runs against shorter runs -> kept: the long position grows with the run length.
- Outcome: the coin's return over the next 14 days is higher -> kept: the next 14 days' return is measured against how long the run has lasted.
- Verdict transfer: yes: the forecast is the run length itself, and the outcome is read at the idea's own 14-day horizon.
Forecast: The forecast is the length of the current run of RSI(14) below 50, in days, capped at 60. It comes from RsiMidlineAgeComponent (period 14, max_bars 60, rsi_window 100). The steps are: - Standardise the signed run length against its own past 160 values. - Negate it, so a run below 50 reads positive. - Clip it at 0. The forecast is long only and grows with the number of consecutive days RSI has stayed below 50. It is small on the first day below 50 and largest on long runs. It is zero whenever RSI is above 50. It is never short.
Config: 010-08_rsi-below-streak-reversal_1d_config.json
Criterion:
- Horizon: 14 bars
- Main measure: The measure uses bars with forecast > 0 on a non-overlapping 14-bar grid in each window, pooled over all coins and windows. On those bars, regress the coin's next-14-bar return minus that coin's mean 14-bar return over all windows on the forecast. Read the t of the slope.
- Supporting check: Among the grid bars with forecast > 0, the mean excess 14-bar return of the top third by forecast minus that of the bottom third is above 0.
- Confirm: The slope's t is +2 or more and the top-minus-bottom-third difference is positive.
- Reject: The slope's t is -2 or less.
- Inconclusive: The idea is neither confirmed nor rejected in either of these cases: - the slope's t is between -2 and +2; - the t is +2 or more but the top-minus-bottom difference is not positive. At least 100 independent grid bars with forecast > 0 are required. With fewer, the result is inconclusive.
