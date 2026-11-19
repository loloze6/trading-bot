---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound
line: 7.g patterns
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days, the larger its fall over the last 1 day, the more it rises over the next 1 day, with most of the rebound coming from the sharpest falls.
Consequence: Buying a fresh sharp drop in a decline pays within a day, so a held position that churns several times a day for three days gives the edge back in fees.
Why:
- F1: The book loses because of costs, not because the signal points the wrong way: fees run 0.0010–0.0015 a day per coin while the position's gross gain ranges from -0.00053 (ETH) to +0.00090 (XMR) a day, at 3.1–3.5 trades a day, so every coin's book is negative (-0.0006 to -0.0015 a day) while holding earns +0.0007 to +0.0016 a day.
- F2: In a 3-day decline the rebound is not graded across the range but sits in the deepest 1-day falls: the lowest 24h-return quintile earns an excess 72h return of +0.0126 (t 3.15, n 536), the next three quintiles earn -0.0075 (t -2.14), -0.0068 and -0.0058, and only deciles 0 and 1 are positive (+0.0142, t 2.45; +0.0114, t 2.07, n 267 each); this is what drives the pooled slope t of -4.34 on r24.
- F3: That deep-fall rebound comes mostly within the first day: the lowest quintile's excess 24h return is +0.0121 (t 4.48, n 536), about the same size as its whole 72h excess, and it holds in both halves of the windows (72h: w1-12 t 1.88, w13-24 t 2.63) and in 5 of 6 coins (BTC alone negative at -0.0026).
- F4: After a 3-day rise, the size of the last 1-day move predicts nothing (slope t 0.27, every quintile |t| < 1.32), so the fresh-move effect exists only inside declines.
