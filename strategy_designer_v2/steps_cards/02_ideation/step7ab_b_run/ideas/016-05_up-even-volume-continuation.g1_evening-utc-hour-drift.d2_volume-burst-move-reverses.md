---
brief: 016_grind-versus-jump-moves
source-idea: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift
line: 7.d not profitable
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger the share of a coin's past 3-day volume traded in its single busiest hour, the more of its 3-day move the coin gives back over the next 7 days.
Consequence: A 3-day move built on one volume burst is a reason to lean against it for a week rather than follow it.
Why:
- F8: Moves made with volume bunched into one hour lean toward giving back. Take the share of the past 3 days' volume traded in its biggest hour:
- F5: Three-day moves made efficiently tend to continue (efficiency is the net 3-day return over the sum of its absolute hourly returns). In the most efficient fifth, the move continues by +91.6 bps over the next 3 days (t 3.3, 1,108 non-overlapping cases) and +104 bps over 7 days (t 2.3). That is 4.4 times a round trip.
