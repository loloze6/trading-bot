---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins
line: 7.b inconclusive
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been large relative to its 30-day high-low range, the larger its 30-day return, the further the coin moves in that same direction over the next day.
Consequence: A trader would follow a trending coin's 30-day direction for the next day rather than fade it.
Why:
- F1: Inside the tested regime, the test's 5-day horizon is the weakest of the clean readings: the slope of the drift-adjusted return on forecast/10 has t 4.27 over the next day (3221 cases, mean directional unusual move +0.39 %, t 3.91) and t 2.83 over 3 days (3138 cases, +0.54 %). Over 5 days it falls to t 1.86 (3120 cases, +0.71 %, t 2.76).
- F3: The slope at 5 days comes almost entirely from the sign of the forecast, not its size. Within each side the slope is negative: t −2.82 on the short side (1539 cases) and −1.07 on the long side (1581 cases). The forecast quartiles show no gradient either: directional means of +1.37 %, +0.89 %, −0.59 % and +1.19 % from the smallest to the largest |forecast|.
