---
line: 7.e profitable but not proven
backtest: 040-01_rising-swing-scaled-weeks-rise-continues_1d
idea tested: 040-01_rising-swing-scaled-weeks-rise-continues
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.5248 USD
---
## Findings
- **F1:** The book's gain is about half the market's own rise. Over folds B and C its summed position gain is 15.97, of which 8.70 is the coin's normal drift times the position held and 7.28 is timing (t 2.39 over 7,664 coin-days in a position). Its daily Sharpe of 1.22 beats holding's 0.77 mostly because it holds a mean position of 0.42 and stays out of falling windows (w14 holding -0.52, book -0.20).
- **F2:** The timing gain comes from a few windows. w11 alone gives +5.58, w17 +2.73 and w10 +2.07, which is more than the whole 7.28. w12 (-1.84), w14 (-1.27) and w18 (-1.16) give part of it back.
- **F3:** What the book earns from inside the rising profile is the sign of the 20-day move, not its size. Coin-days held with a positive forecast have a mean daily excess return of +0.25 % (t 2.23, n 4,034), against -0.23 % on in-profile days with no position (n 1,735). On the 14-day grid, cases with a positive swing-scaled rise make +1.19 % excess, and those with a zero or negative one make -3.90 %.
- **F4:** The grading the idea claims runs the wrong way. On the in-profile grid, among positive swing-scaled rises, the slope of the forward excess return on the rise is negative at every horizon:
- **F5:** Over 14 days in the rising profile, the outcome by quintile of the swing-scaled rise is an inverted U:
- **F6:** The book earns more per held day in calm markets than in agitated ones: a mean gain of 0.249 % a day on 4,493 calm coin-days (timing 5.36), against 0.151 % on 3,171 agitated ones (timing 1.91).

## Ideas
- `040-01.e1_swing-scaled-rise-exhausts-uptrend` (from F4, F5): In a rising market, the more of its 20-day daily swings a coin's 20-day rise spans, the more the coin falls back below its usual drift over the next 14 days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `040-01.e2_uptrend-pullback-keeps-falling` (from F3, F5): In a rising market, the more of its 20-day daily swings a coin's 20-day fall spans, the more the coin keeps falling over the next 14 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
