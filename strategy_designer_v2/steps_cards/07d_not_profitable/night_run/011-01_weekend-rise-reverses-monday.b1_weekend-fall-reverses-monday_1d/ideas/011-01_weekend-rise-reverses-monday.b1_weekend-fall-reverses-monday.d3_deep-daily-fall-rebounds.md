---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell over the past day rises over the next day, and the larger that fall relative to the coin's usual daily move, the larger the rise.
Consequence: A deep one-day fall on any day of the week is a reason to lean long for a day, which gives a reversal book many more cases than Sundays alone.
Why:
- F1: The book is flat almost all the time. It held a position on only 1013 of about 17,500 coin-bars (about 6%), at a mean allocation of 0.46. Its mean daily return was 0.000085, against 0.00119 for holding the coins. This is why the mean daily return, the Sharpe against holding and the Calmar (0.15, a yearly gain of about 3%) all fail.
- F5: The reversal is concentrated after the weekend. On the other weekdays, only the deepest fall quintile (z −1.39) was followed by a next-day rise (0.0056). The other four quintiles were all between −0.0003 and 0.0007. The Sunday quintiles span +0.0076 to −0.0074.
