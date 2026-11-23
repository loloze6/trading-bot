---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr
line: 7.e profitable but not proven
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d3_heavy-weekends-without-xmr_1h
instruments: BTC, ETH, LTC, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's move over Saturday and Sunday continues in its own direction over the next 48 hours. The continuation is larger the heavier the weekend's volume is against its mean over the preceding five weekdays, whatever the size of the move.
Consequence: The weekend volume ratio, not the size of the weekend move, is what a trader should scale a Monday–Tuesday follow-through bet on.
Why:
- F1: Inside the heavy-volume weekends, the move that follows grows with the volume ratio and not with the move's size. On 1,905 weekends, regressing the 48-hour strength on log(volume ratio) and the weekend move in usual moves gives +0.261 (t 5.76) on log volume ratio and −0.186 (t −4.08) on move size. Strength by move tercile within heavy weekends is flat: small 0.18, mid 0.29, large 0.21. This is why the plan's size check, ranked on |forecast| = move × ratio, failed (−0.0025).
- F2: The effect belongs to weekends, not to heavy volume in general. The top weekend volume-ratio quintile has a 48-hour strength of +0.241 (t 3.64, 381 cases) against −0.088 in the lowest. The same Tuesday-close measure gives +0.048 (t 0.90) in its top quintile and a log-ratio slope of +0.056 (t 1.17). For heavy weekends the signed unusual move is +1.64 % at 48 hours (t 3.17, 348 cases), against +0.37 % (t 1.75, 1,135) for heavy midweek stretches.
- F3: The book's gain is timing, not the market's own rise. The market-rise part is about 0.00001 a day of the book's 0.000288 mean daily return. Every coin and seven of eight years have a positive book mean; only 2025 is negative (−0.000267, heavy-weekend move −0.76 %, t −0.60).
