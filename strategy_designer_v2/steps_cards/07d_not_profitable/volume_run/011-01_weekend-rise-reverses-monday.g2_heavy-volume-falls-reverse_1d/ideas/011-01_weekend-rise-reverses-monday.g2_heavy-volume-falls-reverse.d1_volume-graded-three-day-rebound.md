---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's large one-day fall made on heavy volume compared with its 60-day average volume is partly undone over the next 1 day, and the heavier that day's volume, the larger the next day's rebound. The rebound carries on over the next 3 days and grows with the volume ratio, whatever the fall's size.
Consequence: A trader should size the rebound trade by how heavy the selling day's volume was, not by how far price fell, and hold it for about three days instead of one.
Why:
- F1: The book fails only on size: its mean daily return is 0.000423 against the 0.0005 needed, because it is active on just 8.7 % of bars (1523 of about 17,500), holds a mean allocation of 0.64 there, and earns 0.0061 per active bar.
- F2: The rebound is graded by the day's volume ratio, not by the fall: across active-bar volume-ratio quartiles (mean ratio 1.54, 1.83, 2.24, 3.78) the next-day excess return is 0.0026, 0.0073, 0.0099 and 0.0159, and the 3-day excess return is -0.0074, 0.0148, 0.0116 and 0.0327; the Spearman correlation with the next day is 0.071 for volume ratio against 0.046 for the forecast.
- F3: Sizing by fall size starves the book: the lowest forecast quartile holds a mean allocation of only 0.014 yet rebounds 0.0055 the next day, and heavy-volume down days with falls under half a usual move still rebound 0.0059 the next day and 0.0119 over 3 days (n 319, 97 % active); falls of 2 to 3 usual moves rebound less (0.0079, n 178).
- F5: The rebound keeps going past the one day the book holds: excess returns on active bars are 0.0087 at 1 day (t 5.61), 0.0124 at 3 days and 0.0137 at 5 days (n 1488), with day 2 adding 0.0023 (t 1.55); on a non-overlapping 3-day grid, heavy-volume down days gain 0.0259 (t 4.84, n 397).
