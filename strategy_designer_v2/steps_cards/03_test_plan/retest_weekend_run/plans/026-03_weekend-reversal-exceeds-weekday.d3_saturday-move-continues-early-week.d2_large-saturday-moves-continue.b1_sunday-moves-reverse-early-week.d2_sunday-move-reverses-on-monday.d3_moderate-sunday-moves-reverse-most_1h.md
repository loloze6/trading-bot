---
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.d3_moderate-sunday-moves-reverse-most
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: fc27df6a23f8
---
Fidelity:
- Situation: a coin's 24-hour return over Sunday, up to about two usual moves, times its 30-day hourly volatility -> kept: the 24-bar return capped at 2 usual moves times the 720-bar return std, read at Sunday's last bar.
- Comparison: against the coin's usual 30-day move -> kept: the return is divided by the mean absolute 24-bar return over 720 bars.
- Outcome: an opposite move over the next 48 hours that grows with that product -> kept: a negated graded position, held 48 bars.
- Verdict transfer: yes: the test sizes the lean against Sunday's move exactly as the idea states and judges the 48-hour move that follows.
Forecast: The forecast is active only on the bar whose close ends Sunday UTC. That is the bar for which the coming bar is Monday 00:00. A regime rule selects it with WeekdayComponent = 0 and HourOfDayComponent = 0. On that bar the forecast is minus the standardised value of MeanAbsScaledReturnTimesVolatilityComponent, with period 24, window 720, vol_period 720 and cap 2. That value is Sunday's 24h return in usual 30-day 24h moves, clipped at ±2 usual moves, times the 30-day hourly return std. It is standardised against its last 500 hourly values, then negated. After an up Sunday the forecast is negative, after a down Sunday it is positive, and it is near 0 after a flat Sunday. Its size grows linearly with the scaled move up to two usual moves, then only with volatility. On every other bar the forecast is 0. The bet made on Sunday's last bar is held for 48 bars.
Config: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.d3_moderate-sunday-moves-reverse-most_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: The cases are the Sunday-close bars with a nonzero forecast. For each case, take the coin's 48-bar return from that bar's close, minus the coin's normal 48-bar drift over all its windows. Regress that excess return on the bar's forecast, pooling coins and windows. The cases are one per week, so they do not overlap. The measure is the slope's t.
- Supporting check: The mean unusual move over the cases is above 0, taken in the forecast's direction and before costs.
- Confirm: The slope's t is +2 or more, and the mean signed unusual move is above 0.
- Reject: The slope's t is -2 or less, meaning the moves follow Sunday's direction in proportion to the forecast.
- Inconclusive: A slope t strictly between -2 and +2 is inconclusive. So is a t of +2 or more with a mean signed unusual move at or below 0. At least 300 cases are needed in total, with at least 30 per coin.
