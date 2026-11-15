---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 50-day SMA is above its 200-day SMA, the higher the coin's own 20-day return, the larger its return over the next 10 days.
Consequence: Inside an uptrend, a trader should scale long exposure by recent 20-day momentum rather than by the width of the 50/200 spread, and refuse longs in uptrends whose last 20 days fell.
Why:
- F2: Within the forecast-on bars, the coin's own 20-day return separates what follows. When it is up, the 10-day excess return is +0.0221 (361 cases); when it is down, it is -0.0171 (333 cases), Welch t 3.00. The graded slope on the per-coin z-scored 20-day return is 0.0150 with t 2.25 (694 cases).
- F3: The same 20-day momentum shows nothing while the 50-day SMA is below the 200-day SMA: the slope's t is -0.73 and up minus down is -0.0037 vs +0.0002 (t -0.40, 681 cases). Pooled over all bars it is only t 2.17, so the effect lives in the uptrend state.
- F4: The size of the forecast is not graded. Across forecast quartiles the 10-day excess returns run -0.0094, +0.0049, +0.0060 and +0.0006, with hit rates of 0.47 to 0.51, below the 0.53 of off bars. The widest raw-spread sixth has -0.0069 against +0.0078 just around the cross.
- F7: The book's mean daily return of 0.000377 is almost entirely market exposure. The position times the coin's mean daily return gives 0.000353, against 0.000025 of timing, at a mean position of 0.28.
