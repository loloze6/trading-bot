---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation
line: 7.g patterns
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The higher a coin's 10-day return, the more its price rises above its usual move over the next 10 days.
Consequence: Lean long on coins with strong 10-day gains for the following 10 days rather than fading them.
Why:
- F3: A plain past 10-day return carries the same continuation: the top per-coin quintile of 10-day return was followed by +3.00% over the next 10 days (t = 2.50, n = 308), and the second and third quintiles by −2.15% (t = −2.87) and −2.04% (t = −2.64). The lowest quintile was only −0.72% (t = −0.87), so the grading holds from the middle upward and not at the bottom.
- F2: The tested forecast does sort the 10-day outcome: after 10 days, the top forecast bin (15 to 20) shows +4.17% above the coin's mean (t = 2.62, n = 195) and the zero-forecast bars show −1.07% (t = −2.24, n = 853), on the non-overlapping 240-bar grid with 1674 cases in total. The middle bins rise in order: −0.96%, +0.35% and +1.22%.
- F5: Of BTC's gross gain of 0.143% per day, only 0.047% comes from the market's own rise (mean position 0.37 × mean bar return), so about two-thirds is timing.
