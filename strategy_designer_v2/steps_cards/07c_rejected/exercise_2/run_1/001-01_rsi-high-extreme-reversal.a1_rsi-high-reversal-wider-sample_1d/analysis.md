---
line: 7.c rejected
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample_1d
idea tested: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample
step 5: rejected
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3386 USD
---
## Findings
- **F1:** The tested short was rejected because price rose more than usual after extreme high RSI: the 595 extreme cases (forecast ≤ -5) on the 5-bar grid had a pooled mean 5-bar excess return of +1.44% (t = +2.58). Only 1 of 6 coins had a negative mean, and the book lost money (Sharpe -1.26, mean daily return -0.075%, of which -0.056% was timing and -0.019% was the market's own drift).
- **F2:** The rise after high RSI holds where the coin's 60-day return is positive. With 60-day return above 0 and RSI 70–100, the mean excess return was +2.69% over 5 days (n = 112, t = 2.04) and +6.02% over 10 days (n = 61, t = 2.37). In that up-regime, RSI's rank correlation with the 10-day excess return was +0.118 (n = 423, p = 0.015), against -0.020 (n = 404, p = 0.68) when the 60-day return was negative.
- **F3:** The continuation grows with RSI across all coins. The mean 5-day excess return by RSI bucket rises from -0.96% at RSI 40–50 (n = 833, t = -3.11) to +0.69% at 70–80 (n = 193) and +3.10% at 80–100 (n = 64, t = 1.59). The 10-day figures rise from -1.55% (t = -2.30) to +2.65% and +10.3%.
- **F4:** Among extreme cases, the 60-day uptrend carries the sample: 268 of 300 had a positive 60-day return, with a mean of +1.91% (t = 2.40). The 32 downtrend cases averaged +1.55% (t = 0.68).
- **F5:** The effect is uneven across coins and years.
- **F6:** Low RSI also showed some rebound, but it is weak. With RSI 0–30, the mean excess return was +0.67% over 1 day (n = 677, t = 2.47), +1.72% over 5 days (t = 1.30) and +3.38% over 10 days (n = 60, t = 1.81).

## Ideas
- `001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation` (from F1, F2, F3, F4): While a coin's 60-day return is positive, the higher its 14-day RSI, the more the coin rises over the next 10 days, by more than its usual 10-day move.
- `001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c2_rsi-graded-momentum-continuation` (from F1, F3, F5): The higher a coin's 14-day RSI, the more the coin rises over the next 10 days, beyond its usual 10-day move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
