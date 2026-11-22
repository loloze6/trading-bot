---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-04_thinner-weekend-larger-reversal.d1_large-thin-weekend-moves-reverse
line: 7.d not profitable
backtest: 026-04_thinner-weekend-larger-reversal.d1_large-thin-weekend-moves-reverse_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The lower a coin's weekend volume is compared with its volume over the preceding five weekdays, the larger the share of its Saturday-Sunday move that is reversed over Monday and Tuesday (the next 2 days). The reversal is graded by the weekend's thinness alone, whatever the move's size, and turns into continuation over those 2 days when the weekend traded close to its weekdays' volume.
Consequence: A trader would bet against the weekend move at Sunday's close in proportion to how thin the weekend was against its weekdays, and follow it when the weekend was nearly as busy as the week.
Why:
- F2: How thin the weekend was sets the outcome on a graded scale. Thinness is the five weekdays' mean volume over the weekend's mean volume. In its top quartile the weekend move reverses over the next 48 h: weekend rises reverse by +0.219 of a usual move (t 3.55, n 234, total +1.16 %) and weekend falls by +0.060 (t 0.96, n 219, total +0.61 %). In its bottom quartile the move continues instead: falls by -0.200 (t -2.18, n 187, total -1.15 %) and rises by -0.131 (t -1.73, n 267, total -1.21 %).
- F3: The size of the weekend move carries almost nothing. Across Sunday |move| quintiles the 48 h reversal runs from -0.064 (smallest) to +0.045 (largest, t 0.65), and the slope on the clipped move has t -0.13. The raw move × thinness product predicts reversal (slope t -2.78, n 1813), but the book's forecast keeps only t +1.49: its two top |forecast| quintiles sit at the ±20 cap (+0.040 and +0.085 of a usual move), and its smallest quintile loses -0.153.
- F4: The top-thinness reversal is broad. It is positive in 6 of 8 years (2020 +0.347 with t 2.45, 2024 +0.210 with t 2.11; 2021 -0.031, 2023 -0.077) and in 5 of 6 coins (ETH +0.229 with t 2.24, XRP +0.164 with t 2.06; ZEC -0.051).
- F6: The effect belongs to the weekend. The same thinness measure read at Wednesday's close gives 48 h reversals of only -0.043 to +0.032 across its quartiles (all |t| < 1.3). The mean thinness ratio is 1.95 on Sunday against 1.00 on Wednesday.
- F1: The book's loss comes from its short trades and not from fees: 1816 shorts lost a mean 1.42 % per trade before fees, while 1409 longs gained a mean 0.36 %; per case the total move is -0.05 % against a trade cost of 0.19 %, and Sharpe is -0.31.
