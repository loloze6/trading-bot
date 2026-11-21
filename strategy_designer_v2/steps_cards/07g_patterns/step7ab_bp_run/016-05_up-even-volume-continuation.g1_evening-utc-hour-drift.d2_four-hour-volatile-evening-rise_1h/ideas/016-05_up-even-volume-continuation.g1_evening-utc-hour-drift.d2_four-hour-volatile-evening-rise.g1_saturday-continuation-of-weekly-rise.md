---
brief: 016_grind-versus-jump-moves
source-idea: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d2_four-hour-volatile-evening-rise
line: 7.g patterns
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d2_four-hour-volatile-evening-rise_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the 24 hours of Saturday (UTC), a coin keeps moving in the direction of its 7-day return, and the larger its 7-day return relative to its 7-day hourly volatility, the larger its rise over that day.
Consequence: A trader can hold a coin long through Saturday after a strong week, sized up with the strength of that week, and refuse the Saturday long after a weak week; one round trip per week is a small cost against a move several times its size.
Why:
- F1: Saturday's UTC day continues the past week's move: across the 6 coins, the 24 hours from Saturday's 00:00 UTC open gain +84.8 bps beyond the coin's normal daily drift when the coin's 7-day return is in its top third (t 4.65, 770 days), against -13.8 bps in the bottom third (t -1.00). Top minus bottom is +98.6 bps, the largest spread of any weekday; the next largest are Tuesday's +56.8 and Friday's +33.8.
- F2: The Saturday continuation is graded and belongs to Saturday alone: the correlation of the next day's standardised unusual move with the 7-day return scaled by 7-day volatility is 0.126 on Saturdays (2304 days), against 0.008 on all other days.
- F3: The Saturday top-third continuation is positive on every coin, from +26 bps on BTC (t 1.21) to +164 bps on XRP (t 2.31), and in 6 of 8 years (2018 -25 bps, 2023 -33 bps; 2020 +126 bps, 2021 +180 bps, 2024 +136 bps). It is positive in only 62.5 % of the 24 windows, so it comes in bursts.
- F4: The Saturday continuation is far larger than a trade's cost: +85 bps of unusual move per case over 24 hours is about 4.5 times the 19 bps round trip this backtest applied. The tested evening idea's +9 bps over 4 hours is 0.4 times that cost.
