---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The 3-hour return from 22:00 to 01:00 UTC, relative to the coin's usual 3-hour move, is followed by a move the opposite way over the next 24 hours. The larger the night move in usual moves, the larger the move back.
Consequence: A trader would fade a coin's late-night move at the 01:00 UTC close and hold for a day, with no reason to hold it longer.
Why:
- F1: The vol-scaled 2-hour return closing at 01:00 UTC reverses over the next 24 hours more strongly than the tested 00:00 one. The slope is -27.7 bps per usual move (t -7.4, 17096 daily cases) against -15.3 bps (t -4.1) at 00:00 and -18.5 bps (t -5.1) at 02:00. The largest third of cases reverses by 46 bps (t 6.8), and over 3 hours (22:00 to 01:00 closes) by 51 bps (t 7.4), about 2.4 to 2.7 times the 0.19 % cost. No other hour of the 24 scanned comes close: the next strongest are 18:00 to 21:00 closes at t -2.0 to -2.4. The pooled t's are overstated because the 6 coins move together.
- F2: The 01:00 reversal does not last beyond a day. Over 72 hours the slope's t is 0.0 and the top-third reversal is 7 bps (t 0.4, 5604 cases). By year its top third is positive in 6 of 8 years (52 to 84 bps, t 2.4 to 4.1) and flat in 2022 (-8 bps) and 2024 (0 bps).
