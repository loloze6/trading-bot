---
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend_1h
idea tested: 017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3691 USD
---
## Findings
- **F1:** Over non-overlapping 1-day steps, a coin's past 1-day return correlates −0.087 with its next 1-day excess return (n = 16,814). The correlation is negative in all 6 coins (−0.066 to −0.126) and in 7 of 8 years (2024 is +0.011). Across quintiles of the vol-scaled 1-day return, the lowest quintile gains +42.8 bp (t = 4.33, n = 3,251) and the highest loses −18.9 bp (t = −2.13, n = 3,249).
- **F2:** This 1-day reversal sits almost entirely in the coin's highest tercile of 7-day hourly volatility. There the correlation is −0.110 (n = 5,413), against +0.031 and +0.014 in the low and middle terciles.
- **F3:** The next hour's excess return falls steadily across deciles of the last hour's return scaled by 1-day volatility. It runs from +4.6 bp (t = 7.1, n = 41,310) after the sharpest falls to −3.2 bp (t = −6.5) in decile 9 and −1.6 bp (t = −2.6) in decile 10. This t is not clustered by day, so it is likely overstated. The rebound after sharp falls is positive in all 6 coins and largest in the smaller coins (ZEC +9.1 bp, XRP +6.1 bp, BTC +2.8 bp). Over the next 6 hours, the lowest quintile keeps only +4.6 bp (t = 2.0), so most of the effect is in the first hour.
- **F4:** The tested signal is close to zero. At 11:00 UTC the 3-day return correlates only −0.030 with the next hour's vol-scaled return, and the book loses: gross trade mean −0.116 %, net −0.216 %, daily book mean −0.001, Sharpe −4.28. Fees are about as large as the gross loss.
- **F5:** Hour-of-day drift is the same sign in all 6 coins for two hours, but it does not survive 24 hours tested and changes sign across years. The hour from 20:00 to 21:00 UTC averages +4.8 bp (day-clustered t = 2.93); the year 2022 is −5.5 bp. The hour from 13:00 to 14:00 UTC averages −4.2 bp (t = −2.16). I do not count it as an idea.

## Ideas
- `017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend.g1_daily-reversal-in-volatile-regimes` (from F1, F2): The larger a coin's 1-day return, the lower its return over the next 1 day. The effect is strongest, and still graded by the size of the 1-day move, when the coin's 7-day volatility is high.
- `017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend.g2_hourly-rebound-after-sharp-falls` (from F3): The larger a coin's fall over the last hour, measured against its 1-day volatility, the larger its rise over the next 1 hour.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
