---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high
line: 7.d not profitable
backtest: 020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close sits below its highest close of the past 90 days, the more it rises over the next 5 days, the rise growing with the percent distance of the close to that high itself. A close that is only nearer than it was over the past 90 days, but still far below the high, is followed by a fall over the next 5 days.
Consequence: A trader should size the long on how close the price actually is to its 90-day high, not on how close it is compared with its recent past, and should stay out of partial rebounds in a falling coin.
Why:
- F3: Inside the falling legs, nearness to the 90-day high is followed by falls instead of rises. The nearest quintile, held at a position of 1.05, loses 0.32 % per bar, and its 5-day return is -1.27 % (t -2.32, 253 cases); middle nearness is also followed by falls, -1.11 % to -1.79 % (t -2.4 to -3.1). Outside the legs, the nearest quintile is followed by +3.98 % (t 5.51, 449 cases).
- F4: In the bear years 2018 and 2022, closes at middle nearness are followed by the largest falls: quintile 2 by -3.82 % over 5 days (t -4.53, 119 cases), quintile 3 by -3.45 % (t -2.37, 57). The book still holds them at positions of 0.58 and 0.62, against 0.37 and 0.53 over all years. Its forecast is standardised against nearness's own last 90 values, so a partial rebound in a falling market reads as "near".
- F6: The year the book lost most, 2018, is also the year the move after its positions was most negative: it lost 0.155 % per bar, and the 5-day return after its bars was -1.71 % (t -2.54, 426 cases).
- F7: The idea is large enough for its cost: its total move is 1.19 % per case, 6.2 times a round trip, and its unusual move 3.1 times. The failure is in the falls, not in the cost.
