---
brief: 016_grind-versus-jump-moves
source-idea: 016-05_up-even-volume-continuation
line: 7.g patterns
backtest: 016-05_up-even-volume-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the more directly its price climbed, the more it keeps rising over the next 3 days. Directness is the 3-day net move as a share of the sum of its absolute hourly moves.
Consequence: Rises built from steady same-direction hourly steps are worth holding for several more days, while choppy rises of the same size are not.
Why:
- F2: On up moves, the 3-day path efficiency predicts the next 3 days. Efficiency is the net 72-hour log move over the sum of absolute hourly moves. On the non-overlapping 72-bar grid, the top third minus the bottom third of excess forward return is +0.0092 − (−0.0032), Welch t 3.06, n 2865. All six coins are positive on the up side (t 0.88 to 2.18). Inside size terciles of the rise the sign holds but each tercile is weak alone (t 1.13, 0.73, 1.21). In a regression with size and volatility, the past × efficiency term is zero (t −0.01). Much of this effect is therefore the size of the rise.
- F3: The volume evenness that the book trades on adds almost nothing on the same grid. Up moves give top minus bottom excess 0.0027 − (−0.0008), t 0.87, and down moves give t −0.21. The book loses: Sharpe −0.32 and mean daily return −0.00018. Three of six coins lose money (XMR −0.00122/day, LTC −0.00059, ZEC −0.00013) while every coin's holding gains 0.0007 to 0.0016/day.
