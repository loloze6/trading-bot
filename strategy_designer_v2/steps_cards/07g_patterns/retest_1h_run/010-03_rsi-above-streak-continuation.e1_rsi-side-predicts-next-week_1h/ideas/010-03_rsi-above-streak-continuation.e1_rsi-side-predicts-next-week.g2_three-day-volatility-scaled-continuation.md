---
brief: 010_rsi-midline-regime-direction
source-idea: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week
line: 7.g patterns
backtest: 010-03_rsi-above-streak-continuation.e1_rsi-side-predicts-next-week_1h
instruments: BTC, ETH, BNB
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 3-day return relative to its recent volatility, the higher its return over the next 3 days.
Consequence: A trader would lean with a coin's 3-day move, sized by its volatility-scaled strength, holding for days and adjusting slowly so that fees do not consume the gain.
Why:
- F3: Over longer spans, moves tend to continue. The 72-hour scaled return against the next 72 hours has a correlation of +0.051 (t 2.20, 1,860 cases). The 168-hour return against the next 168 hours has +0.062 (t 1.73, 766 cases). BTC and ETH have the same sign at both horizons.
- F4: The tested forecast sorts 7-day excess returns at its extremes. The top forecast quintile is followed by +0.0174 (t 1.82) and the bottom by -0.0119 (t -1.24). Both coins show the ordering: BTC +0.0120 vs -0.0071, ETH +0.0228 vs -0.0168.
- F1: The book's losses come from trading costs, not from a wrong forecast: before costs the position gains 0.00155 a day on BTC and 0.00199 a day on ETH, but fees take 0.00410 and 0.00366 a day. Allocation changes larger than 0.2 make up 88% of all fees (47,264 bars), and the book's mean daily return is negative on every weekday except Monday (t from -1.8 to -3.5).
