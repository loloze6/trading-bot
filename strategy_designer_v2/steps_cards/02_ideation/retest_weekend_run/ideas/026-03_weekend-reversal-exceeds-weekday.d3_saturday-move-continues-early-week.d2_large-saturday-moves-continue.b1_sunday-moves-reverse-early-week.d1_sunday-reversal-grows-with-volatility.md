---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week
line: 7.d confirmed, not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return over Sunday, measured against the coin's usual 30-day move, is followed over the next two days (Monday and Tuesday) by a move in the opposite direction, and the higher the coin's hourly volatility over the last 30 days, the larger that reversal.
Consequence: A trader would lean against Sunday's move at Monday 00:00 UTC for two days, betting more the more turbulent the coin's last 30 days were, and would bet little on a calm coin.
Why:
- F2: The vol-target sizing puts the book's size where the effect is absent, and that is why its gain is too small. In the lowest third of each coin's 30-day hourly volatility, Monday cases move +0.00 % (t 0.01, 765 cases) while the book holds |allocation| 0.54. In the middle third they move +0.69 % (t 2.92) at 0.38. In the highest third they move +1.21 % (t 3.40, 719 cases) at only 0.23. So the book earns −0.08 % per case in the lowest third, +0.33 % in the middle and +0.24 % in the highest, only +0.16 % per case overall.
- F3: High volatility is not an effect of its own. On Tuesday to Saturday, the same 48-hour move against the past 24 hours in the highest volatility third is −0.00 % (t −0.01, 3784 cases), against +1.21 % on Mondays in that third. The condition therefore only grades the weekend reversal, as the theory's thin-liquidity mechanism says: weekend prices are pushed furthest when the coin is turbulent.
- F4: Sizing by the size of Sunday's move does not grade the effect and loses money at the top. By quintile of |Sunday z|, the 48-hour reversal is +0.42 %, +0.79 %, +0.50 %, +0.79 % and +0.62 %, with no rise. The trades with the largest entry forecast (mean |forecast| 17.8, 956 trades) lose −0.60 % net. Trades with mean |forecast| 3.2 to 6.4 gain +0.27 % to +0.36 % net.
- F8: The effect is spread across years and coins, not tied to one period. It is positive in 7 of 8 years, all but 2023 (−0.03 %), and positive on all six coins, from +0.18 % (ZEC) to +0.91 % (ETH).
