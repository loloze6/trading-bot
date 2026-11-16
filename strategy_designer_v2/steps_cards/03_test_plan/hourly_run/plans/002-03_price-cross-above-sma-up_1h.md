---
idea: 002-03_price-cross-above-sma-up
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC/USDT
data-bar: 1h
data-period: fold A
outcome: plan
fit: adapted
---
Fidelity:
- Situation: close above the long average after being below it -> adapted: "after the up-cross" made "while above the 200-bar SMA", graded by percent distance above it.
- Comparison: rises more often and further than after random points -> kept: forward returns are compared with the coin's unconditional forward return at all bars.
- Outcome: price keeps rising over the following bars -> kept: the forward 24-bar return, long side.
- Verdict transfer: yes: being above the long average is the state that an up-cross begins, and this is the guide's allowed "after X" to "while X" change, so a pass or a fail carries over to the idea.
Forecast: Take the percent distance of the close from its 200-bar simple moving average, which includes the current close. Standardise it against its own previous 200 values (target 10, cap 20). Clip it at 0. The forecast is zero while price is at or below the SMA200, so the position is flat. Once the close crosses above, the forecast turns positive and grows with the distance above the average, so the long position grows with it up to the cap. There is no short side, because the idea concerns only up-crosses.
Config: 002-03_price-cross-above-sma-up_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The slope (t-stat) of the next 24-bar coin return, minus that window's mean 24-bar return, regressed on the forecast. Sample at non-overlapping 24-bar steps and pool the 6 windows. This judges the idea before costs and against simply holding the coin.
- Supporting check: Among sampled bars with forecast > 0, the share with a positive forward 24-bar return, compared with the share at all sampled bars (two-proportion z).
- Confirm: The slope is positive with t ≥ 2.
- Reject: The slope is negative with t ≤ -2, meaning moves after price goes above the average tend to reverse. A slope with t between -2 and 2 does not reject.
- Inconclusive: Any t between -2 and 2. The result is also inconclusive with fewer than 150 non-overlapping sampled cases with forecast > 0 pooled, or fewer than 3 of the 6 windows containing such cases.
