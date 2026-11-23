---
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets
brief: 026_weekend-moves-reverse-in-the-week
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: the coin's 24-hour return over Saturday, larger the bigger the move -> kept: the return from Saturday 00:00 to Sunday 00:00 UTC, read at the decision bar before Monday opens.
- Comparison: only while 30-day hourly volatility is low against its past year, and the calmer the coin, the larger -> kept: a regime gate on 30-day volatility against its yearly mean, and Saturday's move divided by the 30-day volatility.
- Outcome: a same-direction move over Monday and Tuesday -> kept: the bet is made at Monday's open and held 48 bars.
- Verdict transfer: yes: the forecast bets on exactly Saturday's move, only in calm regimes, scaled by calmness, over exactly Monday and Tuesday.
Forecast: The forecast is non-zero on one bar only: the close of the Sunday 23:00 bar, whose next bar opens Monday 00:00 UTC. It is also non-zero only when the coin's 720-bar volatility of hourly returns is at or below its 8760-bar (one-year) mean. On that bar it is Saturday's 24-hour return, close[t-24] / close[t-48] - 1. That return is divided by the standard deviation of the 720 hourly returns ending at Saturday's close, times sqrt(24). The result is standardised over its last 500 hourly values (target 10, cap 20). This equals Saturday's move in the coin's yearly usual moves times the calmness ratio (yearly volatility over current volatility). So the forecast grows with both. It is positive after an up Saturday and negative after a down Saturday, and 0 on every other bar. The bet is held 48 bars, through Monday and Tuesday.
Config: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets_1h_config.json
Criterion:
- Horizon: 48 bars
- Main measure: The cases are the bars with a non-zero forecast. On each case, take the coin's 48-bar return from that bar's close and subtract the coin's normal 48-bar drift (its mean on the non-overlapping 48-bar grid of all its windows). Then take the mean over the cases of (forecast / 10) x that de-drifted return, and its t.
- Supporting check: Split the cases at the median of abs(forecast). In each half, take the de-drifted return in the forecast's direction. The upper half's mean minus the lower half's must be above 0.
- Confirm: The main mean is positive with t >= 2 over at least 100 cases, and the supporting check is positive.
- Reject: The main mean is negative with t <= -2 over at least 100 cases.
- Inconclusive: Any t between -2 and 2. A t >= 2 whose supporting check is not positive. Fewer than 100 cases.
