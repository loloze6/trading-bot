---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close sits to its highest close of the past 52 weeks, the higher its return over the next 7 days, only while its 30-day return is positive. Inside that state, the higher the 30-day return and the higher its 7-day return, the larger the gain.
Consequence: Weight the near-high signal by the past week's rise as well as the past month's. This concentrates exposure where the gain is and away from the faded-momentum days that hold the falls.
Why:
- F1: The book's gain comes only from the top fifth of its forecasts. Trending bars in forecast quintile 4 (mean forecast 8.3, allocation 0.48) earn 0.00223 per bar. Quintiles 0 to 2 earn between -0.00008 and 0.00013, although their next-day coin return rises from 0.00006 to 0.0018.
- F4: The falls come when the coin's recent move has faded, and in calmer markets.
- F5: Among long bars, the gain is graded by the coin's own past 7-day return.
- F6: Nearness to the high does predict 7-day excess returns inside the regime, with slope 0.00037, t 2.15 and 1013 non-overlapping cases. The top nearness fifth returns 3.2% over 7 days against about 0.9% in the farthest two fifths.
