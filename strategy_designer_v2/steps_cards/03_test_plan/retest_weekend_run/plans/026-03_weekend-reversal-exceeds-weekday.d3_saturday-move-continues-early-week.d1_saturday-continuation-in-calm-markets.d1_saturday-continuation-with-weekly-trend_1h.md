---
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d1_saturday-continuation-with-weekly-trend
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: a coin's 24-hour return over Saturday, in calm markets (30-day hourly volatility low against its past year) -> adapted: Saturday's return is read at Monday 00:00 with a 24-bar lag, scaled by 30-day hourly volatility; the calm-market condition is kept as a regime rule (percentile at or below the median of the past year).
- Comparison: the coin's 7-day return pointing the same way as Saturday's move -> adapted: agreement is a regime condition (stand aside otherwise, as the consequence says), and its degree is graded by adding the 7-day return.
- Outcome: a move in Saturday's direction over Monday and Tuesday, growing with Saturday's size -> kept: the position is entered at Monday 00:00 and held 48 bars.
- Verdict transfer: yes: the agreeing, calm weeks are where the idea predicts its strongest continuation, so a confirm or a reject there carries to the idea.
Forecast: The forecast is built only on the bar whose next bar starts Monday 00:00 UTC, and only when four conditions hold. The 30-day volatility percentile over the past year must be at most 0.5, and Saturday's return and the 7-day return must have the same sign. On that bar the forecast is the equal-weight mean of two standardised values. The first is Saturday's 24-hour return (close[t-24] / close[t-48] - 1) divided by the 720-bar standard deviation of hourly returns. The second is the 168-bar percent return. The forecast is positive after an up Saturday in an up week and negative after a down Saturday in a down week. It grows with both moves, and it is 0 on every other bar. The bet is then held for 48 bars, through Monday and Tuesday.
Config: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d1_saturday-continuation-with-weekly-trend_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: On each entry bar (forecast not 0), compute the coin's 48-bar return minus that coin's mean 48-bar return over all its windows (non-overlapping stretches). Regress this excess return on the entry forecast, pooled over coins and windows, and read the t of the slope.
- Supporting check: The mean over cases of the excess 48-bar return in the forecast's direction must be above 0.
- Confirm: Confirmed when the slope's t is 2 or more with at least 100 cases, and the mean directional excess return is above 0.
- Reject: Rejected when the slope's t is -2 or less with at least 100 cases.
- Inconclusive: Any slope t between -2 and 2 is inconclusive. So is a slope t of 2 or more when the mean directional excess return is 0 or below. So is any result from fewer than 100 entry cases.
