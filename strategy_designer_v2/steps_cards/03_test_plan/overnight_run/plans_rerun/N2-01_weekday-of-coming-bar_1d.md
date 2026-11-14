---
idea: N2-01_weekday-of-coming-bar
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: the coming daily bar is the Saturday session, the one after a Friday-dated bar -> adapted: the Saturday condition is kept as a regime, and the long is sized by the coin's past Saturday excess return so that it is graded
- Comparison: Saturday return against the coin's average day -> kept: WeekdayReturnComponent subtracts the mean of all past bar returns from the mean of past Saturday returns
- Outcome: the Saturday bar returns more than the coin's average day, so long pays -> kept: Saturday bar returns are measured against the coin's mean daily return
- Verdict transfer: yes: the position is long only on Saturday bars, so its excess over holding is the Saturday premium the idea claims.
Forecast: A WeekdayComponent rule puts the bar in the `mean_reversion` regime only when the coming bar is a Saturday (weekday 5). Every other bar is `unknown`, which is null, so the forecast is 0 and the position is flat. In the Saturday regime the forecast is WeekdayReturnComponent with lookback_bars 182, the library default and about 26 Saturdays. This is the mean of past Saturday returns minus the mean of all past returns, standardised (window 182, min_periods 45) and then clipped at 0. The forecast is positive and grows with how much the coin's past Saturdays beat its average day. It is zero when past Saturdays did not beat the average day, and it is never short. The position opens at the Friday bar's close and closes at the Saturday bar's close.
Config: N2-01_weekday-of-coming-bar_1d_config.json
Criterion:
- Horizon: 1 bar
- Main measure: Take every bar where the forecast is above 0. For each one, compute allocation × (next-bar return minus the coin's mean daily return over all 24 windows together). Report the mean of these values with its t-statistic. Each case is a single non-overlapping bar.
- Supporting check: Over all Saturday bars, whatever the forecast, compute the mean Saturday return minus the coin's all-window mean daily return, with its t-statistic.
- Confirm: The main-measure mean is positive with t ≥ 2, pooled over the coins.
- Reject: The main-measure mean is negative with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive, including an estimate near zero. At least 300 active Saturday bars are required, pooled over coins and windows; with fewer, the result is inconclusive.
