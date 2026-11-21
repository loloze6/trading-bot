---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound.c1_deep-plunge-next-day-rebound
line: 7.d not profitable
backtest: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound.c1_deep-plunge-next-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, is a drop of several times its 30-day average absolute daily return, the price rises over the next 1 day by more than the coin's normal 1-day drift, only while its past 7 days have been turbulent (its 7-day average absolute daily return large against its 30-day average); the larger the drop multiplied by that turbulence, the larger the rise.
Consequence: A trader should buy a deep hourly plunge only when it comes after a week of unusually large daily moves, and size the buy by the plunge times that turbulence, because that is where the rebound is several times the cost of a trade.
Why:
- F2: The rebound depends on how turbulent the coin's past week was. The measure is its 7-day mean absolute 24-hour return over its 30-day mean absolute 24-hour return.
- F3: The same split holds in the book's own bars. Its calm-week bars lose -0.56 before fees and -1.41 after 0.85 of fees. Its turbulent-week bars earn +13.34 before 1.72 of fees, which is 85 % of the book's whole gain (15.70 gross, 5.15 fees).
- F4: The effect is graded by the drop multiplied by the week's turbulence:
- F5: Most cases are too weak to pay. 4477 of 8426 cases are drops of 1 to 1.5 multiples, with +0.08 % excess (t 1.1), below the 0.19 % cost. Drops of 3 to 5 multiples give +1.56 % (t 4.3, 332 cases), so the pooled unusual move of +0.11 % is 0.6 times the cost.
- F7: In those falling windows the book still held 0.12 to 0.35 of the book and lost in calm and in middle weeks (-0.51 and -0.76 before fees). So the losses that drive the Calmar come from drops bought in calm weeks.
