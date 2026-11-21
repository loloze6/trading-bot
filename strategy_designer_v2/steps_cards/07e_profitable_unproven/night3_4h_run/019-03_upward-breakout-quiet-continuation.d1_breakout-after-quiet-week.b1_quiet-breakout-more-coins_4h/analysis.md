---
line: 7.e profitable but not proven
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins_4h
idea tested: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4615 USD
---
## Findings
- **F1:** Most of the book's gain comes from the market's own rise. Of its mean daily return of 9.95 bps, 7.02 bps come from the position held times the coin's mean daily return, and only 2.93 bps from timing. The mean position is 0.48 and the coins' mean daily return is 13.68 bps.
- **F2:** The gain rests on a few trades. The top 5 % of the 10,657 trades sum to +20,826 % net, more than the whole book's +18,953 %. The other 95 % sum to −1,873 %, with a median trade of −0.13 % and a win share of 0.47.
- **F3:** The book earns in the coin's own up-trends and loses in its down-trends. On days in the top fifth of the coin's 30-day return (median +42 %), the book makes 92.6 bps a day, 2.03 times its total gain. In the bottom fifth (median −28 %) it loses 37.9 bps a day, −0.83 times its total gain.
- **F4:** At the plan's horizon, and at any horizon, breakouts carry almost no unusual move. Over 1 day it is +0.07 % (t 0.64), over 3 days +0.19 % (t 1.39), over 6 days +0.27 % (t 1.25) and over 12 days +0.11 % (t 0.34), on 5,000 to 5,500 cases spaced at least 3 days apart.
- **F5:** How a breakout continues depends on the coin's 7-day return before it, and the effect grows over 12 days.
- **F6:** The coin's 30-day return before a breakout separates the same way over 12 days.
- **F7:** Timing gains come in up-market years and timing losses in down-market years. Timing was +32.8 bps a day in 2020 (coins +46.5) and +11.9 in 2021. It was −15.5 in 2022 (coins −26.4), −6.3 in 2018 and −11.2 in 2025.
- **F8:** Much of the move happens before a trader can act. The signal's own breakout bar has already risen 3.15 % on average by its close.

## Ideas
- `019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e1_breakout-continues-rising-week` (from F3, F4, F5, F7): When a coin's four-hour bar closes above the high of its preceding two days, the coin rises more than usual over the next 12 days, and the larger its 7-day return before that bar, the larger the rise.
- `019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e2_breakout-fails-in-downtrend` (from F3, F6, F2): When a coin's four-hour bar closes above the high of its preceding two days while its 30-day return is negative, the coin falls more than usual over the next 12 days, and the deeper that 30-day fall, the larger the decline.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
