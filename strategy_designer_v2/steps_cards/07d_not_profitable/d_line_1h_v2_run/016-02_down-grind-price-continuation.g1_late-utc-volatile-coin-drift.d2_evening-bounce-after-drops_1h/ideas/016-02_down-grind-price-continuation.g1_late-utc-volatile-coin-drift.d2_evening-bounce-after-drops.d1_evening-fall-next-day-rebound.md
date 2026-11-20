---
brief: 016_grind-versus-jump-moves
source-idea: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops
line: 7.d not profitable
backtest: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Each coin rises over the 24 hours after 21:00 UTC, and the larger its fall over the past 24 hours measured in units of its 7-day hourly volatility, the larger that rise.
Consequence: A trader would buy a coin at the 21:00 close after a steep vol-adjusted 24-hour drop and hold it for about a day, so one round-trip fee is paid against a graded move about twice its size, and would refuse the trade after a shallow fall or a rise.
Why:
- F1: Fees, not the forecast, sink the book: the 7,153 trades average a gross gain of 0.0083 (t 0.47, 52.3% winners) against a fee of 0.100, leaving -0.092 net per trade; across all bars the held position earns 1.3e-5 per bar gross while fees cost 1.9e-5 per bar, so the daily book return is -0.000143 while holding the coins earns +0.00119.
- F2: The bounce the book trades is smaller than one round trip even where it is strongest: at the 21:00 bars, the excess 2-hour return is 0.00179 (t 4.58, n 2112) in the deepest-fall quartile and only 0.00126, 0.00064 and 0.00105 in the next three; the book's fee per position is about 0.0011 at entry (0.000224 per hour-20 bar against 41% of those bars in a position at a mean size of 0.51) and about as much again at exit.
- F5: Over a full day after the 21:00 close the fall's effect is graded and large: the excess 24-hour return is +0.00218 (t 1.93) in the deepest-fall quartile, +0.00072 in the second, -0.00091 in the third, -0.00188 (t -1.80) in the shallowest and -0.00086 (t -1.70) after no fall, so the spread is about 0.004, roughly twice a round-trip fee.
- F7: The loss is spread over the whole period, not held in one window: gross position gain is positive in 19 of 24 windows, yet fees exceed gross in 17 of them, and the lowest Sharpe with one window left out is still -0.90.
