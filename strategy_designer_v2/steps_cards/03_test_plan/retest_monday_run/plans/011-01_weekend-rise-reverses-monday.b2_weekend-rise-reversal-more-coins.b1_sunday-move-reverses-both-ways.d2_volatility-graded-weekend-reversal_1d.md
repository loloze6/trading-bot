---
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d2_volatility-graded-weekend-reversal
brief: 011_weekend-moves-reverse-weekday
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 453ddf5ae165
---
Fidelity:
- Situation: the coin's Saturday-to-Sunday close-to-close return, read at Sunday's close -> adapted: on/off "moved" made graded, as the Sunday bar's return used only on Sunday bars through a calendar regime.
- Comparison: the 20-day daily volatility against the 60-day daily volatility -> kept: the 20-return std over the 60-return std, both ending at Sunday's close, scales the bet.
- Outcome: the price moves against the weekend move over Monday and Tuesday, more so as the ratio rises -> kept: the bet is held 2 daily bars from Sunday's close.
- Verdict transfer: yes: the bet is placed at each Sunday close, against the weekend move, sized by the volatility ratio, and held exactly over Monday and Tuesday.
Forecast: The regime is active only on Sunday bars, when the coming bar is a Monday (WeekdayComponent reads 0). On those bars the forecast is minus the Sunday bar's return x 100 x (std of the last 20 daily returns / std of the last 60 daily returns), standardised over its own past 60 values (min 20). The forecast is positive after a weekend fall and negative after a weekend rise. Its size grows with the size of the weekend move and with how far 20-day volatility sits above 60-day volatility. It is zero on every other weekday. The book holds the Sunday bet for 2 bars, Monday and Tuesday.
Config: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.d2_volatility-graded-weekend-reversal_1d_config.json
Criterion:
- Horizon: 2 bars
- Main measure: Use every Sunday bar with a nonzero forecast as one case; the cases do not overlap. For each case, take the coin's return from Sunday's close to Tuesday's close, minus the coin's mean 2-day return over all its windows (holding the coin), times the sign of the forecast. Compute the mean of this signed excess return over the cases and its t, before costs.
- Supporting check: Across the cases, regress the signed excess 2-day return on s20/s60. Recompute s20/s60 from the closes as the std of the last 20 over the last 60 daily returns at Sunday's close. The slope must be positive with t >= 2.
- Confirm: The main mean is positive with t >= 2, and the supporting slope is positive with t >= 2.
- Reject: The main mean is negative with t <= -2: weekend moves continue rather than reverse.
- Inconclusive: Inconclusive if the main t lies between -2 and 2, or if the main t is >= 2 but the slope's t is below 2. At least 300 Sunday cases are required, else inconclusive.
