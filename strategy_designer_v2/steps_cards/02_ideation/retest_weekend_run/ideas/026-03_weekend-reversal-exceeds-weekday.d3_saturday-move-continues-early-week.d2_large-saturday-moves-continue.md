---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week
line: 7.d confirmed, not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return over Saturday, measured against the coin's usual 30-day move, is followed over the next two days by a move in the same direction. That continuation grows faster than in proportion to Saturday's move, so Saturday's largest moves carry most of it.
Consequence: A trader would put most of the weekly bet on the weekends whose Saturday move was largest in usual moves, and little on the ordinary ones.
Why:
- F5: The effect is concentrated in the strongest cases. The top quintile of |forecast| earns +1.63 % per case (t 4.23, 485 cases), while the four lower quintiles earn only +0.07 % to +0.30 % (t 0.19 to 0.98). Trading only the top two quintiles gives Calmar 0.78 against 0.70.
- F2: The effect lives in calm markets and is absent in turbulent ones. In the low tercile of a coin's 30-day hourly volatility, the Monday–Tuesday move in Saturday's direction averages +1.04 % (t 5.0, 750 cases). In the middle tercile it is +0.30 % (t 1.28, 747) and in the high tercile −0.04 % (t −0.12, 749). The 5 % worst adverse path over the 48 hours goes from −8.1 % in the low tercile to −19.9 % in the high one.
