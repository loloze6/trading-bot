---
brief: 016_grind-versus-jump-moves
source-idea: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d2_four-hour-volatile-evening-rise
line: 7.d not profitable
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d2_four-hour-volatile-evening-rise_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 3-day move continues in its direction over the next 3 days, and the more evenly its volume was spread across the hours of that move, the larger the continuation.
Consequence: A trader would follow multi-day moves built on evenly spread volume and refuse those built on a single burst of volume, which tend to give back part of the move.
Why:
- F8: Volume concentration points the same way as the brief. A 3-day move whose volume is least concentrated in its largest hour continues by +41 bps in its direction over the next 3 days (t 1.82). One whose volume is most concentrated reverses by -17 bps (t -1.00), from about 1,846 cases per third.
- F5: The brief's grind shows on rises over 3 days. A 3-day rise in the most efficient third is followed by a 3-day unusual move of +86 bps (t 3.03, 1,031 non-overlapping cases), which is 4.5 times the cost of a trade. Efficiency here is the net 3-day move over the sum of its hourly absolute moves. Rises in the least efficient third are followed by -36 bps (t -1.28, 947 cases).
