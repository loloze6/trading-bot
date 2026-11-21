---
brief: 016_grind-versus-jump-moves
source-idea: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops
line: 7.d not profitable
backtest: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin rises over the next 24 hours after a fall over the past 24 hours, and the larger that fall measured in units of its 7-day hourly volatility, the larger that rise.
Consequence: A trader would buy a coin after a steep vol-adjusted 24-hour drop at any hour and hold it for about a day, and would refuse the trade when the coin has not fallen.
Why:
- F5: Over a full day after the 21:00 close the fall's effect is graded and large: the excess 24-hour return is +0.00218 (t 1.93) in the deepest-fall quartile, +0.00072 in the second, -0.00091 in the third, -0.00188 (t -1.80) in the shallowest and -0.00086 (t -1.70) after no fall, so the spread is about 0.004, roughly twice a round-trip fee.
- F6: Across every hour of the day, the deepest quarter of vol-scaled 24-hour falls is followed by a positive excess 24-hour return at 23 of 24 hours, from 0.0050 to 0.0068 at hours 0 to 5, against 2-hour excesses that change sign from hour to hour (-0.0012 to +0.0024).
- F1: Fees, not the forecast, sink the book: the 7,153 trades average a gross gain of 0.0083 (t 0.47, 52.3% winners) against a fee of 0.100, leaving -0.092 net per trade; across all bars the held position earns 1.3e-5 per bar gross while fees cost 1.9e-5 per bar, so the daily book return is -0.000143 while holding the coins earns +0.00119.
