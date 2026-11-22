---
idea: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins
brief: 028_volume-confirmed-hourly-moves-continue
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1h
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: 004d1ddfa7f1
---
Fidelity:
- Situation: an hour whose rise is far above the coin's typical hourly move, on volume several times its average -> adapted: the "far above" and "several times" thresholds become a graded product (rise in usual moves x volume ratio) with a strong dead zone; "after that hour" becomes "while that hour is the latest bar", and the bet is held 24 bars.
- Comparison: the typical hourly move and the average hourly volume, both over the past 30 days -> kept: the return's standard deviation over 720 bars and the mean volume over 720 bars.
- Outcome: the price keeps rising over the next 24 hours, more after a larger rise times volume, with no shorts -> kept: long only, held 24 bars, judged on what follows the largest positions.
- Verdict transfer: yes: the forecast is the idea's own rise-times-volume measure, so the 24-hour return after it confirms or rejects the idea itself.
Forecast: The forecast uses VolumeWeightedScaledReturnComponent with vol_period 720 and volume_period 720. It multiplies two things: - the latest hour's return divided by the standard deviation of hourly returns over the past 30 days; - that hour's volume divided by its 30-day mean. The product is standardised over its past 500 values (min_periods 120). It is clipped at 0, so only rises on volume count and there are no shorts. Then signed_power with exponent 3 applies the strongest graded dead zone: ordinary hours give almost 0, and a large rise on heavy volume grows the long sharply. The forecast is positive only on such hours and zero otherwise. Each bet is held for 24 bars.
Config: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins_1h_config.json
Criterion:
- Horizon: 24 bars
- Main measure: Take each case (a rise of the forecast of at least 2 points, read once per 24-bar grid cell of each window). Measure the coin's 24-bar return from the case's close minus the coin's normal 24-bar drift over all windows. Report the mean over all cases and coins, with the t of that mean.
- Supporting check: Split the cases at the median forecast. The mean unusual 24-bar move of the top half minus that of the bottom half must be above 0.
- Confirm: The mean unusual move is positive with t >= 2 on at least 30 cases, and the supporting check is above 0.
- Reject: The mean unusual move is negative with t <= -2 on at least 30 cases.
- Inconclusive: A t between -2 and 2, fewer than 30 cases, or t >= 2 with the supporting check not above 0.
