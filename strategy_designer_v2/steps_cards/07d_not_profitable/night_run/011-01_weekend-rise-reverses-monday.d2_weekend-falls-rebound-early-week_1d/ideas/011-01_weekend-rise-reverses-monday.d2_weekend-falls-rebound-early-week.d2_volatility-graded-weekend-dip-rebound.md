---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell over the weekend rises over the next 3 days, and the higher its 20-day volatility of daily returns at Sunday's close, the larger that 3-day rise.
Consequence: Weekend dips are worth buying in proportion to how volatile the coin has been recently, not in proportion to the size of the dip alone.
Why:
- F3: The rebound sits almost entirely in high-volatility weeks. Among weekend-fall Sundays, the excess Sunday-to-Wednesday return is 2.55 % (t=4.18, n=318) in each coin's top tercile of 20-day volatility, against -0.03 % (t=-0.09, n=318) and 0.08 % (t=0.19, n=310) in the lower two terciles.
- F5: Volatility-target sizing puts the book's largest positions where there is no effect and its smallest where the effect is. The mean position is 0.52 in the low-volatility tercile, which carries 12.8 % of the Sunday gain, and 0.26 in the high-volatility tercile, whose 3-day excess return is about 2.5 %.
- F6: The forecast's own grading adds little once volatility is known. Inside the high-volatility tercile the slope of excess return on forecast is -0.0004 (t=-0.35, n=318), and in the low tercile it is 0.0001 (t=0.13). The overall slope (t=4.2) is carried mostly by the volatility level that goes with large falls.
