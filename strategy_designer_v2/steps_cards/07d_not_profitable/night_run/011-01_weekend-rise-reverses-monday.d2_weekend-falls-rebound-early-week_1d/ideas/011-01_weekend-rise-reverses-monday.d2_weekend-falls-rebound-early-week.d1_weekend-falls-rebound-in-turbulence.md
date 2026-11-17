---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 3 days, and the larger the weekend fall relative to its usual daily move, the larger the rise, only while its 20-day volatility is high against its 60-day volatility. Within that state, the higher its 20-day volatility against its 60-day volatility, the larger the 3-day rise.
Consequence: A trader should buy weekend sell-offs that come in turbulent, rising-volatility weeks, size them up rather than down, hold through Wednesday, and skip weekend falls in calm weeks.
Why:
- F1: The book is long only from Sunday's close to Monday's close, so it misses most of the rebound it bets on. It holds a position on 40.5 % of Sunday bars and on no other weekday except 0.04 % of Fridays. Trades last a median of 24 hours. After a weekend fall the coin's daily rises are 0.45 % on Monday, 0.08 % on Tuesday and 0.30 % on Wednesday, a 3-day rise of 0.82 % (n=1198), of which the book captures only the first day.
- F3: The rebound sits almost entirely in high-volatility weeks. Among weekend-fall Sundays, the excess Sunday-to-Wednesday return is 2.55 % (t=4.18, n=318) in each coin's top tercile of 20-day volatility, against -0.03 % (t=-0.09, n=318) and 0.08 % (t=0.19, n=310) in the lower two terciles.
- F4: The same holds for volatility rising against its own past. The excess 3-day return is 2.15 % (t=3.16, n=188) in the top tercile of 20-day over 60-day volatility, against -0.06 % and 0.20 % in the lower two terciles.
- F5: Volatility-target sizing puts the book's largest positions where there is no effect and its smallest where the effect is. The mean position is 0.52 in the low-volatility tercile, which carries 12.8 % of the Sunday gain, and 0.26 in the high-volatility tercile, whose 3-day excess return is about 2.5 %.
- F6: The forecast's own grading adds little once volatility is known. Inside the high-volatility tercile the slope of excess return on forecast is -0.0004 (t=-0.35, n=318), and in the low tercile it is 0.0001 (t=0.13). The overall slope (t=4.2) is carried mostly by the volatility level that goes with large falls.
