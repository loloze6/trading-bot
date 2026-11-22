---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues
line: 7.d not profitable
backtest: 026-01_weekend-rise-reverses-early-week.d1_calm-regime-weekend-move-continues_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 30-day hourly volatility is low against its own last 6 months, a rise over its 7 days to Monday 00:00 UTC continues over the following two days (Monday and Tuesday). The larger that 7-day rise against the coin's 30-day volatility, the larger the continuation.
Consequence: In calm weeks a trader would buy at the start of Monday after a rising week, sized by how strong the week's rise was, rather than by the weekend's move alone.
Why:
- F3: The continuation lives where the weekend move extends the preceding 5 days (Monday to Friday) in the same direction: 1.22 % per case (t 3.89, n 569) against 0.33 % (t 1.24, n 593) when they disagree.
- F4: Ranked by that prior 5-day move in the weekend's direction (scaled by 30-day hourly volatility), the book's gain per case grows across the quintiles: 0.11 % (t 0.52), −0.14 % (t −0.58), 0.46 % (t 2.34), 0.74 % (t 3.01), 0.71 % (t 2.60).
- F5: Longs carry the effect and shorts barely do:
- F6: The book is too thin and too shallow to clear its bars:
