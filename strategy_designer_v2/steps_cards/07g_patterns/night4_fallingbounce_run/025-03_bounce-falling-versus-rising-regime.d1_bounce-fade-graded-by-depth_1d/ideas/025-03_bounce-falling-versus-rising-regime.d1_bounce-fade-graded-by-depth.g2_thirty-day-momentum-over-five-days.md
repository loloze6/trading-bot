---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-03_bounce-falling-versus-rising-regime.d1_bounce-fade-graded-by-depth
line: 7.g patterns
backtest: 025-03_bounce-falling-versus-rising-regime.d1_bounce-fade-graded-by-depth_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In one coin, the return over the next 5 days is higher the higher its 30-day return lies in usual daily moves. Coins below zero drift under their normal drift, and coins above it drift over.
Consequence: A trader would lean long coins with a strong month and short coins with a weak month, in proportion to the month's move in usual daily moves, for about 5 days.
Why:
- F4: Across all grid bars, the 30-day return in usual daily moves predicts the next 5-day return above drift with r 0.060 (t 3.04, 2555 cases). The 1-day move in usual daily moves predicts it with r 0.046 (t 2.54, 2987 cases).
- F5: Quiet days (1-day move between -1 and +1 usual moves) in coins with a negative 30-day return are followed by a 5-day return 0.73 % below drift (928 cases, t -2.15). With a positive 30-day return they are followed by +0.34 % (930 cases, t 0.99).
- F1: On the non-overlapping 5-day grid, a one-day rise of more than 1 usual daily move in a coin whose 30-day return is positive is followed by a 5-day return 2.89 % above the coin's normal drift (236 cases, t 3.41). The same rises in coins with a negative 30-day return are followed by +0.38 % (116 cases, t 0.43).
