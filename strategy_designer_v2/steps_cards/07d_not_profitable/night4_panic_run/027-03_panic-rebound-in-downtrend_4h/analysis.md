---
line: 7.d not profitable
backtest: 027-03_panic-rebound-in-downtrend_4h
idea tested: 027-03_panic-rebound-in-downtrend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3386 USD
---
## Findings
- **F1:** The book was in a position on only 3.5 % of its coin-days and made 79 trades in total, about 0.0042 trades a day against the 0.01 required. On the 96.5 % of days it was flat, the coins rose +0.132 % a day on average and the book earned nothing (−2.4e-07 a day). This is why its mean daily return (6.3e-05) and its Sharpe against holding (−0.402) fail.
- **F2:** The 3x range rule makes the signal rare. On the 84-bar grid of all windows, only 7 of 720 cells had a 6-bar mean range at least 3 times its 180-bar mean. Another 55 cells had a ratio between 1.5 and 2, and their 84-bar unusual move was +3.85 % (t 1.45), against −0.72 % (t −0.82, 433 cells) for ratios at or below 1.
- **F3:** The negative 30-day prior return adds nothing. Among 24-hour falls with a range ratio of 1.5 to 2, cells with a non-negative prior return had an unusual 84-bar move of +6.41 % (19 cells, t 1.41) and cells with a negative prior return +9.27 % (7 cells, t 1.47). Requiring the prior fall removes most of the cases without making the effect larger.
- **F4:** The depth of the 24-hour fall carries the effect even without the range rule. Cells whose 6-bar return was at least 3 times the coin's mean absolute 6-bar move downward had an unusual 84-bar move of +8.83 % (16 cases, t 2.42; total +10.74 %). Mild falls (fall z between −1 and 0) had −2.11 % (236 cases, t −1.58).
- **F5:** Within cells whose range ratio was at least 1.5, the sign of the 24-hour move matters. Falls with fall z at or below −3 gave +7.92 % (15 cases, t 2.10) and falls with fall z between −2 and −1 gave +11.02 % (11 cases). Rises with fall z between 1 and 2 gave −3.86 % (13 cases) and rises above 2 gave −1.86 % (13 cases). So range expansion pays only together with a fall.
- **F6:** On the days it was in a position, the book's trades did earn their premium. The book made +0.173 % a day while the coins fell −0.225 % a day. Trades averaged +0.59 % net with a median of −0.05 % and a 49 % win share, held about 8.9 days. The cost of one trade (0.19 %) is small against the +4.26 % total move per case, so the failure comes from too few cases, not from cost.
- **F7:** The gain is uneven across coins. BTC's 15 trades lost −7.23 % on average and XMR's 16 trades lost −1.89 %, while XRP (+5.75 %, 13 trades), ZEC (+5.66 %, 10 trades) and ETH (+3.53 %, 16 trades) carried the book.

## Ideas
- `027-03_panic-rebound-in-downtrend.d1_graded-sell-off-liquidity-premium` (from F1, F2, F3, F4, F5, F6): After a 24-hour fall that is large against the coin's usual 24-hour move, while its bar range over those 24 hours is above its 30-day average, the coin earns more than its usual drift over the next 14 days. The larger the fall times the range expansion, the larger that excess, whatever the coin's 30-day return before.
- `027-03_panic-rebound-in-downtrend.d2_deep-one-day-fall-rebound` (from F4, F6): The deeper a coin's 24-hour fall against its usual 24-hour move, the higher its return above its normal drift over the next 14 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
