---
idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days
brief: 023_range-reversion-when-no-trend
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: be08f97ea86e
---
Fidelity:
- Situation: the 30-day rise covers a large share of the 30-day high-low range -> adapted: a rule needs abs(30-day net move)/(30-day high-low range) ≥ 0.5, and the forecast is graded by the rise, which is zero unless it is a rise.
- Comparison: beyond the coin's normal drift -> kept: excess over the coin's mean 10-day return across all windows.
- Outcome: the larger the rise, the further the coin keeps rising over the next 10 days -> kept: a long sized by the 30-day rise, held 10 bars.
- Verdict transfer: yes: the test measures this rise-to-range condition, the rise-sized long and the 10-day excess move, so its result is the idea's result.
Forecast: A regime rule activates when NetMoveToRangeRatio (period 30, source high_low) is at least 0.5, meaning the 30-day net move covers at least half of the 30-day high-low range. On those bars the forecast is the 30-day percent return (PriceEvolution, period 30), standardised over its last 60 values. It is then clipped at 0, so it is positive and grows with the size of the rise. It is 0 when the 30-day move was a fall. On all other bars the forecast is 0 (flat). It never goes short.
Config: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.e2_clean-rises-extend-ten-days_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: A case is a bet (a rise of the forecast of at least 2 points), read once per cell of a non-overlapping 10-bar grid in each window. For each case, take the coin's 10-bar return from the signal's close minus the coin's normal 10-bar drift (its mean over all windows). The measure is the mean of that excess return over all cases, with its t.
- Supporting check: Split the cases at the median forecast. The mean excess return of the cases above the median, minus that of the cases below it, must be above 0.
- Confirm: The mean excess return is positive with t ≥ 2, over at least 30 cases, and the supporting check is above 0.
- Reject: The mean excess return is negative with t ≤ -2, over at least 30 cases.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a positive t ≥ 2 when the supporting check is not above 0. So is any result from fewer than 30 cases.
