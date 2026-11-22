---
idea: 026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 08ec5a873928
---
Fidelity:
- Situation: a coin's 24-hour return over Sunday -> kept: the 24-bar return at the close of Sunday's last hourly bar (Monday 00:00 UTC), read only on that bar.
- Comparison: the larger Sunday's move, the larger the opposite move -> kept: the forecast grows with the size of Sunday's return.
- Outcome: an opposite move over the next 24 hours -> kept: the position is the fade of Sunday's return, held 24 bars.
- Verdict transfer: yes: the test measures Sunday's return, fades it in proportion to its size, and judges the next 24 hours as the idea states.
Forecast: The regime detector selects one bar a week: the bar whose close is Monday 00:00 UTC (the coming bar is weekday 0, hour 0). On that bar the forecast is the negated, standardised 24-bar percent return (PriceEvolutionOnPeriodComponent, comparison_period 24), which is Sunday's return. Standardise uses window 60 and min_periods 20, the convention for a 24-bar lookback. The forecast is short after a Sunday rise and long after a Sunday fall, and it grows linearly with the size of Sunday's move. On every other bar the forecast is 0, and the holding period keeps each Monday bet for 24 bars.
Config: 026-03_weekend-reversal-exceeds-weekday.d2_sunday-move-fades-monday_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: The slope of the next-24-bar return from the Monday 00:00 close, minus the coin's normal 24-bar drift, regressed on that bar's forecast. Cases are taken once per week per coin and window (non-overlapping), pooled over coins and windows. The t of the slope is reported with the case count.
- Supporting check: The mean over the cases of sign(forecast) × (the next-24-bar return minus the drift) is above 0.
- Confirm: The slope is positive with t ≥ 2 and the supporting mean is above 0.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: Any slope with t between -2 and 2 is inconclusive, as is a confirming slope whose supporting mean is not above 0. Fewer than 300 Monday cases with a nonzero forecast is also inconclusive, whatever the t.
