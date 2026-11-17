---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's move over Sunday (UTC close-to-close) is retraced over the following 2 days (Monday and Tuesday), and the retracement is larger the higher the coin's Sunday volume relative to its 20-day average volume.
Consequence: The Sunday reversal trade would be held through Tuesday and sized up when weekend volume was heavy, rather than when it was thin.
Why:
- F1: Over the next 2 days, Sunday's move is undone far more than any other weekday's move: against the Sunday bar's sign the mean excess return is +0.82% (t=5.08, n=2051), and +0.56% on Monday alone (t=4.71). The other six weekdays sit between −0.36% and +0.08% over 2 days, with t from −2.65 to 0.59. All 6 coins and all 8 years point the same way (coin t from 1.23 to 3.28; year means from +0.08% to +1.83%).
- F2: The book catches only part of the reversal in F1, and fees eat that part. It holds a position for Monday only, while about 30% of the 2-day reversal comes after Monday (0.56% against 0.82%). Its Monday mean is +0.080% (t=1.55, n=2484), but it pays a steady −0.041% on Sunday days (t=−19.2), which is the entry fee. On four of the other five weekdays it holds no position at all (mean exactly 0).
- F4: Contrary to the brief, low weekend volume does not deepen the reversal. The 2-day reversal after Sunday by relative-volume tercile is +0.65% when volume is low (t=2.43), +0.84% in the middle (t=3.16) and +0.97% when it is high (t=3.18), with 684, 683 and 684 cases.
