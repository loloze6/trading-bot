---
idea: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.e1_vol-scaled-20-day-high-breakout
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: e48527ec0eac
---
Fidelity:
- Situation: daily close above its highest close of the prior 20 days, in units of 20-day daily volatility -> kept: VolatilityScaledDistanceFromHighComponent (period 20, vol_period 20), clipped at 0.
- Comparison: farther clearances against smaller ones -> kept: the forecast's size grows with the clearance.
- Outcome: the coin rises more over the next 10 days -> kept: each bet is held 10 daily bars.
- Verdict transfer: yes: the forecast is the idea's own measure, held for its horizon, so a confirm or reject of its graded gain is a confirm or reject of the idea.
Forecast: Each day the forecast takes the close's distance above the highest close of the 20 days before it, divided by the standard deviation of the last 20 daily returns. That value is standardised against its own past 60 values, so an average-sized reading is about 10, capped at 20. It is then clipped at 0. The forecast is zero while the close is at or below the prior 20-day high. It is positive and grows linearly with the clearance once the close is above that high. It is never negative.
Config: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.e1_vol-scaled-20-day-high-breakout_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Take the cases, one per 10-bar grid cell of each window, a case being a rise of the forecast of at least 2 points. For each case, compute the coin's 10-bar return from the signal bar's close minus the coin's normal 10-bar drift, measured over all windows. Regress that excess return on the signal bar's forecast, pooled over coins and windows, and use the slope's t.
- Supporting check: The mean excess 10-bar return over all cases is above 0.
- Confirm: Confirmed when the slope's t is 2 or more and the mean excess return of the cases is above 0, before costs.
- Reject: Rejected when the slope's t is -2 or less: larger clearances are followed by smaller excess rises.
- Inconclusive: Any slope t between -2 and 2 is inconclusive. So is a slope t of 2 or more with a mean excess return at or below 0. Fewer than 100 cases pooled over all coins and windows is also inconclusive.
