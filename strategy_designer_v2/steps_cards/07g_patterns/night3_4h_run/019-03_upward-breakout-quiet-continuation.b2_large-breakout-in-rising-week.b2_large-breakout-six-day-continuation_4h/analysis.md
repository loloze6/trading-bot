---
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation_4h
idea tested: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4479 USD
---
## Findings
- **F1:** A sharp one-day fall is followed by a rebound the next day. On the 1-day grid (6 bars, 3245 cases per quintile), the quintile with the lowest 1-day return, measured in the coin's usual move, has a next-day unusual move of +0.50 % (strength 0.099, t 5.1). The two highest quintiles are followed by slight falls (strength −0.043, t −2.7, and −0.047, t −2.5). The rebound's +0.50 % is 2.6 times the 0.19 % cost of a round trip, so it is graded across the whole range and large enough to pay.
- **F2:** Only the largest upward breaks continue; the tested idea's 7-day filter adds little. Over 3 days (18 bars), the top quartile of the break size above the 2-day high, in 30-day mean ranges, has an unusual move of +1.35 % (strength 0.144, t 3.26, 734 cases). The three lower quartiles range from −0.34 % to −0.04 %, with t between −1.0 and −0.1. Over 6 days the top quartile gives +1.25 % (t 2.08) and the others −0.62 % to +0.11 %. All upward breaks taken while the 7-day return is positive give only +0.53 % (t 1.68, 1641 cases).
- **F3:** The brief's core claim does not show. The absolute 6-day move, in the coin's usual moves, is flat across quintiles of range compression (12-bar mean range over 180-bar mean range): 0.73, 0.61, 0.71, 0.67 and 0.74. After upward breaks, the compression terciles give strengths of 0.081, −0.063 and 0.076, with no grading.
- **F4:** Upward breaks during a falling week lean down: −0.49 % over 3 days (t −1.93, 959 cases) and −0.59 % over 6 days (t −1.46). This cannot be told apart from chance given the number of angles looked at.
- **F5:** The time of the bar matters, but the move is too small to trade. The 4-hour bar after the 16:00 UTC bar rises by 0.054 of its usual move (t 6.8, 16354 bars), and the one after the 12:00 bar by 0.028 (t 3.2). After Friday bars the next bar rises by 0.055 (t 6.5). With a usual 4-hour move of about 2 %, that is about 0.1 % of price per bar, below the 0.19 % round trip (consistent with the earlier finding F2).
- **F6:** The book's Calmar failure comes from 2022, where it follows the market down: book Sharpe −1.47, mean −0.19 %/day against holding's −0.18 %/day. In 2018 the 7-day filter protected it: book +0.01 %/day against holding −0.35 %/day.
- **F7:** The book's gains rest on a few large trades. Of 2607 trades (median duration 6.3 days), the mean net return is +3.4 % but the median is −0.31 %, the win rate is 35 to 47 % and 9.1 % of trades lose more than 10 %.

## Ideas
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.g1_sharp-daily-fall-rebound` (from F1): The lower a coin's 1-day return, measured in its usual 1-day move, the more the coin rises over the next day.
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.g2_large-break-three-day-continuation` (from F2, F3): The farther a four-hour close sits above the highest high of the coin's preceding two days, measured in the coin's 30-day average four-hour range, the more the coin rises over the next three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
