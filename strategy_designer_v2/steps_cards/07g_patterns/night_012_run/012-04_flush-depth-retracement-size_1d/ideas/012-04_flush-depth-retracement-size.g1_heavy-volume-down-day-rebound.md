---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-04_flush-depth-retracement-size
line: 7.g patterns
backtest: 012-04_flush-depth-retracement-size_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a day a coin closes lower, the higher that day's volume relative to its median over the prior 20 days, the larger the coin's rise over the next day.
Consequence: Heavy-volume down days are a reason to buy for the next day rather than sell, and quiet down days are not.
Why:
- F1: On down days (bar return below zero), the log of volume over its prior 20-day median predicts the next-day excess return with slope +0.0045 (t 5.28, n 7056 non-overlapping cases); on up days the same slope is +0.0002 (t 0.25, n 7300), so the volume effect sits only on falling days.
- F3: Among down days, next-day excess return rises with the volume-ratio quintile: from −0.05% (bottom quintile, n 1391) to +0.70% (top quintile, n 1400); up days stay flat or negative in every quintile (−0.14% in the top quintile).
- F4: The pooled volume slope is positive in every coin at one day (t from 0.69 in BTC to 2.82 in ZEC) but uneven by period: t 1.22 in w1–w12 and t 4.11 in w13–w24, so the effect is stronger in the later windows.
- F5: The tested flush filter adds little: sharp falls (z ≤ −2) with volume ≥ 2× and a lower wick ≥ 0.3 average +1.88% excess over 3 days (t 1.78, n 31) against +0.11% for other sharp falls (n 139), and −0.62% over the next day (t −1.06, n 85). The wick shape does not carry the rebound; the volume does.
