---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d1_heavy-volume-low-close-rebound
line: 7.d confirmed, not profitable
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d1_heavy-volume-low-close-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The heavier a coin's volume on a day relative to its own prior 20-day average and the nearer that day's close sits to the day's low, the more the coin rises over the next 10 days, and the more so the deeper the coin's 60-day fall before that day.
Consequence: A trader leans long for 10 days after heavy-volume low closes that come at the end of a deep 60-day decline, and stays out otherwise rather than holding the coin through its bear markets.
Why:
- F1: The book is close to holding the coins rather than trading the signal. It was in a position on 98 % of coin-days with a mean allocation of 0.85. It kept a mean allocation of 0.77 even on the 7616 bars with a forecast of 0.5 or less, where it lost −0.018 % a day. Its deepest fall was −64 %, against −80 % for holding. So Calmar fails (0.48) because the book carries the coins' own bear-market falls: w2 −37 %, w7 −29 %, w9 −29 %, w14 −47 %.
- F2: During the book's falls deeper than 30 % (1208 days), it held a mean allocation of 0.82 while the coins fell −0.16 % a day. 34 % of those days were in a falling 60-day trend, against 18 % on the other days. Its daily gain was −0.023 % on falling-60-day bars and +0.27 % on rising ones (4435 and 4449 bars).
- F3: The signal's edge sits inside falling markets. On the 10-day grid, cases with a forecast of 10 or more after a negative 60-day return gained +1.67 % excess (n 78). The same falling trend without the signal lost −1.21 % (n 251). So the falling condition alone loses and is not an effect of its own. In the lowest quarter of 60-day returns the gap widens: +4.06 % with the signal (n 48) against −1.47 % without (n 159).
- F5: The edge in falling markets is not stable, and a simple filtered book does not yet fix it. Strong-signal cases after a falling 60-day trend gained −0.75 % in w1–12 and +4.12 % in w13–24 (39 cases each). A book sized by the 10-day-held forecast only in falling 60-day trends had a Sharpe of −0.13. A book sized by the forecast at all times had a Calmar of 0.27 with a deepest fall of −46 %.
