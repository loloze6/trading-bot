---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend
line: 7.d not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 48-hour return over Wednesday and Thursday is followed by a move in the same direction over the next two days, Friday and Saturday, and the larger the Wednesday-Thursday move, the larger the move that follows, only while that midweek move is a rise.
Consequence: A trader would buy a coin into the weekend after a midweek rise, with more conviction the larger the rise, and would not short it after a midweek fall.
Why:
- F1: The book's whole edge per case is too thin for its cost: the 2379 Thursday-23:00 cases move +0.30 % in total over 48 hours against a 0.19 % round-trip cost, the 4130 recorded trades average −0.09 % gross and −0.19 % net, and the book is flat five days a week, so its mean daily return is only 0.011 % against 0.05 % required.
- F2: The continuation lives almost only after midweek rises: long cases move +0.96 % total (+0.69 % unusual, 1132 cases), while short cases move −0.36 % total (−0.09 % unusual, 1247 cases), so the short half of the book pays the cost for nothing.
- F3: The effect after rises is graded by size. Rises in the largest |48h move| quintile continue +2.12 % over 48 hours (t 4.02, 249 cases) and those in the fourth quintile +1.15 % (t 3.23, 234 cases). The matching falls show no continuation: −0.09 % (t −0.19) in the top quintile and −0.87 % (t −2.42, a rebound) in the fourth.
- F7: The book misses most of the coin's rise: holding the coins earns 0.33 % on Fridays and 0.45 % on Saturdays per day, while the book earns 0.03 % and 0.11 %. Combined with the yearly sign flips (2019: −0.84 % per case, t −2.57; 2023: −0.32 %), this leaves the Sharpe 0.29 below holding and the Calmar at 0.08.
