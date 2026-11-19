---
brief: 016_grind-versus-jump-moves
source-idea: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift
line: 7.g patterns
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Each day, the coin rises over the two hours from 21:00 to 23:00 UTC more than in its other hours, and the rise is larger the higher its realised hourly volatility over the past 7 days.
Consequence: A long held through 21:00–23:00 UTC rather than 20:00–22:00 catches the hours that actually carry the late-evening drift, worth taking only when the coin's volatility makes the move large next to costs.
Why:
- F1: The coin's rise is concentrated in the 21:00–23:00 UTC block, not the tested 20:00–22:00 block: the hourly bar starting 21:00 averages +5.45 bp (t 6.75, n 17,403) and the one starting 22:00 +4.36 bp (t 5.66), the two strongest of the 24 hours, while the 20:00 bar the book held averages only +0.45 bp (t 0.55).
- F2: The two-hour return from the 21:00 close to the 23:00 close is positive for every coin, from +8.4 bp to +10.8 bp with t between 3.1 and 4.7, and in 7 of 8 years (2022: −4.3 bp, t −1.43), against a 24-hour mean of about +12 bp for the whole day.
- F3: The 21:00–23:00 rise grows with the coin's 7-day realised hourly volatility: +4.7 bp (t 3.39) in its lowest volatility quintile and +24.5 bp (t 6.42, n 3,282) in its highest, with the middle quintiles at 4.4 to 9.0 bp.
- F4: The book lost because it held the wrong hours and paid more than they earn: its held bar starting 20:00 moved +0.31 bp, its held bar starting 21:00 moved +5.47 bp, trades averaged −0.064 % before fees against 0.47 % commission each, and the result was a Sharpe of −2.87.
