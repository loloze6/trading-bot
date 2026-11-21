---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d2_extreme-daily-run-reverses
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d2_extreme-daily-run-reverses_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The higher a coin's hourly volatility over the past week, the more its 24-hour fall, measured in usual 24-hour moves, is followed by a rise over the next 24 hours: the larger the fall, the larger the rebound.
Consequence: A trader can buy a coin's sharp daily falls in turbulent weeks for a day, where the rebound is several times a round trip, and refuse the same trade in calm weeks.
Why:
- F1: The reversal of a coin's 24-hour run appears only when its past-week hourly volatility is high: after a run of more than one usual 24-hour move, the forecast-signed drift-adjusted return over the next 24 hours is +189 bps (t 6.32, 859 non-overlapping cases) in each coin's top volatility quintile, against -10 to +20 bps (|t| ≤ 1.12, about 856 cases each) in the four lower quintiles.
- F2: Inside the top volatility tercile the reversal is graded by the size of the run: by quartile of the absolute volatility-scaled 24-hour return, the signed 24-hour return is +6, +7, +63 (t 3.60) and +134 bps (t 6.52), about 1,389 cases each. The upper half is 3 to 7 times the round-trip cost of about 19 bps, while the idea as tested captured only 6 bps per case, 0.3 times that cost.
- F3: The high-volatility reversal holds on every coin: on the top tercile with absolute run above 1, it is +78 bps on BTC (t 2.50) and +115 to +184 bps on ETH, LTC, XMR, XRP and ZEC (t 2.19 to 3.08), 216 to 255 cases per coin. It is positive in all 8 years (+33 to +208 bps), with t above 2 in 4 of them (2018, 2019, 2021, 2023).
- F4: The reversal is stronger after falls than after rises. In the top volatility tercile, falls are followed by a rebound of +200 bps (t 6.45, 685 cases) and rises by a give-back of +67 bps (t 2.40, 677 cases). The book's trades show the same split: longs earned +0.32 % net (24,717 trades) and shorts lost -0.96 % net (23,093 trades).
- F6: In calm conditions the 24-hour run does not reverse, and after moderate falls it continues: in the bottom volatility tercile the excess return after a -0.5 to -1.5 run is -24 bps (t -2.31, 1,113 cases). Over all bars, the largest-rise decile gives back only -21 bps (t -1.71), against +70 bps after the largest-fall decile (t 4.73).
