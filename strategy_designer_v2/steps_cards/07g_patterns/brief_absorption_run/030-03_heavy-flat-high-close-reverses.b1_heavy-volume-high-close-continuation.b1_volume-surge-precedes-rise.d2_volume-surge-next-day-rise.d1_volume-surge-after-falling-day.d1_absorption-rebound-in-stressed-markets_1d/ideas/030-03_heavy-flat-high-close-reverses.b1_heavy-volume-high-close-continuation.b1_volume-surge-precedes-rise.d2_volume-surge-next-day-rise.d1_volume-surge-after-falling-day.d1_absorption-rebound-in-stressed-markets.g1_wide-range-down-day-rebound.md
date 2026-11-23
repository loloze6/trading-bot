---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d1_absorption-rebound-in-stressed-markets
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d1_absorption-rebound-in-stressed-markets_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The wider a coin's high-low range on a down day relative to its average daily range over the prior 20 days, the more the coin rises over the next 2 days, the more so when its 20-day volatility runs high against its 4-month volatility.
Consequence: A trader buys down days by how far their range exceeds the recent norm rather than by their volume, and refuses rebound trades on narrow-range down days.
Why:
- F1: On down days, the day's range against its prior 20-day mean range carries the next-day rebound by itself: by range quintile per coin the next-day excess return is -0.15 % (t -1.35), -0.15 %, +0.18 %, +0.23 % and +0.87 % (t 5.76, n 1569). In a down-day regression that also holds the fall, the volume ratio and the close location, only the log range ratio is significant (beta 0.0050, t 2.65); the fall (t -0.72) and the volume ratio (t 0.47) add nothing.
- F2: The wide-range rebound lasts beyond one day. On non-overlapping grids, top-quintile down days gain +1.32 % excess over 2 days (t 4.68, n 824), against -0.59 % (t -2.75) for the narrowest quintile. Top-third down days gain +0.85 % over 3 days (t 2.43, n 781), against -0.63 % (t -2.26) for the bottom third.
- F3: Range explains the book's own forecast. Among the top-third forecast down days, the narrow-range cases earn -0.29 % (n 80) and the wide-range cases +0.76 % (t 5.33, n 1857). Wide-range down days are positive in all 6 coins (+0.28 % to +0.78 %, t 1.6 to 2.8) and in all 8 years (+0.03 % to +1.65 %). They are stronger when the 20/120-day volatility ratio is above its median (+0.71 %, t 3.78) than below it (+0.19 %, t 1.25).
- F6: The size of the wide-range down-day move clears the cost of a trade, unlike the tested idea's per-case move. The top range quintile's next-day excess is +0.87 %, about 4.6 times the 0.19 % cost. The tested idea's unusual move was +0.15 % per case, 0.8 times the cost.
