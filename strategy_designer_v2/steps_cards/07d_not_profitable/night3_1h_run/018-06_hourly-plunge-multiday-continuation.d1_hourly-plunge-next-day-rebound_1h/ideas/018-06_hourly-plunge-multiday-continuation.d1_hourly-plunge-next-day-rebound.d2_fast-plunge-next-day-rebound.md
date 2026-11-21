---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound
line: 7.d not profitable
backtest: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, is a drop of several times its 30-day average absolute daily return, the price rises over the next 1 day by more than the coin's usual 1-day move, except when the drop was spread over the whole day. The larger the share of the drop made in the last 6 hours, the larger the rise.
Consequence: A trader should buy a sudden capitulation, not a slow daily slide of the same size.
Why:
- F1: The rebound sits almost entirely in the largest drops. After a drop of 3 or more multiples of the 30-day average absolute daily return, the next 24 hours end 0.38 of a usual 1-day move above the drift (+2.0 % raw, 376 cases). After drops of 1 to 3 multiples they end only 0.07 to 0.08 above (+0.46 % to +0.62 % raw, 2696 cases). The book traded all of them, so the idea's average unusual move is +0.11 % per case, 0.6 times the 0.19 % cost of a trade.
- F5: The rebound is larger when the drop came fast. When most of the 24-hour drop happened in its last 6 hours, the next 24 hours rise +0.78 % above drift (t 3.6, 795 cases). After slow drops they rise +0.24 % (t 1.4, 795 cases).
- F6: The rebound is done within a day. Hot drops of 3 or more multiples are +2.65 % above drift at 24 hours and +2.76 % at 72 hours, so a longer holding adds almost nothing.
