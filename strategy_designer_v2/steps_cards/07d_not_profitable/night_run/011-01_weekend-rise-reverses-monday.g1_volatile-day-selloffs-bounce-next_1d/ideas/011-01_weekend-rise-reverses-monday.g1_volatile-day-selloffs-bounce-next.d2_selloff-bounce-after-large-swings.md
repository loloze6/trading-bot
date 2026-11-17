---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's day-long fall is large compared with its usual daily move over the past 60 days, it rises over the next 1 day, and the larger the fall in units of its usual move, the larger the rise. This holds only while the coin's 20-day return is large in units of its usual daily move, and the rise is larger the larger that 20-day move.
Consequence: A trader buys sharp one-day falls inside strongly moving spells and refuses them in flat, rangebound spells.
Why:
- F6: The bounce also shows when the coin's 20-day move is large in units of its usual move. By quintile of the absolute 20-day vol-scaled move, the top quintile (mean 2.03) gave an excess of +0.0098 (t 3.99), and the lowest gave -0.0007 (t -0.35).
- F4: The book runs its smallest positions where the effect is largest. By 60-day-std quartile the mean position fell from 0.65 to 0.26, while the excess rose from +0.0014 (t 0.84) to +0.0096 (t 3.88). The result is a mean daily return of 0.00045, against 0.0005 required and 0.00118 from holding, with active bars only 28% of the total.
