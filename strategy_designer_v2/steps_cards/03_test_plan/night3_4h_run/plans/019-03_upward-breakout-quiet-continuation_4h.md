---
idea: 019-03_upward-breakout-quiet-continuation
brief: 019_quiet-range-then-breakout-on-four-hour-bars
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: ad5059559106
---
Fidelity:
- Situation: a 4h bar closes above the highest high of the preceding two-day stretch -> adapted: graded by how far the close sits above that high (zero at or below it), over the prior 12 bars.
- Comparison: the stretch's narrowness against the coin's 30-day average 4h range -> kept: the mean bar range over 180 bars divided by the 12-bar stretch's range multiplies the reading.
- Outcome: the coin rises over the next three days, more after narrower stretches -> kept: long, held 18 bars.
- Verdict transfer: yes: the component measures the breakout above the prior two-day high, weighted by narrowness against the 30-day average range, and the book holds each bet for the three-day horizon.
Forecast: The forecast uses NarrowRangeBreakoutComponent with period 12 (two days) and base_period 180 (30 days). On each bar it gives max(0, close − H) / close × 100 × B / S. H is the highest high of the prior 12 bars and S is their range. B is the mean 4h bar range over the last 180 bars. It is zero whenever the close is at or below the prior two-day high. It is positive only on a close above that high. It grows with the size of the break and with how narrow the stretch was against the 30-day average range. It is standardised against its own past 180 values, then put through signed_power with exponent 3 and pivot 10. This is the strongest graded dead zone, because the breakout is a rare event: small breaks out of ordinary stretches stay near zero, and large breaks out of very narrow stretches are amplified. The forecast is never negative (long only by construction), and each bet is held 18 bars.
Config: 019-03_upward-breakout-quiet-continuation_4h_config.json
Criterion:
- Horizon: 18 bars
- Main measure: Cases are bets: rises of the forecast of at least 2 points, read once per 18-bar grid cell of each window. For each case, take the coin's 18-bar return from the close of the signal bar, minus the coin's normal 18-bar drift (its mean over non-overlapping 18-bar stretches of all its windows). Measure the mean of this excess return over all coins and windows, with the t of that mean. This is before costs.
- Supporting check: Split the cases at the median forecast of their signal bars (larger = narrower stretch and bigger break). The mean excess 18-bar return of the upper half minus that of the lower half must be above 0.
- Confirm: The mean excess return is positive with t ≥ 2, and the supporting check passes (upper half minus lower half > 0).
- Reject: The mean excess return is negative with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. A t ≥ 2 with the supporting check failing is also inconclusive. So is any result with fewer than 30 independent cases across all coins and windows.
