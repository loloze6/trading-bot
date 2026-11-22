---
line: 7.d not profitable
backtest: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback_1d
idea tested: 025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3538 USD
---
## Findings
- **F1:** The book loses because its fees exceed its gross gain. The position's summed gain before costs is 0.628 and its summed fees are 1.514, 2.4 times as much, over a turnover of 1588 (0.095 % fee per unit traded). The 1883 short trades average -1.12 % before fees and -1.22 % after.
- **F2:** The gain sits only in the largest bounces, and the small ones carry the fees.
- **F3:** In coins with a negative 90-day return, the excess next-day fall is close to zero after ordinary rises.
- **F4:** The bounce fade belongs to falling markets. In coins with a positive 90-day return, rises above 1 usual move are followed by excess next-day falls of -0.09 % to -0.35 %, so those coins keep rising, against +0.5 % to +3.9 % in falling coins.
- **F5:** The book stays short after the effect is gone, which inflates fees and losses.
- **F6:** After a sharp bounce in a falling coin, a next day that falls is followed by a rise the day after. When that day's move is below -1 usual move the coin then rises 2.23 % (n 41); when it is between -1 and 0 usual moves it rises 1.41 % (n 122). The book is flat on those days.
- **F7:** How deep the 90-day fall is does not grade the giveback. After rises above 1 usual move, the four 90-day-return quartiles show excess next-day falls of +1.06 %, +0.79 %, +0.78 % and +1.15 %.

## Ideas
- `025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.d1_only-extreme-bounces-fade` (from F1, F2, F3, F5): In a coin whose 90-day return is negative and that has just had a one-day rise of several usual daily moves, the larger that rise in usual daily moves, the larger its fall over the next day, with the fall growing much faster than the rise, so that rises of about one usual daily move are followed by almost no fall and only rises of well beyond one usual move give back a large part of themselves.
- `025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.d2_giveback-then-rebound` (from F6, F5): In a coin whose 90-day return is negative, after a one-day rise of several usual daily moves followed by a falling day, the larger that falling day in usual daily moves, the larger the coin's rise over the following day.
- `025-02_deeper-fall-bigger-giveback.d2_next-day-bounce-giveback.d3_bounces-extend-in-uptrends` (from F4): In a coin whose 90-day return is positive and that has just had a one-day rise of several usual daily moves, the larger that rise in usual daily moves, the larger its further rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
