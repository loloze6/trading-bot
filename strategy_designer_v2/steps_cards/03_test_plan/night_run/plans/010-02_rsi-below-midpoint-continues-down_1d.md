---
idea: 010-02_rsi-below-midpoint-continues-down
brief: 010_rsi-midline-regime-direction
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 791f9c660ae8
---
Fidelity:
- Situation: share of the past 14 days that the 14-day RSI spent below its midpoint -> kept
- Comparison: a larger share against a smaller share, graded across the share -> kept
- Outcome: a larger fall over the next 7 days -> kept
- Verdict transfer: yes: the forecast is the 14-day below-midpoint share of RSI(14), and it is judged on the next 7 daily bars' return.
Forecast: The forecast uses one indicator, RsiAboveMidlineShareComponent, with period 14, window 14, side "below" and rsi_window 100. It gives the share of the last 14 daily bars on which RSI(14) was below 50, minus 0.5. That value is standardised over its past 60 values (min_periods 20) and then negated. The forecast is short when RSI spent more than half of the 14 days below 50, and the short grows as that share rises, up to 14 of 14 days. It is long when the share is under half, and grows to the full long size at 0 of 14 days. It is zero at exactly 7 of 14 days. The share moves in steps of 1/14, which is 15 levels, so the forecast is graded. The forecast is active on every bar, with no regime.
Config: 010-02_rsi-below-midpoint-continues-down_1d_config.json
Criterion:
- Horizon: 7 bars
- Main measure: The 7-bar forward excess return regressed on the recorded forecast, pooled over coins and windows. - Excess return: close[t+7]/close[t] - 1, minus that coin's mean 7-bar return over all its windows. - Samples: non-overlapping bars at positions 0, 7, 14, … of each window. - Result: the t-statistic of the slope.
- Supporting check: The book's mean daily timing gain must be above 0 before costs. The timing gain is the book's mean daily return minus its gain from the market's own rise.
- Confirm: The idea is confirmed when both hold: - the slope's t is 2 or more, so a larger below-midpoint share is followed by a larger excess fall; - the timing gain is positive.
- Reject: The idea is rejected when the slope's t is -2 or less, meaning a larger below-midpoint share is followed by a larger excess rise.
- Inconclusive: A slope t between -2 and +2 is inconclusive. So is a t of 2 or more with a timing gain of 0 or below. The test needs at least 300 non-overlapping cases pooled over the three coins; about 1,200 are expected.
