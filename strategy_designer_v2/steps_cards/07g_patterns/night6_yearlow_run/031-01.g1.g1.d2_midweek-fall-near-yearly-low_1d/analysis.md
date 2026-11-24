---
line: 7.g patterns
backtest: 031-01.g1.g1.d2_midweek-fall-near-yearly-low_1d
idea tested: 031-01.g1.g1.d2_midweek-fall-near-yearly-low
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4499 USD
---
## Findings
- **F1:** The Wednesday (UTC) move reverses the move from Saturday's close to Tuesday's close, and the reversal is graded. On Tuesday bars, the Spearman correlation between the 3-day vol-scaled return and Wednesday's excess return is -0.137 (p 6e-10, 2033 cases). This is the strongest of the 7 weekday tests, which otherwise range from -0.08 to +0.03. With the cases of one day taken together, -z3 × Wednesday excess has a t of 2.11 over 346 days.
- **F2:** In F1's reversal, Wednesday's excess return falls steadily across the bins of the Tuesday 3-day z:
- **F3:** The tested idea's grading holds in the bars. Saturday's excess return in the forecast's direction rises with |forecast|, from -0.20 % (t -0.88) in the lowest quintile to +1.01 % (t 4.79) and +0.87 % (t 3.69) in the top two. All 6 coins are positive (+0.36 % to +0.53 %).
- **F4:** Part of the book's Saturday gain is plain Saturday drift. The Friday-close-to-Saturday excess return is +0.30 % unconditionally (t 2.07 by day, 414 days). In the upper half of the yearly range, Saturdays after a midweek fall, where the book is flat, also rise (+0.33 %, t 1.89).
- **F5:** The short side's Saturday falls are weak:
- **F6:** A one-day fall is followed by a next-day rise, but the effect is only clear when volatility is high:

## Ideas
- `031-01.g1.g1.d2.g1_wednesday-reverses-weekend-move` (from F1, F2): The larger a coin's return from Saturday's close to Tuesday's close (UTC), measured in its usual daily moves, the more the coin moves the other way over Wednesday. A weekend-to-Tuesday rise is followed by a Wednesday fall, and a fall by a Wednesday rise, each larger the larger the 3-day move.
- `031-01.g1.g1.d2.g2_high-volatility-down-day-bounce` (from F6): While a coin's last 20 days have been volatile relative to its own history, the larger its one-day fall in usual daily moves, the more it rises over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
