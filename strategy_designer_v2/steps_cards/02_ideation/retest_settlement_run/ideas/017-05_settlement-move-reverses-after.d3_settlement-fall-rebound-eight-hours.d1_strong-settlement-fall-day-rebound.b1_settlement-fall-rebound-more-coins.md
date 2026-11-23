---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound
line: 7.b inconclusive
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: The return over the 24 hours after the 00:00 and 16:00 UTC funding settlement times runs opposite to a fall over the 2 hours before it, and the larger the fall against the coin's usual 2-hour move, the larger the rise, with the largest falls carrying almost all of the rebound.
Consequence: A trader buys only the large settlement falls and holds the rebound for a day, so that each trade captures several times its cost instead of paying a full cost on small falls that do not rebound.
Why:
- F1: The supporting check failed because the forecast saturates, not because the rebound is ungraded: 6034 of the 8564 cases sit at a forecast of 10 or more, and that top group mixes falls of only 1 to 1.5 usual 2-hour moves (1899 cases, +0.02 %, t 0.17) with falls deeper than 4 usual moves (511 cases, +1.09 %, t 3.56), so the two groups differ by -0.02 % while the main measure stands at +0.24 % with t 4.16.
- F2: Measured on the depth of the fall itself, the settlement-bar rebound is graded as the idea says: the excess 24-hour return is +0.80 % (t 3.91, n 1103) for falls of 3 or more usual moves, +0.30 % (t 2.19, n 1406) for 2 to 3, +0.35 % (t 2.49, n 1331) for 1.5 to 2, +0.07 % (t 0.68, n 2335) for 1 to 1.5, and -0.05 % to -0.19 % after small falls and rises; the Spearman correlation of depth with excess return over the cases is 0.050 (p 2e-6).
- F5: The settlement cases are mixed across coins and years. By coin they range from BTC +0.00 % (t 0.02, n 1533) to XMR +0.30 % (t 2.48) and ZEC +0.31 % (t 1.96). By year they range from 2020 +0.71 % (t 4.43) to 2022 -0.32 % (t -2.48), and 2025 is -0.11 %. Six coins give too few independent cases per coin to show the graded tail clearly.
- F7: On average the move is too small to pay, but the deepest falls clear the cost. The unusual move is +0.16 % per case, 0.8 times the 0.19 % cost of a trade, and the total move is +0.30 %, 1.6 times the cost; the book's Sharpe is 0.42, 0.135 below holding, with a Calmar of 0.15. The settlement falls of 3 or more usual moves move +0.80 %, about 4 times the cost.
