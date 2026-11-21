---
idea: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c1_broken-support-below-average
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: e48527ec0eac
---
Fidelity:
- Situation: the daily close sits just below lows where the coin turned up several times in 90 days -> adapted: the threshold "several" becomes graded, using the count of swing lows within 2% of the nearest one above the close, weighted by how near that level is.
- Comparison: the more turning-up lows just above the close, the larger the fall, only while the close is below its 50-day average -> kept: the count sets the size, and a regime rule keeps the idea active only while the close is under its 50-day SMA.
- Outcome: price falls over the next 10 days -> kept: short, with each bet held 10 daily bars.
- Verdict transfer: yes: the forecast measures the cluster of past turning-up lows just above the close, below the 50-day average, and bets short over 10 days, as the idea states.
Forecast: A regime rule turns the idea on only while the close is below its 50-day simple average; on every other bar the forecast is 0. When on, the forecast reads the cluster of past turning-up lows just above the close. It uses SwingHighClusterCountComponent with these settings: pivot "low", level "above", period 90, side 2, band 2%, form "proximity", power 1. Its value is the number of 90-day swing lows within 2% of the lowest swing low at or above the close, times 1/(1+D), where D is the close's percent distance below that level. It is 0 when no swing low sits above the close. The value is standardised against its own past 90 values (average size about 10). It is then passed through signed_power with exponent 2 and pivot 10, so single or distant touches are damped toward 0 and large, near clusters are amplified. Finally it is negated, so the forecast is never positive. It is 0 when there is no cluster above the close, and it grows more negative (a larger short) as the cluster gets bigger and nearer.
Config: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b2_broken-support-ten-day-fall.c1_broken-support-below-average_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Use the non-overlapping 10-bar grid of each window and take the cells whose bar has a forecast of -2 or below. For each such case, compute the short-direction unusual move: -(close[t+10]/close[t] - 1 - the coin's normal 10-bar drift over all its windows). The measure is the t of the mean of these moves over all coins.
- Supporting check: Among the cases, the mean short-direction unusual move of those with |forecast| above the cases' median, minus that of those at or below it, must be above 0.
- Confirm: The main-measure t is 2 or more over at least 30 cases, and the supporting check is above 0.
- Reject: The main-measure t is -2 or less over at least 30 cases.
- Inconclusive: A t between -2 and 2. A t of 2 or more with the supporting check at or below 0. Fewer than 30 cases.
