---
idea: 027-01_panic-range-multiple-rebound.b1_panic-rebound-within-a-day
brief: 027_panic-days-are-followed-by-a-premium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 3503e22a3698
---
Fidelity:
- Situation: the coin falls over a 24-hour stretch with a range that is a large multiple of its 30-day average 24h range -> adapted: the on/off "falls" is graded by the fall's depth in usual 24h moves, multiplied by the 24h range in mean 24h ranges over 30 days.
- Comparison: its usual return -> kept: the return is measured against the coin's normal 6-bar drift over all windows.
- Outcome: a higher return over the next 24 hours, rising with the range multiple -> kept: 6-bar forward return, long, scored by position size.
- Verdict transfer: yes: the measured return after graded panic bars, against the usual drift, is exactly the idea's claim.
Forecast: The forecast uses ScaledFallRangeMultipleComponent with period 6, lag 0 and window 180. It is the 24h fall in usual 24h moves times the 24h high-low range in mean 24h ranges over the last 30 days. It is exactly 0 when the last 24h did not fall, so the forecast is never negative. Standardise puts it on the scale of its own past 192 values. Signed_power with exponent 3 and pivot 20 is the strongest graded dead zone: ordinary falls stay near 0, and the position grows steeply with the deepest, widest panics.
Config: 027-01_panic-range-multiple-rebound.b1_panic-rebound-within-a-day_4h_config.json
Criterion:
- Horizon: 6 bars
- Main measure: Each case is a bet, meaning a rise of the forecast of at least 2 points, read once per 6-bar grid cell. For each case, take the coin's 6-bar return from the signal bar's close minus its normal 6-bar drift (all windows), before costs. Measure the mean over cases and its t.
- Supporting check: On the 6-bar grid bars with forecast > 0, regress the excess 6-bar return on the forecast. The slope must be positive (above 0), which tests the claim that a larger multiple gives a higher return.
- Confirm: Mean excess return t >= 2 over at least 30 cases pooled across coins, and the supporting slope is positive.
- Reject: Mean excess return t <= -2 over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is t >= 2 with a slope that is not positive, or fewer than 30 cases.
