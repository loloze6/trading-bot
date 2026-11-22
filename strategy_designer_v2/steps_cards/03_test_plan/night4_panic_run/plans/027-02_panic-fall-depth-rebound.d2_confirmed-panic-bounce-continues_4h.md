---
idea: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues
brief: 027_panic-days-are-followed-by-a-premium
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 4h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 3503e22a3698
---
Fidelity:
- Situation: a 24-hour stretch whose range is several times its 30-day average and in which the coin fell, ending 24 hours ago -> adapted: a regime rule on ScaledFallRangeMultipleComponent (6-bar stretch, lag 6, 180-bar base), which reads the fall and the range multiple as one product above 3, held while that stretch is the one 24 hours back.
- Comparison: the size of the coin's rise over the 24 hours after the stretch, larger against smaller -> kept: the 6-bar return, graded, inside the panic regime.
- Outcome: a higher return over the following 14 days, rising with the size of the bounce -> kept: the 84-bar forward return against the coin's normal drift.
- Verdict transfer: yes: the test measures whether, after qualifying panic stretches, a larger 24-hour bounce is followed by a larger 14-day excess return.
Forecast: The forecast is active only on bars where the 6-bar stretch that ended 6 bars ago both fell and had a large range. The rule requires its fall, counted in usual 6-bar moves, times its range, counted in multiples of the 30-day mean 6-bar range, to be at least 3. On those bars the forecast is the coin's 6-bar (24h) percent return, standardised against its own past 60 values. It is positive and larger the stronger the bounce since the panic, and negative when the coin kept falling. It is zero (flat) on every bar outside the panic regime.
Config: 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues_4h_config.json
Criterion:
- Horizon: 84 bars
- Main measure: On the cases (bets in the panic regime, one per 84-bar grid cell of each window), the slope of the coin's 84-bar forward return minus its normal drift, regressed on the forecast at the case bar.
- Supporting check: The mean excess 84-bar return (return minus normal drift) of the cases with positive forecast is above 0.
- Confirm: The slope is positive with t >= 2 over at least 30 independent cases, and the supporting check's mean is above 0.
- Reject: The slope is negative with t <= -2 over at least 30 independent cases.
- Inconclusive: Any slope with t between -2 and 2 is inconclusive, and so is a confirming slope whose supporting check fails. Any result from fewer than 30 independent cases is also inconclusive.
