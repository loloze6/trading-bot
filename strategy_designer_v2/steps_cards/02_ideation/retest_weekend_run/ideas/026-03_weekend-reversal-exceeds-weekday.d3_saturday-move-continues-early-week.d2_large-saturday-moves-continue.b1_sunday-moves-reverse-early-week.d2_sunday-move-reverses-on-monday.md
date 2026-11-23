---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week
line: 7.d confirmed, not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return over Sunday, measured against the coin's usual 30-day move, is followed over the next 24 hours (Monday) by a move in the opposite direction, the larger the higher the coin's hourly volatility over the last 30 days.
Consequence: A trader would lean against Sunday's move at Monday 00:00 UTC and be out by Tuesday 00:00 UTC, so no position is carried into days that earn nothing.
Why:
- F1: The reversal belongs to Monday alone. Over 48 hours from the 00:00 UTC bar, the drift-adjusted move against the past 24 hours is +0.62 % on Monday (t 3.98, 2244 cases). On every other weekday it lies between −0.36 % and +0.21 %, for example Tuesday −0.04 % (t −0.30) and Saturday +0.21 % (t 1.78). This is the weekend effect the theory names.
- F5: The book carries positions far past the two days, which dilutes its mean daily return on days in a position (0.021 % against the required 0.05 %).
- F6: Most of the reversal comes within Monday itself. It is +0.46 % over 24 hours (t 4.08, 2265 cases), +0.62 % over 48 hours (t 3.98) and +0.78 % over 120 hours (t 3.19). One day's holding gives the larger move per day in a position (0.46 % against 0.31 % a day over two days).
- F2: The vol-target sizing puts the book's size where the effect is absent, and that is why its gain is too small. In the lowest third of each coin's 30-day hourly volatility, Monday cases move +0.00 % (t 0.01, 765 cases) while the book holds |allocation| 0.54. In the middle third they move +0.69 % (t 2.92) at 0.38. In the highest third they move +1.21 % (t 3.40, 719 cases) at only 0.23. So the book earns −0.08 % per case in the lowest third, +0.33 % in the middle and +0.24 % in the highest, only +0.16 % per case overall.
