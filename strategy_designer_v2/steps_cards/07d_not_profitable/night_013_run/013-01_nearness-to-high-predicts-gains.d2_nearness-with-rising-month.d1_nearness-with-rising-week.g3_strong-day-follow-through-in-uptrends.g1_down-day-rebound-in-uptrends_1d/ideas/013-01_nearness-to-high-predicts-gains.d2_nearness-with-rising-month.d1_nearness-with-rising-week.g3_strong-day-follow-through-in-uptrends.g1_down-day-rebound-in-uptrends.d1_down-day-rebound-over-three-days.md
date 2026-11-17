---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends.g1_down-day-rebound-in-uptrends
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends.g1_down-day-rebound-in-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is positive, the larger its latest one-day fall relative to its 30-day daily volatility, the higher its return over the next 3 days.
Consequence: After a sharp down day inside an up-month, a trader should expect the rebound to unfold over several days rather than the next day alone, and keep the long through it.
Why:
- F1: The book's deepest fall, 24.0% over 380 days from w20 to w23, came while holding the coins gained: the book summed -0.263 in daily returns while holding summed +0.861, and in w20–w24 the position's gain before costs averaged -0.000155 per bar against +0.000523 in w1–w19, while the coin itself rose 0.002529 per bar against 0.000836.
- F2: In w20–w24 the active bars' rebound came after the 1-day horizon: next-1-day return 0.000369, next-3-day 0.009113 and next-5-day 0.020980 (n=815), against 0.002961, 0.005315 and 0.005711 in w1–w19 (n=3054); positions were held about 2.0 days on average.
- F3: On the active bars as a whole, the forward return keeps building past one day, with 0.0024 at 1 day (t 3.09, n 3839), 0.0061 at 3 days (t 4.33) and 0.0089 at 5 days (t 4.82); with non-overlapping samples on down days inside a rising month, the fall-size slope is t 2.64 at 1 day (n 2961) and t 2.06 at 3 days (n 959).
