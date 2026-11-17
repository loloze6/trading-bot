---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is positive, the larger its one-day returns relative to its 30-day daily volatility, averaged over its last 7 days, the higher its return over the next 7 days.
Consequence: In an up-month, lean into coins whose past week was made of unusually strong days, and keep that view for the week instead of re-trading each day's move.
Why:
- F1: The book's loss is fees, not the forecast: before fees the book earns -0.000013 per bar against a mean fee of 0.000380 per bar, leaving -0.000395 per bar, about the book's -0.000392 mean daily return; on trending bars the fee is 0.000728 per bar against a gain of -0.000024.
- F2: The forecast changes far faster than its 7-day effect: the position turns over 0.35 of the book per bar, the forecast changes sign on 58% of trending bars, and its lag-1 autocorrelation is -0.077, so the book re-trades a 7-day forecast every day.
- F3: Over the 1 day the book actually holds, the forecast points the wrong way: on trending non-overlapping 1-day cases the slope is -0.000052 (t -1.08, n 8624), and the next-day return is 0.0024 after negative forecasts against 0.0013 after positive ones; the edge appears only at 7 days (slope 0.00110, t 3.04, n 1215) and 14 days (slope 0.00162, t 1.94, n 585).
- F5: The slow part of the same measure predicts better: the 7-day mean of one-day returns over 30-day volatility has a 7-day slope with t 4.56 (n 955), against t 3.12 for the latest day alone and t 3.04 for the forecast. Its quintiles rise in order, with 7-day excess returns of -0.011, -0.013, +0.003, +0.014 and +0.028.
