---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade.b1_deep-hourly-falls-rebound
line: 7.g patterns
backtest: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade.b1_deep-hourly-falls-rebound_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: Each coin rises over the two hours from 21:00 to 23:00 UTC, and the rise is larger the higher the volume of the hour from 20:00 to 21:00 UTC compared with the coin's average hourly volume over the past 30 days.
Consequence: A busy 20:00 UTC hour is a reason to expect a stronger late-evening rise in the coin over the next two hours.
Why:
- F1: The coins rise in the two hours from 21:00 to 23:00 UTC (from the close of the bar that opens at 20:00 to two bars later). The mean is +9.61 bp with t 6.54 over 5834 day-cases. That is the largest of the twelve two-hour slots of the day; the next largest are +3.72 bp (t 2.59) and -3.46 bp (t -2.34). It holds on each coin: BTC +8.40 bp (t 4.67) and ETH +10.82 bp (t 4.65). It is positive in 81 % of the 48 coin-windows, in 7 of the 8 years (2022 is the exception at -5.11 bp, t -1.17), and on all seven weekdays (+8.0 to +11.8 bp).
- F3: The 21:00–23:00 UTC rise grows with the coin's recent volatility. By quintile of the 30-day mean absolute hourly return it is +7.78, +5.97, +7.18, +11.43 and +16.71 bp (top quintile t 3.40). It is largest when the 20:00 bar's volume is high against its 30-day average: the top volume quintile gives +20.96 bp (t 4.61), against +4.75 to +9.75 bp in the other four. The evening rise is unrelated to the prior 20-hour return (correlation -0.005, n 5594).
