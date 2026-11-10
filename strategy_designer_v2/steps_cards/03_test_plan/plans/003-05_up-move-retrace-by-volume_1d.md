---
idea: 003-05_up-move-retrace-by-volume
brief: 003_thin-volume-moves-revert
data-instruments: BTC/USDT
data-bar: 1d
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a sharp upward move on low or on high volume -> adapted: the move is the one-bar rise, graded by its size; low versus high is the bar's volume against its 20-bar mean, set as a regime condition.
- Comparison: thin moves against heavy moves of similar size -> adapted: both groups are sized by the same graded move size and compared per unit of position.
- Outcome: thin moves give back more of the rise, heavy moves hold -> adapted: the holding period is dropped, so the outcome is the next bar's return after each up bar.
- Verdict transfer: yes: the test compares returns after thin and heavy up moves of matched size, which is the theory's own pass/fail condition.
Forecast: The forecast uses one indicator, the one-bar percent change of the close (PriceEvolution, period 1), standardised over 60/20. It then goes through signed_power with exponent 2, so small moves are damped and sharp moves dominate. The regime detector decides which way the forecast points: - On an up bar whose volume is at or above its 20-bar mean ("heavy"), the regime is trending and the forecast is long, growing with the move's size. - On an up bar with volume below that mean ("thin"), the regime is mean_reversion and the same quantity is negated, so the forecast is short, growing with the move's size. - On down or flat bars the forecast is zero.
Config: 003-05_up-move-retrace-by-volume_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Each up bar is weighted by the absolute value of its forecast, and its next-bar coin return is recorded. The measure is the weighted mean of those returns after heavy up bars minus the same mean after thin up bars, with a Welch t-test pooled over the 6 windows. Taking the difference cancels the coin's own drift, which plays the role of the buy-and-hold benchmark.
- Supporting check: The weighted mean next-bar return after thin up bars, minus the coin's unconditional mean daily return over the same windows, should be negative.
- Confirm: The heavy-minus-thin difference is positive with t ≥ 2. Returns are 1-bar and do not overlap, so each bar counts once.
- Reject: The heavy-minus-thin difference is negative with t ≤ -2, meaning thin moves hold better than heavy ones.
- Inconclusive: Any t between -2 and 2, including a difference of either sign. The test is also inconclusive if fewer than 30 forecast-bearing up bars fall in either group across all windows.
