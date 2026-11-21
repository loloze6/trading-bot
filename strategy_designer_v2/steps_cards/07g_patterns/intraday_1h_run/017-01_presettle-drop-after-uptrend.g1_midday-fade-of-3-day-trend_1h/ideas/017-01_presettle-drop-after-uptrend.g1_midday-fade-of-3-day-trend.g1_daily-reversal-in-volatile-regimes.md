---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day return, the lower its return over the next 1 day. The effect is strongest, and still graded by the size of the 1-day move, when the coin's 7-day volatility is high.
Consequence: In a high-volatility period, a trader would lean against the coin's last day's move over the following day, more heavily the larger that move was.
Why:
- F1: Over non-overlapping 1-day steps, a coin's past 1-day return correlates −0.087 with its next 1-day excess return (n = 16,814). The correlation is negative in all 6 coins (−0.066 to −0.126) and in 7 of 8 years (2024 is +0.011). Across quintiles of the vol-scaled 1-day return, the lowest quintile gains +42.8 bp (t = 4.33, n = 3,251) and the highest loses −18.9 bp (t = −2.13, n = 3,249).
- F2: This 1-day reversal sits almost entirely in the coin's highest tercile of 7-day hourly volatility. There the correlation is −0.110 (n = 5,413), against +0.031 and +0.014 in the low and middle terciles.
