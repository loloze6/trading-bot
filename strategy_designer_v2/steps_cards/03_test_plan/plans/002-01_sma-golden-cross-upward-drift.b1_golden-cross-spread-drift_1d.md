---
idea: 002-01_sma-golden-cross-upward-drift.b1_golden-cross-spread-drift
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
---
Fidelity:
- Situation: the 50-day SMA is above the 200-day SMA, with a wider percent spread counting as stronger -> kept
- Comparison: the next 10-day rise compared with the coin's usual 10-day return -> kept
- Outcome: the coin rises more over the next 10 days as the spread widens -> kept
- Verdict transfer: yes: the forecast is the positive part of the percent spread between the 50-day and 200-day SMAs, tested on 10-day returns in excess of the coin's usual 10-day return.
Forecast: The forecast starts from the percent spread between the 50-day and 200-day simple moving averages of the close, (SMA50 - SMA200) / SMA200 x 100. It is standardised against its own past 200 values, so a typical spread size gives 10, capped at 20. It is then clipped at 0. It is zero while SMA50 is at or below SMA200, which makes it long-only. It is positive while SMA50 is above SMA200 and grows in proportion to the width of the spread. There is no regime: the clip makes the "while above" condition graded, starting from zero at the cross.
Config: 002-01_sma-golden-cross-upward-drift.b1_golden-cross-spread-drift_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: The cases are the bars where the forecast is above 0, taken on the non-overlapping 10-bar grid of each window and pooled over coins and windows. On these cases, regress the excess 10-day return (close[t+10] / close[t] - 1 minus that coin's mean 10-bar return over all its windows) on the forecast at t. Report the slope's t-statistic.
- Supporting check: The forecast-weighted mean of the excess 10-day return on those same cases must be above 0.
- Confirm: The slope's t is 2 or more and the forecast-weighted mean excess return is above 0.
- Reject: The slope's t is -2 or less.
- Inconclusive: A slope t between -2 and 2, or a t of 2 or more with a forecast-weighted mean excess return of 0 or less, is inconclusive. Fewer than 100 positive-forecast grid cases is also inconclusive.
