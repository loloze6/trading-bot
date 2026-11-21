---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge
line: 7.d not profitable
backtest: 018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, falls by several times its 30-day average absolute daily return, the coin rises over the next 10 days more than its normal drift, only while its price is above its 60-day average price, and the further above that average and the larger its 30-day return before the drop, the larger the rise.
Consequence: A trader buys sharp drops only in coins trading above their 60-day average, and so stands aside through the long shared declines that carry the book's deepest falls.
Why:
- F1: The Calmar fails because of falls the six coins share. The book's deepest fall is 57.3 %, from w12 to a trough in w14: 351 days down and 326 days to recover, while the coins' average fell 75 % over the same days. The second is 43.7 % (w6 to w9) against a 57 % fall of the coins. With a yearly return of 38.9 %, this gives the 0.68 Calmar.
- F2: The book is a near-permanent long position, not a rebound bet. It is long on 71 % of bars at a mean allocation of 0.93, because every 240-hour hold is followed by another drop signal. In the losing windows w7, w9, w13 and w14 it was still long on 58 % of bars and lost 0.90 bps per bar, while the coin lost 1.07.
- F3: The book's gain sits where the coin trades above its 60-day average price. On those bars it is long on 96 % of bars and earns 1.02 bps per bar (t 4.2, 154 438 bars). Below that average it is long on 53 % of bars and earns 0.22 bps (t 1.5, 158 671 bars). In the quintile furthest above the average it earns 1.52 bps per bar.
- F4: Leaving out the positions entered below the 60-day average cuts the gross deepest fall from 56.3 % to 38.8 %. Gross Calmar rises from 0.74 to 0.78 and gross yearly return falls from 41 % to 30 %. Time long falls from 71 % to 57 %.
- F7: Trades entered while the coin's 60-day return is between -10 % and +2 % lose 4.3 % net on average, with 22 % winners (78 trades). Trades entered after a 60-day rise above 13 % earn 13.7 % (80 trades).
