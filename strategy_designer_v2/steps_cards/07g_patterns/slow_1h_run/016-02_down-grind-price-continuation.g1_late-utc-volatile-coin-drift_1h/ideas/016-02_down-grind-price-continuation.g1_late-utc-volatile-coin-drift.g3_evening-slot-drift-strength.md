---
brief: 016_grind-versus-jump-moves
source-idea: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift
line: 7.g patterns
backtest: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Each coin rises over the two hours from 21:00 to 23:00 UTC, and the rise held on a day is larger when the coin's daily drift over the past 30 days has been higher, so that the slot gain is large enough per trade to matter.
Consequence: A trader can take the evening slot long only with enough size and conviction to beat the round-trip fee, since the gross slot gain alone is smaller than its cost.
Why:
- F1: The 21:00–23:00 UTC rise the tested idea uses is real in the bars and broad. The hour starting 20:00 averages +5.45 bp (t 6.75, n 17403) and the hour starting 21:00 averages +4.36 bp (t 5.66). Together the two hours are positive in all 6 coins (+4.2 to +5.5 bp, t 2.98 to 4.44) and in 7 of 8 years; the exception is 2022 (−2.18 bp, t −1.44).
- F2: The book loses because its fees are larger than its gross gain, not because the slot drift is absent. Summed per-bar gross gains are positive for every coin (+0.98 to +1.69), while summed fees are larger for every coin (2.53 to 3.49). The book only earns in the 20:00 and 21:00 bars (+1.96 and +2.49 bp per bar on average).
