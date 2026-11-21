---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation
line: 7.d not profitable
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes above the highest high of a coin's preceding two days, only while the coin's 7-day return is positive and its 60-day return is positive, the coin rises over the next six days. The farther that close sits above the two-day high, measured in the coin's 30-day average four-hour range, the larger the rise.
Consequence: A trader would refuse upward breaks made while the coin is still below its level of two months ago, which is where the cases concentrate in the bear stretches that carry the book's deepest fall.
Why:
- F1: The Calmar fails because of one long bear stretch: the book's deepest fall is −61 % (yearly return +30 %), lasting 271 days across w1, w2 and w3 (all 2022), where the book's daily returns summed to −85 % against −74 % for holding the coins, with a correlation of 0.77 to holding.
- F3: The idea's cases split by window. In the five losing windows (w1, w2, w3, w5, w9) the mean unusual 6-day move is −2.27 % (t −4.27, 304 cases). In the other windows it is +1.17 % (t 3.24, 1337 cases).
- F4: Being long a 7-day rise does not keep the book out of bear stretches. The book is long on 58 % of bars in the losing windows against 63 % elsewhere. There, the long bars' gain per bar is negative at almost every level of the 30-day return, 7-day return and distance from the 30-day high, for example −0.00084 per bar within 5 % of the 30-day high.
- F5: The coin's 60-day return is positive in only 42 % of the cases in the losing windows, against 62 % elsewhere. Among the cases, a 60-day return between −10 % and 0 is followed by −2.2 % (t −2.70, 92 cases), and 0 to +20 % by +1.6 % (t 1.93, 182 cases).
- F7: The break's size grades the trades steeply: from the smallest to the largest fifth of breaks (median 0.10 to 1.54 average 4-hour ranges), the mean net trade result is +1.6, +1.2, +1.8, +4.4 and +8.1 %. Yet the worst tenth of trades loses about 8 to 10 % in every fifth.
