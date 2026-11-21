---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound.c1_deep-plunge-next-day-rebound
line: 7.d not profitable
backtest: 018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound.c1_deep-plunge-next-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, is a drop of several times its 30-day average absolute daily return while its past 7 days have been calm (its 7-day average absolute daily return small against its 30-day average), the price keeps falling over the next 1 day below the coin's normal 1-day drift; the calmer the week before the drop, the larger the further fall.
Consequence: A trader should refuse to buy, or treat as a reason to sell, a sudden plunge that breaks a quiet week, because it tends to keep falling for a day.
Why:
- F2: The rebound depends on how turbulent the coin's past week was. The measure is its 7-day mean absolute 24-hour return over its 30-day mean absolute 24-hour return.
- F4: The effect is graded by the drop multiplied by the week's turbulence:
- F6: In the falling windows w13 to w16 the turbulent-week rebound almost vanishes: +0.10 % (t 0.2, 388 cases), against +1.16 % (t 8.3, 1737 cases) in the other windows. Calm-week cases there fall -1.39 % (t -4.0, 312 cases).
- F7: In those falling windows the book still held 0.12 to 0.35 of the book and lost in calm and in middle weeks (-0.51 and -0.76 before fees). So the losses that drive the Calmar come from drops bought in calm weeks.
