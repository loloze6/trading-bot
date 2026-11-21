---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_weekly-rise-keeps-running
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_weekly-rise-keeps-running_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The straighter a coin's 7-day rise, meaning the larger its net 7-day move compared with the sum of its hourly up and down moves, the more the coin rises over the next 3 days.
Consequence: A weekly rise built by a steady hourly grind is a reason to stay long for the next days, more so than an equally large but choppy rise.
Why:
- F4: How the 7-day move was made does carry information about the next 3 days. Holding the 7-day return fixed, the path's efficiency (net 7-day move over the sum of absolute hourly moves) gains +31 bps of 3-day excess per standard deviation (t 2.66, 5251 cases), while the 7-day return itself falls to t 1.1. The straightest third of 7-day rises is followed by +79 bps of 3-day excess (t 2.5, 893 cases), against -20 bps for the least straight third.
- F5: The grind effect in F4 is not stable. It sits in the later half of the windows (+57 bps per sd, t 3.2) and not the earlier half (+8 bps, t 0.5). It is mostly XRP (t 3.1) and ZEC (t 2.0), with LTC and XMR negative. It is negative in 2022 (t -2.0).
- F6: The tested 7-day rise alone barely predicts the next 3 days' excess return. Its slope is +16 bps per sd (t 1.4); it is significant only on XRP and ZEC (t 2.2 each) and negative on LTC (t -1.8). Its size is -0.04 % of unusual move per case, so the book's gain comes from the coin's drift (+0.41 %), not timing.
