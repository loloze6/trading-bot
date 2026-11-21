---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.d3_failed-break-in-downtrend
line: 7.g patterns
backtest: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.d3_failed-break-in-downtrend_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 10-day return relative to its recent daily volatility, the further it moves in the same direction over the next 10 days, beyond its normal drift.
Consequence: Trade a coin in the direction of its own volatility-scaled 10-day move rather than against it, and refuse to fade a strong 10-day move.
Why:
- F1: Over 10 days, a coin's own past 10-day return predicts its next 10-day move in the same direction, and the larger the past return the larger the move. On the non-overlapping 10-day grid of all six coins (1403 cases), the drift-removed next 10-day move rises with the past 10-day return scaled by the coin's 20-day volatility (slope 0.091 of a usual move per unit, t 3.6). By quintile of the past 10-day return, the unusual move goes from -1.5 % (t -2.0, 306 cases, second quintile) to +2.4 % (t 2.3, 312 cases, top quintile). That top-quintile move is about 12 times the 0.19 % round-trip cost.
- F2: The 10-day continuation points the same way on all six coins (slopes 0.009 to 0.181), but it is strong on only one. Only XRP reaches t 3.0 (234 cases), ZEC is at t 1.8, and LTC is near zero (t 0.13).
- F3: The continuation depends on the period. It is strong in 2020 (slope 0.255, t 3.4) and 2024 (slope 0.148, t 2.5, about 175 cases per year). It is weakly negative in 2018, 2022 and 2023 (t -0.58, -0.88, -0.94). It is a trending-market effect, not a constant one.
- F4: The tested idea's situation runs against this continuation. Breaks above a past swing-high close during a 20-day fall are followed by a 10-day unusual move of -0.4 % (t -0.54, 397 cases), not the decline the idea expects in a way that pays. The 1148 short trades lost 3.15 % each on average after fees (median -1.65 %).
- F5: Closes above a past swing-high close during a 20-day rise continue, but the level itself adds nothing.
