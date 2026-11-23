---
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.d2_sunday-falls-rebound-early-week
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: fc27df6a23f8
---
Fidelity:
- Situation: a coin's fall over Sunday's 24 hours, against its usual 30-day move, in a volatile coin -> adapted: graded long-only reading at Sunday's last close, the Sunday 24h fall in usual 24h moves over 720 bars times the 720-bar hourly volatility, with no on/off threshold.
- Comparison: the usual 30-day move, and a larger rise the higher the 30-day hourly volatility -> kept.
- Outcome: a rise over the next 48 hours (Monday and Tuesday) -> kept.
- Verdict transfer: yes: the forecast exists only at Sunday's close, sized by the scaled fall times the volatility, and it is held exactly the 48 hours the idea names.
Forecast: The forecast is computed only on the bar whose close ends Sunday. That is the 23:00 UTC Sunday bar, whose coming bar starts Monday 00:00. A calendar regime selects it; every other bar is flat. On that bar the forecast reads `MeanAbsScaledReturnTimesVolatilityComponent` with period 24, window 720 and vol_period 720. This is Sunday's 24h return, divided by the mean absolute 24h return over the last 30 days, times the 30-day standard deviation of hourly returns. The value is standardised over its past 500 hourly values, negated and clipped at 0. So the forecast is positive after a falling Sunday. It grows with the depth of the fall in usual moves and with the coin's volatility. It is 0 after a rising or flat Sunday, so the forecast is long only. The bet is held 48 bars, through Tuesday.
Config: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.d2_sunday-falls-rebound-early-week_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: The cases are the Sunday-close bars with forecast >= 2. For each case, take the coin's 48h return from that close, minus the coin's normal 48h drift (its mean 48h return on non-overlapping stretches of all windows). Report the mean of this excess over the cases and its ordinary t. The cases are a week apart, so they do not overlap.
- Supporting check: The correlation between the forecast and the 48h excess return, over the same cases, is above 0.
- Confirm: The mean excess 48h return has t >= 2 and the supporting correlation is above 0.
- Reject: The mean excess 48h return has t <= -2.
- Inconclusive: A t between -2 and 2 is inconclusive. So is a t >= 2 with a correlation at or below 0. Fewer than 100 cases over all coins and windows is inconclusive whatever the t.
