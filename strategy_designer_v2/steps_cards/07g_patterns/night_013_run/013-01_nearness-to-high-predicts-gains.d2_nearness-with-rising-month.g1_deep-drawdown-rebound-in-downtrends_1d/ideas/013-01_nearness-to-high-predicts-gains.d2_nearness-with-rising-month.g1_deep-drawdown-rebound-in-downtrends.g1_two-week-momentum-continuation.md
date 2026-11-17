---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 14-day return, the higher its return over the next 7 days.
Consequence: A trader would lean long the coins that rose most over the past two weeks and avoid holding those that fell most, rather than buying the deep fallers.
Why:
- F1: Across all bars on the non-overlapping 7-day grid, a coin's 14-day return predicts its 7-day forward excess return with slope 0.0515 (t 3.77, n 2155 independent cases). Its 30-day return does the same more weakly: slope 0.0248 (t 2.88, n 1723), and a per-coin rank version still gives t 2.51.
- F2: The 30-day momentum is uneven, not steady. It is strong in 2025 (t 4.24) and in ZEC (t 2.80), reversed in 2018 (t -3.88), and between -1.3 and +1.1 in the other years and coins. The 60-day return carries nothing (slope -0.003, t -0.54, n 1147), so the effect sits in the last two to four weeks.
- F3: The tested depth relation is not monotone when the 30-day return is negative. Only the deepest fifth below the 60-day high is followed by a positive excess (+0.0208, t 1.74, n 166). The next fifth is the worst (-0.0281, t -2.65), and the fifth closest to the high is -0.0076 (t -1.10). This matches the step-5 slope of t -0.37 and the book's mean daily return of 8.4e-05.
- F6: Closes at a new 60-day high are followed by a 7-day excess of +0.0198 (n 158), against -0.0014 for the other bars. The Welch t is 1.44, so the brief's breakout continuation is in the right direction but not distinct from chance.
