---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week
line: 7.d confirmed, not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's rise over Sunday, measured against the coin's usual 30-day move, is followed over the next two days (Monday and Tuesday) by a fall, and the higher the coin's hourly volatility over the last 30 days, the larger that fall.
Consequence: A trader would short a coin at Monday 00:00 UTC after a Sunday rise for two days, betting more the more turbulent the coin, and would not take the long side after a Sunday fall.
Why:
- F7: The short side, after a Sunday rise, carries more of the effect than the long side: +0.86 % (t 3.85, 1142 cases) against +0.38 % (t 1.73, 1102 cases). It is strongest in the highest volatility third, at +1.85 % (t 3.83, 368 cases). That is 9.7 times the 0.19 % cost of a trade, while the lowest third's +0.00 % cannot pay any cost.
- F2: The vol-target sizing puts the book's size where the effect is absent, and that is why its gain is too small. In the lowest third of each coin's 30-day hourly volatility, Monday cases move +0.00 % (t 0.01, 765 cases) while the book holds |allocation| 0.54. In the middle third they move +0.69 % (t 2.92) at 0.38. In the highest third they move +1.21 % (t 3.40, 719 cases) at only 0.23. So the book earns −0.08 % per case in the lowest third, +0.33 % in the middle and +0.24 % in the highest, only +0.16 % per case overall.
- F3: High volatility is not an effect of its own. On Tuesday to Saturday, the same 48-hour move against the past 24 hours in the highest volatility third is −0.00 % (t −0.01, 3784 cases), against +1.21 % on Mondays in that third. The condition therefore only grades the weekend reversal, as the theory's thin-liquidity mechanism says: weekend prices are pushed furthest when the coin is turbulent.
