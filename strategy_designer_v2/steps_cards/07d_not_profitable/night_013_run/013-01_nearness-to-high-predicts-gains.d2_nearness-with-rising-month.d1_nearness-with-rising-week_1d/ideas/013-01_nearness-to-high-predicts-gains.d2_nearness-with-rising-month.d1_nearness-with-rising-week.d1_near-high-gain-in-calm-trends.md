---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close sits to its highest close of the past 52 weeks, the higher its return over the next 7 days, only while its 30-day return is positive; inside that state, the higher the 30-day return and the higher its 7-day return, the larger the gain, and the gain is larger still the lower the coin's daily-return volatility over the past 60 days.
Consequence: Put the largest long exposure on calm, rising coins near their high, where the forecast's following move is about twice as large, rather than spreading it evenly across volatility.
Why:
- F1: The book earns a mean daily return of 0.000366 while the coins themselves average 0.001315, because the book is barely exposed: its mean position is 0.072, it is flat on 46% of bars and short on 21%, and long bars carry 99.8% of its gain (coin next-bar return 0.00295 when long, against 0.00053 when short and 0.00052 when flat).
- F2: In the trending regime the gain sits almost entirely in the top forecast fifth (next-bar coin return 0.0056, gain 0.0035 per bar, mean position 0.60), while the bottom fifth holds a mean short of -0.25 as the coin still rises 0.0007 per bar and earns only 0.0001, and the middle fifths earn between -0.00003 and 0.0006.
- F4: Among trending bars with a forecast above 6, the calmest third of realised volatility (0.47) sees a next-bar coin return of 0.0070, against 0.0035 and 0.0032 in the middle (0.73) and most volatile (1.19) thirds, so the signal's move is about twice as large where volatility is low.
