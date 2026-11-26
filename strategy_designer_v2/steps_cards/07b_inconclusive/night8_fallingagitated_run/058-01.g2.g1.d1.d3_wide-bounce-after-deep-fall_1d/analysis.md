---
line: 7.b inconclusive
backtest: 058-01.g2.g1.d1.d3_wide-bounce-after-deep-fall_1d
idea tested: 058-01.g2.g1.d1.d3_wide-bounce-after-deep-fall
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2126 USD
---
## Findings
- **F1:** Step 5's main measure is on the side the idea predicts but short of the bar: +0.51 % mean short excess return over the next day, t 1.63, on 792 cases that fall on only 406 days. The size reading agrees, at +0.77 % unusual move, t 2.36, over 333 days, a strength of 0.163. On folds B and C alone, the 371 cases give +0.94 % with t 1.73 over 173 days, so the test lacks independent days rather than direction.
- **F2:** The cases bunch on the same days (371 cases on 173 days in folds B and C), because the six coins enter falling agitated bounces together. The day clustering, not the case count, holds the t below 2.
- **F3:** The effect is graded as the idea says, and the extreme carries it.
- **F4:** The give-back is a one-day move that is gone by the second day. The mean short excess is +0.94 % (t 1.73) at 1 day, +0.35 % (t 0.46) at 2 days, +0.09 % (t 0.11) at 3 days and −0.47 % (t −0.50) at 5 days. The plan's 1-day horizon is the right one, and a longer horizon would not sharpen the answer.
- **F5:** The sign holds broadly but weakly in each slice, so no single part of the data carries it.
- **F6:** The book shows the move is larger than a trade's cost, but the book still fails. The total move per case is +0.64 %, 3.3 times the 0.19 % cost of a trade, and the book's Sharpe is 0.53. It fails only on Sharpe against holding (−0.04) and Calmar (0.31), with positions on 8 % of the coins' days. More cases on more coins, not a different sizing, is what can make the result clear.

## Ideas
- `058-01.g2.g1.d1.d3.b1_wide-bounce-all-coins` (from F1, F2, F5, F3): In a falling, agitated market, a coin's up day that comes after a 3-day fall is followed by a fall over the next day, and the larger that day's high-to-low range plus the depth of its 3-day fall, both against the standard deviation of its daily returns over the past 30 days, the larger the next-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
