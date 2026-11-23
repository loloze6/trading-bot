---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g2_high-volatility-hourly-shock-reversal
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g2_high-volatility-hourly-shock-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The higher a coin's 24-hour volatility is relative to its 30-day volatility, the more its large 24-hour return, measured against its 30-day volatility, reverses over the next 24 hours.
Consequence: A trader would fade one-day moves hardest when the day's volatility is far above its monthly norm, and refuse the fade when volatility is calm.
Why:
- F4: Among cases with |z24| > 1, the 24-hour fade grows with the ratio of 24-hour to 30-day volatility: +0.04 % (t 0.2, n 562) for a ratio below 0.8, +0.41 % (t 3.1, n 1485) for 0.8–1.2, +0.72 % (t 4.4, n 1334) for 1.2–2 and +1.46 % (t 3.0, n 322) above 2.
- F1: A coin's 24-hour return, scaled by its 30-day hourly volatility (z24), is followed by a graded reversal over the next 24 hours. On a non-overlapping 24-bar grid, the excess return in the fade direction is -0.06 % (t -1.2, n 7793) for |z24| ≤ 0.5, +0.07 % (t 0.9, n 4287) for 0.5–1, +0.46 % (t 4.7, n 2882) for 1–2, +0.61 % (t 2.2, n 602) for 2–3 and +1.73 % (t 3.1, n 219) above 3, and the pooled slope of the excess 24-hour return on z24 is -0.28 % per unit (t -6.9, n 15806).
