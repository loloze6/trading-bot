---
brief: 016_grind-versus-jump-moves
source-idea: 016-08_down-volume-burst-reversal.g1_late-evening-rebound-after-daily-falls
line: 7.g patterns
backtest: 016-08_down-volume-burst-reversal.g1_late-evening-rebound-after-daily-falls_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin rises over the 2 hours after the 20:00 UTC close, and the rise is larger the larger the coin's average absolute hourly return over its past 30 days.
Consequence: A trader would hold, or refuse to short, a coin through the 21–22 UTC hours and expect more from the more volatile coins.
Why:
- F1: Every coin drifts up in the late UTC evening, whatever its past 24 hours did. Hourly returns on bars closing at 21:00 and 22:00 UTC average +5.45bp (t 6.75, n 17403) and +4.36bp (t 5.66, n 17417); no other hour exceeds |t| 3.8. Over those two hours each coin averages +4.2 to +5.5bp (t 3.0 to 4.4), every weekday is positive (t 2.1 to 3.9), 7 of 8 years are positive (2022 is -2.2bp, t -1.4), and 83% of windows have a positive mean.
- F2: The book cannot turn the confirmed 2-hour edge into money. Its 7238 trades last 1.0 hour on median and lose 0.095% before fees (t -7.2) and 0.195% after; every coin is negative after fees (-0.11% to -0.27%). The position held over the bar closing at 21:00 gains only +1.87bp (t 2.38, n 7225), the second positive hour (22:00) is not held, and the round-trip fee of about 0.10% is larger than either.
