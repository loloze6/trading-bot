---
idea: 025-03_bounce-falling-versus-rising-regime
brief: 025_bounces-fade-in-falling-markets
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: a one-day rise of several usual daily moves -> adapted: the rise threshold is made graded, as the day's return in usual 20-day moves, damped by a cube below the pivot.
- Comparison: 90-day return negative versus positive -> kept: a regime rule on the sign of the 90-bar return.
- Outcome: the 5-day return is lower in the falling case, and the gap widens with the rise -> kept: each rise is held 5 bars, short when the 90-day return is negative, long when positive, sized by the rise.
- Verdict transfer: yes: the book bets the 5-day difference between the two 90-day states, sized by the rise, so its result is the idea's result.
Forecast: The rise is the day's return divided by the standard deviation of the last 20 daily returns. It is standardised over 60 bars and clipped at 0, so down days give 0. A cube with pivot 10 then keeps ordinary up days near 0 and makes rises of several usual moves large. When the 90-day return is 0 or above, the forecast is this value, long. When it is below 0, the forecast is the same value negated, short. It is 0 on down days and during warm-up. Its size grows with the size of the rise, so the long/short gap grows with the rise.
Config: 025-03_bounce-falling-versus-rising-regime_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Cases are bets, read once per 5-bar grid cell of each window. For each case, take the coin's 5-day return from the signal bar minus the coin's normal 5-day drift. Measure the mean of this excess return for long cases (90-day return >= 0) minus the mean for short cases (90-day return < 0), with Welch's t.
- Supporting check: Split the cases at the median |forecast|. The gap (long-case mean minus short-case mean) in the larger half must exceed the gap in the smaller half.
- Confirm: The difference is positive with Welch t >= 2, and the supporting check passes.
- Reject: The difference is negative with Welch t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a t >= 2 where the larger-half gap does not exceed the smaller-half gap. A result is also inconclusive if either group has fewer than 30 cases.
