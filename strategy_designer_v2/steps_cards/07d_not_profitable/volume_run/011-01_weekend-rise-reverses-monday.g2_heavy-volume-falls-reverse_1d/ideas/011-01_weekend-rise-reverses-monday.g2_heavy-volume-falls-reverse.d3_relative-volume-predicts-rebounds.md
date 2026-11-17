---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Any one-day fall in a coin is followed over the next 3 days by a rise that grows with that day's volume compared with its 60-day average volume. The most heavily traded down days rebound the most.
Consequence: A trader can buy down days in proportion to their relative volume, and should avoid buying those made on thin volume.
Why:
- F2: The rebound is graded by the day's volume ratio, not by the fall: across active-bar volume-ratio quartiles (mean ratio 1.54, 1.83, 2.24, 3.78) the next-day excess return is 0.0026, 0.0073, 0.0099 and 0.0159, and the 3-day excess return is -0.0074, 0.0148, 0.0116 and 0.0327; the Spearman correlation with the next day is 0.071 for volume ratio against 0.046 for the forecast.
- F3: Sizing by fall size starves the book: the lowest forecast quartile holds a mean allocation of only 0.014 yet rebounds 0.0055 the next day, and heavy-volume down days with falls under half a usual move still rebound 0.0059 the next day and 0.0119 over 3 days (n 319, 97 % active); falls of 2 to 3 usual moves rebound less (0.0079, n 178).
- F4: The effect belongs to heavy volume: down days on volume below 0.7 of the 60-day average are followed by -0.0020 the next day and -0.0089 over 5 days (n 3003), while those at 1.5 to 2, 2 to 3, and above 3 times average are followed by 0.0062, 0.0126 and 0.0141 the next day.
