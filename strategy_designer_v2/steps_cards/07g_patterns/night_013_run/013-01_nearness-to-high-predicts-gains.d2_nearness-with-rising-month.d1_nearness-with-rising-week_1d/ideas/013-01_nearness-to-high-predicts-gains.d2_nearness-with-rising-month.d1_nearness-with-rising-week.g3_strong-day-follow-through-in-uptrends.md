---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is positive, the larger its latest one-day return relative to its 30-day daily volatility, the higher its return over the next 7 days.
Consequence: In an up-month, add to coins after an unusually strong day instead of fading the move.
Why:
- F5: A large one-day move scaled by the coin's 30-day volatility is followed by gains only in the trending state. The top quintile of this move has a 7-day excess return of +0.0176 (t 2.21, n 392). The rank slope is t 2.68 when the 30-day return is positive (n 1,013) and t 0.44 otherwise (n 945).
- F7: The book's whole gain comes from the trending state: the summed bar gains are 7.25 there against -0.005 in the flat state. Within the trending state, the 30-day return adds little to the 7-day forecast (rank t 0.72), while the 7-day return carries it (t 3.18).
