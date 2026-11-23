---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.d2_sunday-falls-rebound-early-week
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.d2_sunday-falls-rebound-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's fall over the past 24 hours, measured in units of its usual 24-hour move over the past 30 days, is followed over the next 24 hours by a rise, the larger the deeper the fall, on any day of the week.
Consequence: A trader would buy a coin after an unusually deep one-day fall, on any weekday, and hold it a day, since the deepest falls rebound about three times the cost of a trade.
Why:
- F1: Measured on every weekday, a coin's one-day fall in units of its 30-day mean absolute daily move is followed by a next-day excess return that grows with the fall: slope +0.0028 per unit, t 5.40, 7057 falling days. The bottom decile (mean −2.6 units) earns +0.60 % next day, t 4.04, n 1436, and the second decile +0.31 %, t 2.57. Rises show no slope (−0.00016, t −0.39, n 7286).
- F2: The next-day rebound after bottom-decile falls is positive in all 6 coins, from +0.24 % (BTC, t 0.87) to +0.96 % (ZEC, t 2.32) and +0.95 % (XMR, t 3.10). It is also positive in all 8 years, from +0.08 % (2019) to +1.63 % (2021, t 2.91), so no single coin or year carries it.
- F3: The rebound is not confined to the weekend. Bottom-decile falls on weekdays rebound +0.52 % next day (t 3.26, n 1206) and on weekends +1.03 % (t 2.55, n 230). The next-day correlation with the scaled move is negative from Tuesday to Thursday and on Saturday and Sunday (t −2.3 to −4.3), and positive only after Mondays (+0.057, t 2.58). The brief's weekend-only mechanism therefore does not separate from a general reversal of large daily falls.
