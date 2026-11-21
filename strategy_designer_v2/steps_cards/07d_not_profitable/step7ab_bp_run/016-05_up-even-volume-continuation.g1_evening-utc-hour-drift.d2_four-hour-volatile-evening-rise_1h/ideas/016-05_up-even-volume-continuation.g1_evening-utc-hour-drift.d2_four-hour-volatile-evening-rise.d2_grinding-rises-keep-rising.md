---
brief: 016_grind-versus-jump-moves
source-idea: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d2_four-hour-volatile-evening-rise
line: 7.d not profitable
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d2_four-hour-volatile-evening-rise_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin whose price rose over the past 3 days rises further over the next 3 days, and the more of its hourly movement over those 3 days went into the net rise (net 3-day return over the sum of its hourly absolute moves), the larger the further rise.
Consequence: A trader would go long the coins whose 3-day rise was a steady grind and hold for days, a move of about 86 bps against a 19 bps round trip.
Why:
- F5: The brief's grind shows on rises over 3 days. A 3-day rise in the most efficient third is followed by a 3-day unusual move of +86 bps (t 3.03, 1,031 non-overlapping cases), which is 4.5 times the cost of a trade. Efficiency here is the net 3-day move over the sum of its hourly absolute moves. Rises in the least efficient third are followed by -36 bps (t -1.28, 947 cases).
- F6: The grind effect on rises holds in every coin, from +44 bps (ETH) to +197 bps (ZEC) in the most efficient third. It is carried mostly by windows w13 to w24 (+150 bps, against +13 bps in w1 to w12).
- F9: Neither the direction nor the efficiency alone ranks what follows. The Spearman correlation with the next 3-day unusual move is -0.009 for the signed 3-day return and -0.001 for the signed efficiency (5,539 cases). The effect lives in rises that are efficient (F5) and falls that are choppy (F7), not along one signed scale.
