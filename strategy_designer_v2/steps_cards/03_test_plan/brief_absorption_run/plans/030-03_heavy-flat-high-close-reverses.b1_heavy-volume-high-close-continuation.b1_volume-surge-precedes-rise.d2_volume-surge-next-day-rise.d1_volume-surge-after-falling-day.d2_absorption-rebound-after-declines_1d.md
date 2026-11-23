---
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d2_absorption-rebound-after-declines
brief: 030_absorption-day-close-location
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: bc0cb550291c
---
Fidelity:
- Situation: a down day, heavier volume and a larger fall, after a 20-day decline -> kept: the day's fall (in usual daily moves) x volume ratio x prior 20-day decline, 0 on up days.
- Comparison: volume against its own prior 20-day average -> kept: the day's volume over the mean of the 20 days before it.
- Outcome: the coin rises over the next day, more so the stronger the situation -> kept: next-bar return, horizon 1 bar.
- Verdict transfer: yes: the forecast is the idea's own product of fall, relative volume and prior decline, held for its one-day horizon.
Forecast: `FallVolumeTimesPriorDeclineComponent` with vol_period 20, volume_period 20 and decline_period 20, ungated. It multiplies three parts: the day's fall in units of the 20-day return standard deviation, the day's volume over its prior 20-day mean, and the percent decline over the 20 days ending yesterday. It is then standardised over 60 bars (min 20). The forecast is 0 on up days and on days without a prior 20-day decline, and positive (long) otherwise. It grows with each of the three parts. It is never negative.
Config: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d2_absorption-rebound-after-declines_1d_config.json
Criterion:
- Horizon: 1 bars
- Main measure: The slope of the next-bar return on the forecast, pooled over all coins, windows and bars. The next-bar return is close[t+1]/close[t]-1 minus that coin's mean daily return over all its windows. Its t is reported with the count of bars.
- Supporting check: The mean next-bar excess return (as above) on bars with forecast > 0 is positive.
- Confirm: The slope has t >= 2 and the mean excess return on forecast > 0 bars is above 0.
- Reject: The slope has t <= -2.
- Inconclusive: A slope t between -2 and 2 is inconclusive. So is a slope t >= 2 with a mean excess return on forecast > 0 bars at or below 0. Fewer than 100 bars with forecast > 0 is inconclusive whatever the t.
