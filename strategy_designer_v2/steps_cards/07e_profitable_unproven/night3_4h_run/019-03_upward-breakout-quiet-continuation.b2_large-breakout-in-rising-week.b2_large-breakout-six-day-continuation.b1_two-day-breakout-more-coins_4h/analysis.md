---
line: 7.e profitable but not proven
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.b1_two-day-breakout-more-coins_4h
idea tested: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.b1_two-day-breakout-more-coins
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4624 USD
---
## Findings
- **F1:** The idea's grading is there, but the test could not see it. The forecast sits at its cap of 20 on at least 75 % of entries (median 20, mean 18.77), so the median split left 0 cases in the larger half. Graded by the raw break instead (close minus the two-day high, in 30-day average 4h ranges), the 6-day unusual move rises from -0.53 % in the smallest quintile (break 0.07 ranges) to +2.88 % in the largest (break 1.52 ranges). Strength goes from -0.043 to +0.187, about 680 cases per quintile.
- **F2:** The largest-break quintile's unusual move of +2.88 % per case is about 13 times the 0.22 % round-trip cost. The two smallest quintiles are at or below zero (-0.53 %, -0.03 %), so most of the book's bets carry no move of their own.
- **F3:** Most of what the book earns is the market's own rise. On days averaged over the coins it makes 0.125 % against 0.139 % for holding, with a correlation of 0.78. It loses 1.43 % on the 1,350 days the coins fall and gains 1.48 % on the 1,548 days they rise. Across coins, the market rise accounts for about 1.4 of the roughly 2.0 bps gained per bar.
- **F4:** The 7-day return grades the move too. Among breaks, the top quintile of 7-day return (median +21 %) is followed by +3.66 % unusual move over 6 days (strength 0.22). The lower four quintiles range from -0.64 % to +1.00 %.
- **F5:** Break size and 7-day return add up. The largest-break third combined with the strongest-week third gives +3.50 % over 6 days (505 cases). The smallest-break third gives -0.07 % to -0.48 % at any 7-day return.
- **F6:** The coin's 30-day return grades the outcome. Breaks after a 30-day fall (median -22 %) are followed by -0.92 % over 6 days (t -1.74, 528 cases). Breaks after a 30-day rise of +21 % to +51 % are followed by +1.86 % to +2.14 % (t 2.0 to 2.3).
- **F7:** The brief's quiet stretch points the wrong way. Breaks out of the narrowest prior two-day range (1.5 average ranges) are followed by -0.09 % over 6 days. Breaks out of the widest (5.0 ranges) are followed by +2.25 % (t 2.79, 674 cases); the move belongs to breaks after an already wide, active stretch.
- **F8:** The gain depends on bull periods. The 6-day unusual move per case is +2.66 % in 2020 and +4.38 % in 2021, but -2.72 % in 2022 and -0.96 % in 2025. Only 44.7 % of the 5,265 trades win, and the top 5 % of trades carry the whole net sum.
- **F9:** The grading holds coin by coin. In 15 of 19 coins, the largest-break third beats the smallest over 6 days (per-coin rank correlations up to 0.27).
- **F10:** The horizon fits. The bets' unusual move has t 1.33 at 1 day, 2.40 at 2 days, 2.85 at 6 days and 1.67 at 12 days.

## Ideas
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.b1_two-day-breakout-more-coins.e1_large-break-in-strong-week` (from F1, F2, F4, F5, F9, F10): When a coin's four-hour close breaks above the highest high of its preceding two days, the farther the close sits above that high (in the coin's 30-day average four-hour range) and the stronger the coin's 7-day return, the larger the coin's rise over the next six days.
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.b1_two-day-breakout-more-coins.e2_breakout-within-monthly-uptrend` (from F3, F6, F8): When a coin's four-hour close breaks above the highest high of its preceding two days, the higher the coin's 30-day return, the larger its rise over the next six days.
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.b1_two-day-breakout-more-coins.e3_wide-range-breakout-continuation` (from F7, F1): When a coin's four-hour close breaks above the highest high of its preceding two days, the wider that two-day range was (in the coin's 30-day average four-hour range), the larger the coin's rise over the next six days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
