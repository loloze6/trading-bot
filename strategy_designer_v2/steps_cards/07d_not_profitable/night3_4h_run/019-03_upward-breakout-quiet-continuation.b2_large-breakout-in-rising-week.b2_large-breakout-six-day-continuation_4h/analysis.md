---
line: 7.d not profitable
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation_4h
idea tested: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5799 USD
---
## Findings
- **F1:** The Calmar fails because of one long bear stretch: the book's deepest fall is −61 % (yearly return +30 %), lasting 271 days across w1, w2 and w3 (all 2022), where the book's daily returns summed to −85 % against −74 % for holding the coins, with a correlation of 0.77 to holding.
- **F2:** Every coin lost in that fall, and the book lost more than holding on four of six: BTC −22 % against −15 % for holding, ETH −21 % against −14 %, XMR −6 % against −2 %, LTC −14 % against −14 %, with XRP (−9 % against −12 %) and ZEC (−14 % against −15 %) the exceptions.
- **F3:** The idea's cases split by window. In the five losing windows (w1, w2, w3, w5, w9) the mean unusual 6-day move is −2.27 % (t −4.27, 304 cases). In the other windows it is +1.17 % (t 3.24, 1337 cases).
- **F4:** Being long a 7-day rise does not keep the book out of bear stretches. The book is long on 58 % of bars in the losing windows against 63 % elsewhere. There, the long bars' gain per bar is negative at almost every level of the 30-day return, 7-day return and distance from the 30-day high, for example −0.00084 per bar within 5 % of the 30-day high.
- **F5:** The coin's 60-day return is positive in only 42 % of the cases in the losing windows, against 62 % elsewhere. Among the cases, a 60-day return between −10 % and 0 is followed by −2.2 % (t −2.70, 92 cases), and 0 to +20 % by +1.6 % (t 1.93, 182 cases).
- **F6:** The coin's 15-day return grades the cases. Cases with a 15-day return above 15 % gain +1.8 % unusual (t 2.10, 410 cases), while cases with 0 to 5 % lose −1.3 % (t −2.22, 239 cases).
- **F7:** The break's size grades the trades steeply: from the smallest to the largest fifth of breaks (median 0.10 to 1.54 average 4-hour ranges), the mean net trade result is +1.6, +1.2, +1.8, +4.4 and +8.1 %. Yet the worst tenth of trades loses about 8 to 10 % in every fifth.
- **F8:** Contrary to the brief, breaks out of expanded ranges pay more than breaks out of quiet ones. When the 7-day mean range is above 1.2 times the 30-day one, trades average +6.7 % against +1.4 to +3.4 % below it, and long bars earn +0.00114 per bar in the paying windows against 0.00012 to 0.00061.
- **F9:** The trades are a few large wins over many small losses: 2607 trades held about 8 days, with a median of −0.31 %, a mean of +3.4 % and 43 % winners. The worst 5 % lose 14 % or more and the single worst lose 46 to 56 % on ETH, LTC, XRP and ZEC.
- **F10:** The size is not what fails. The total move per case (+1.30 %) is 6.8 times a 0.19 % round trip and the unusual move 2.6 times. The failure is the depth of the falls, not the gain per trade.

## Ideas
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.d1_breakout-above-rising-two-months` (from F1, F3, F4, F5, F7): When a four-hour bar closes above the highest high of a coin's preceding two days, only while the coin's 7-day return is positive and its 60-day return is positive, the coin rises over the next six days. The farther that close sits above the two-day high, measured in the coin's 30-day average four-hour range, the larger the rise.
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.d2_breakout-graded-by-fortnight-trend` (from F6, F7, F9): When a four-hour bar closes above the highest high of a coin's preceding two days, only while the coin's 7-day return is positive, the coin rises over the next six days. The larger the coin's 15-day return, and the farther that close sits above the two-day high in the coin's 30-day average four-hour range, the larger the rise.
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.d3_breakout-from-expanding-ranges` (from F8, F7): When a four-hour bar closes above the highest high of a coin's preceding two days while the coin's 7-day average four-hour range is wide against its 30-day average range, the coin rises over the next six days. The wider that recent range against the 30-day one, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
