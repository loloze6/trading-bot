---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend
line: 7.d not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: After a fall in a coin's 48-hour return, the coin rises over the next two days, and the larger the fall, the larger the rebound.
Consequence: A trader would buy after a sharp two-day fall rather than short it, with more conviction the deeper the fall.
Why:
- F2: The continuation lives almost only after midweek rises: long cases move +0.96 % total (+0.69 % unusual, 1132 cases), while short cases move −0.36 % total (−0.09 % unusual, 1247 cases), so the short half of the book pays the cost for nothing.
- F3: The effect after rises is graded by size. Rises in the largest |48h move| quintile continue +2.12 % over 48 hours (t 4.02, 249 cases) and those in the fourth quintile +1.15 % (t 3.23, 234 cases). The matching falls show no continuation: −0.09 % (t −0.19) in the top quintile and −0.87 % (t −2.42, a rebound) in the fourth.
- F6: Across all weekdays the two largest move quintiles split by direction. Rises continue +0.56 % over the next 48 hours (t 4.23, 3452 cases). Falls are followed by a rise, −0.36 % in the fall's direction (t −2.67, 3127 cases).
