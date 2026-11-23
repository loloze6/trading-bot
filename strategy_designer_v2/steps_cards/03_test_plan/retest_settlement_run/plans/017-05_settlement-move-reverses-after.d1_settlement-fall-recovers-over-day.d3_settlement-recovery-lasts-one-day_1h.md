---
idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d3_settlement-recovery-lasts-one-day
brief: 017_funding-settlement-clock-pressure
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a 00:00 or 16:00 UTC funding settlement, with a fall over the 2 hours before it -> kept: the settlement bar is the regime, and the 2-bar return is read at that bar's close.
- Comparison: the fall's size against the coin's usual 2-hour move -> kept: the 2-bar return is divided by its mean absolute value over the last 720 bars.
- Outcome: the price rises over the next 24 hours, more after a larger fall, and the effect is gone by the second day -> kept: a 24-bar hold, with the second day checked separately.
- Verdict transfer: yes: the test measures the scaled pre-settlement fall at exactly those clock times, and the following day's and second day's returns.
Forecast: The forecast is active only on the bar whose close is a 00:00 or 16:00 UTC settlement. This uses HourOfDayComponent on the coming bar's hour, 0 or 16, as a regime rule. On every other bar it is 0, and each bet is held for 24 bars. On a settlement bar it is the 2-bar return in multiples of the mean absolute 2-bar return over 720 bars (MeanAbsScaledReturnComponent, period 2, window 720). That value is standardised over 500 bars, negated and clipped at 0. The forecast is positive after a fall into settlement and grows linearly with the fall's depth in usual moves. It is 0 after a rise, and it never goes short.
Config: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d3_settlement-recovery-lasts-one-day_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The cases are settlement bars (regime mean_reversion), taking the first one in each non-overlapping 24-bar grid cell of each window, pooled over coins and windows. Each case's 24-bar forward return, minus the coin's normal 24-bar drift, is regressed on its forecast. The measure is the slope's t.
- Supporting check: Run the same regression for the second day's return (close[t+48] / close[t+24] - 1, minus the drift) on the same cases. It passes when that slope's t is below 2.
- Confirm: The main slope is positive with t >= 2, over at least 200 cases with forecast > 0, and the second-day check passes.
- Reject: The main slope is negative with t <= -2, over at least 200 cases with forecast > 0.
- Inconclusive: Any main t between -2 and 2 is inconclusive. So is a main t >= 2 with a second-day t >= 2. So is any result with fewer than 200 cases with forecast > 0.
