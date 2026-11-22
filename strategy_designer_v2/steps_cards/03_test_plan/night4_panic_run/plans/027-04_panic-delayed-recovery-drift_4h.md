---
idea: 027-04_panic-delayed-recovery-drift
brief: 027_panic-days-are-followed-by-a-premium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 3503e22a3698
---
Fidelity:
- Situation: a 24-hour stretch where the range is several times its usual size and the price falls hard -> adapted: the "several times" and "falls hard" thresholds become a graded product of the 24h fall in usual 24h moves and the 24h range in multiples of its 30-day mean.
- Comparison: the later return against the coin's usual return, rising with the panic's extremity -> kept: drift-removed returns, with the position size growing with the panic reading.
- Outcome: price rises from one day after the stretch ends to 14 days after it -> adapted: "after X" becomes "while X", since the component reads the stretch that ended 6 bars earlier and each bet is held 78 bars (13 days).
- Verdict transfer: yes: the forecast is the idea's lagged panic reading, held over the idea's own 1-to-14-day window, so a confirm or reject of the cases carries to the idea.
Forecast: The forecast uses ScaledFallRangeMultipleComponent with period 6, lag 6 and window 180. It reads the 24h stretch that ended 24h ago. Its value is the stretch's fall in usual 24h moves times its 24h range in multiples of the 30-day mean 24h range, and it is 0 when the stretch did not fall. This is standardised against its own past 180 values. It then goes through signed_power with exponent 3 and pivot 20, the strongest dead zone allowed. Ordinary falls stay near 0, and only extreme panics give large long positions. The forecast is never negative (long only), and it grows with the cube of the panic's extremity.
Config: 027-04_panic-delayed-recovery-drift_4h_config.json
Criterion:
- Horizon: 78 bars
- Main measure: A case is a rise of the forecast of at least 2 points, read once per non-overlapping 78-bar grid cell of each window. For each case, take the coin's 78-bar return from the signal bar's close minus the coin's normal 78-bar drift (its mean over all windows). The measure is the mean of this unusual move over all cases, with the t of that mean, before costs.
- Supporting check: Split the cases at the median forecast at the signal bar. The mean unusual move of the upper half minus that of the lower half must be above 0, which tests that more extreme panics are followed by larger gains.
- Confirm: The mean unusual move is positive with t >= 2, and the supporting check passes.
- Reject: The mean unusual move is negative with t <= -2.
- Inconclusive: Any t between -2 and 2, or t >= 2 with the supporting check failing. A result from fewer than 30 cases across all coins and windows is also inconclusive.
