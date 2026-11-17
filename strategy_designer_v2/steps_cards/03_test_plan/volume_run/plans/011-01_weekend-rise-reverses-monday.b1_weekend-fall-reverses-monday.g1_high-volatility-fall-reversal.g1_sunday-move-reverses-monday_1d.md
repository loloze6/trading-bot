---
idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a coin's Sunday daily return, measured in its 20-day daily standard deviations -> adapted: a regime on the bar stamped Sunday (coming bar Monday), with the graded vol-scaled return (period 1, vol_period 20) as the signal.
- Comparison: the reversal is larger on Sundays with higher volume -> kept: Sunday volume against its 20-day average is recorded and compared in the criterion.
- Outcome: Monday's move goes against Sunday's move, larger after a larger move, over the next 1 day -> kept.
- Verdict transfer: yes: the test measures Monday's reversal per unit of the scaled Sunday move, and whether it is larger on heavy-volume Sundays, on Sunday-to-Monday bars only.
Forecast: The forecast is non-zero only on the Sunday bar, whose next bar is Monday, as chosen by a weekday regime. On that bar it is minus Sunday's return divided by the 20-day standard deviation of daily returns, standardised against its own past 60 values. It is short after an up Sunday and long after a down Sunday, and it grows linearly with the size of the move up to the cap of 20. On every other day it is 0, so the position is held from Sunday's close to Monday's close only. A second component records Sunday volume against its 20-day average. It has weight 0, so it does not change the forecast; it is there to record the volume for the check.
Config: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: On the Sunday bars (regime mean_reversion), regress Monday's return (close[t+1]/close[t]-1) minus the coin's mean daily return over all windows on the Sunday forecast, pooled over coins and windows. The measure is the slope and its t.
- Supporting check: Split the Sunday bars at the median of `sunday_volume` last_history_value, per coin. Compute the slope from the main measure in each half, and take the high-volume slope minus the low-volume slope, with its t.
- Confirm: The main slope is positive with t >= 2, and the volume difference is positive with t >= 2.
- Reject: The main slope is negative with t <= -2 (Sunday moves continue into Monday), or the volume difference is negative with t <= -2 (reversal weaker on heavy-volume Sundays).
- Inconclusive: Any other result is inconclusive, including slopes or differences near zero with |t| < 2. The test needs at least 300 Sunday cases in total and at least 100 in each volume half.
