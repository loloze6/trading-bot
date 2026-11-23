---
idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d1_heavy-weekend-extends-week
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: fc27df6a23f8
---
Fidelity:
- Situation: a Saturday-Sunday move on higher volume than the mean of the preceding five weekdays -> kept: at the close of Sunday 23:00, the 48-bar return and the mean hourly volume of the last 48 bars against the mean of bars t-167..t-48.
- Comparison: the weekend move extends the coin's own move over those five weekdays, and it is larger with a larger weekend move, heavier weekend volume and a larger same-direction five-day move -> kept: a regime rule requires the same sign for the 48-bar return and the lagged 120-bar return, and the forecast grows with each factor.
- Outcome: the price continues in the weekend move's direction over the next 48 hours -> kept: each bet is held for 48 bars and judged on the 48-bar return.
- Verdict transfer: yes: the cases, conditions, direction and horizon are those the idea states, so a confirm or reject of this test is a confirm or reject of the idea.
Forecast: The forecast is active only on the bar closing at Monday 00:00 UTC, the end of the weekend, and only if three conditions hold. The weekend 48-bar return and the prior five-weekday return (the 120-bar return ending 48 bars ago) must have the same sign. The weekend mean hourly volume must be above the mean of the 120 weekday bars before it. On that bar the forecast is the equal-weight mean of two standardised components, so both share the weekend move's sign. The first is the weekend 48-bar return in usual 48-bar moves (30-day mean), multiplied by the weekend-over-weekday volume ratio. The second is the prior five-weekday return in usual moves, based on the 20-bar return volatility. The forecast is positive after a heavy up-weekend that extends an up-week and negative after a heavy down-weekend that extends a down-week. It grows with the weekend move, with the volume ratio and with the prior week's move. On every other bar, and when a condition fails, it is 0. The bet is held for 48 bars.
Config: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d1_heavy-weekend-extends-week_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: A case is a Monday 00:00 bar with a non-zero forecast; cases are one per week per coin, so they do not overlap. For each case, take the coin's 48-bar return from that close, minus the coin's mean 48-bar return over all windows, signed by the forecast. Measure the mean of this over all coins and cases, with its t.
- Supporting check: Across the cases, the Spearman rank correlation between abs(forecast) and the signed excess 48-bar return must be above 0.
- Confirm: The mean signed excess return is above 0 with t ≥ 2, and the supporting rank correlation is above 0.
- Reject: The mean signed excess return is below 0 with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is a confirming main measure whose rank correlation is not above 0. The test also needs at least 100 cases over all coins and windows; with fewer it is inconclusive.
