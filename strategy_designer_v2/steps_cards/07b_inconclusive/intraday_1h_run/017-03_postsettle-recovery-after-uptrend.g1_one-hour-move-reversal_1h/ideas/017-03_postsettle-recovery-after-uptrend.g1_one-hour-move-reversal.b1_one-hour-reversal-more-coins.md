---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-03_postsettle-recovery-after-uptrend.g1_one-hour-move-reversal
line: 7.b inconclusive
backtest: 017-03_postsettle-recovery-after-uptrend.g1_one-hour-move-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's return over the next 1 hour runs against its own last-hour return, and the larger that move relative to the coin's recent hourly volatility, the larger the reversal. The reversal is strongest when the coin's 30-day volatility is high.
Consequence: Fade sharp single-hour moves, sized up in volatile periods, and refuse to chase them.
Why:
- F1: The fade is real and clearly graded by the size of the last-hour move. The pooled excess gain is 8.15e-05 per bar (t 10.23, 416,645 bars). It rises with the size of the forecast, from 0.1e-05 (t 0.74) at |forecast| ≤ 2 to 18.1e-05 (t 5.91) at |forecast| above 15. The raw fade, the next-hour return against the sign of the last hour, grows from −2.7e-05 (t −0.78) in the smallest |z| quintile to 33.1e-05 (t 7.58) in the largest.
- F2: The 30-day-volatility check points the predicted way but is weak, which is why the result is unclear. High-volatility bars earn 10.0e-05 (t 8.10) against 6.9e-05 (t 5.08) for low-volatility bars, a Welch t of 1.69 with 156,480 bars in each group. High beats low in all six coins, but only by 0.6e-05 (ZEC) to 6.5e-05 (LTC).
