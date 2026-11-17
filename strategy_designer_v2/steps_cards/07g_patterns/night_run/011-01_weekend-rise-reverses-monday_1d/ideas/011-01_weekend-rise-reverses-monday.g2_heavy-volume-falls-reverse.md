---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's large one-day fall made on heavy volume compared with its 60-day average volume is partly undone over the next 1 day, and the heavier that day's volume, the larger the next day's rebound.
Consequence: Heavy-volume liquidation days are better read as forced selling to buy against than as information to follow.
Why:
- F4: In the high-volatility half, the reversal sits on days of heavy volume (volume above the coin's median ratio to its 60-day average), not light volume: the slope is -5.38e-3 (t -4.86) against -0.44e-3 (t -0.30) in the top quartile, and -2.71e-3 (t -3.63) against +1.71e-3 (t 1.29) in the third quartile, which is the opposite of the brief's thin-book reasoning.
- F2: In the top volatility quartile this reversal comes from down days only: the slope is -10.95e-3 (t -5.37, n 1,760) on days that fell and +1.07e-3 (t 0.71, n 1,866) on days that rose.
- F3: Graded by size over all days, the next day's excess return is +7.30e-3 after days at or below -2 usual moves (n 834) and +4.41e-3 after days between -2 and -1 (n 1,730), against only -0.5e-3 to -1.7e-3 after rises of any size.
