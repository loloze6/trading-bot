---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift
line: 7.b inconclusive
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.g2_late-evening-utc-upward-drift_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's return over the two hours from 21:00 to 23:00 UTC is above its normal hourly drift, and the excess is larger the higher the coin's 30-day hourly volatility.
Consequence: A trader would hold the coin long through 21:00–23:00 UTC, or time purchases before that stretch and sales after it.
Why:
- F1: The test's main measure is on the predicted side, with a position-weighted mean 2-bar excess of +0.078 % and t 7.91 over 16,888 cases. It is positive on every coin (+0.075 % to +0.098 %, t 2.70 to 4.24) and in 7 of 8 years. Only the supporting check failed (above-median minus below-median position −0.018 %), so the inconclusive result comes from the check, not from a missing effect.
- F2: The supporting check measured the position, not the volatility. At the 20:00 bar the position held correlates −0.66 with the coin's 30-day hourly volatility, because vol-target sizing divides by volatility. The "above-median position" cases are therefore the low-volatility ones, so the check ran opposite to the idea's grading.
- F3: Graded by the idea's own variable, the effect grows with volatility. Within each coin, the 2-bar excess from the 20:00 close rises from +0.042 % (t 2.69) in the lowest 30-day volatility quintile to +0.201 % (t 5.64) in the highest. On the standardised volatility the forecast uses, it rises from +0.003 % (t 0.12) in the lowest quintile to +0.154 % (t 4.56) in the highest.
