---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade
line: 7.g patterns
backtest: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: A coin moves against its past 24-hour return over the next 24 hours, and the larger that 24-hour return measured in the coin's usual 24-hour moves (from its 30-day hourly volatility), the larger the opposite move. It is largest after the deepest 24-hour falls.
Consequence: After a coin has fallen far more than usual over a day, a trader has reason to buy for the next day, and more so the deeper the fall, because the expected rebound is several times the cost of a trade.
Why:
- F1: A coin's 24-hour unusual move runs against its past 24-hour return, graded by that return measured in usual 24-hour moves. The slope is −0.0020 per unit, t −3.90, on 5552 non-overlapping 24-hour cases pooled over both coins. The slope is negative in all four coin and half-period splits: BTC early −0.0003 (t −0.4), BTC late −0.0026 (t −2.6), ETH early −0.0020 (t −1.9), ETH late −0.0032 (t −2.5). The 72-hour past return shows no such slope (t 0.36).
- F2: After a 24-hour fall deeper than two usual 24-hour moves, the next 24 hours end +1.29 % above the coin's normal drift (t 2.58, 149 cases). That is about 12 times the 0.11 % cost of a trade. The bins in between are graded: +0.09 % after −2 to −1, −0.09 % after 0 to +1, −0.21 % after +1 to +2, −0.35 % above +2. The deep-fall effect sits in the late half (BTC +2.43 %, t 2.72; ETH +3.55 %, t 2.58), not the early half (BTC −0.11 %, ETH −0.34 %).
