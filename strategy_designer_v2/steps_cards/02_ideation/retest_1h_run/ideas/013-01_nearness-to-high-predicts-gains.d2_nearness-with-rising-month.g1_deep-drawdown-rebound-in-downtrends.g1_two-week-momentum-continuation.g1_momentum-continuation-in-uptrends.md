---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Among coins whose 60-day return is positive, the larger a coin's 14-day rise, the higher its return over the next 7 days.
Consequence: A trader would add to long positions in proportion to the two-week rise while the coin's two-month trend is up, rather than taking the short side of the same signal.
Why:
- F1: The book's whole timing gain sits on its long side: long bars earn 0.00121 a day above the coin's mean drift (t 3.61, n 8559), while short bars earn 0.000025 (t 0.10, n 8762), and short bars lose 0.00048 a day in raw gain (t -1.87).
- F2: In each coin the short side's raw bar gain is at or below zero (BTC -0.0003, LTC -0.0007, XMR -0.0011, XRP -0.0006, ZEC -0.0002, ETH +0.00007), while the long side's is positive in all six (from 0.00008 for LTC to 0.0040 for XRP).
- F3: The forecast's edge does not rise steadily with the 14-day return. Coins in the 2nd and 3rd ret14 deciles (14-day falls of roughly 7–19 %) lose 3.0 % and 2.2 % more than their coin's mean over the next 7 days (t -3.14 and -2.82). That loss shows in all six coins (-1.9 % to -3.2 %). The deepest-fall decile is flat (+0.3 %, t 0.36, n 216). On the rising side, deciles 9–10 gain +1.9 % and +2.4 % (t 2.04 and 1.79).
- F4: Among rising coins the 14-day return still sorts the next 7 days (slope 0.071, t 2.58, n 581). Among coins whose 60-day return is negative, the slope is weaker (0.060, t 1.63, n 566).
