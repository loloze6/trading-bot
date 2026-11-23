---
line: 7.b inconclusive
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue_1h
idea tested: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3649 USD
---
## Findings
- **F1:** The tested continuation is close to zero, not small but real. Step 5's main t is 0.80, with an unusual move of +0.04 % per case and a strength of 0.013, a quarter of the 0.05 that real ideas show. My recomputation of Saturday's move against the next 48 hours gives +0.06 % in Saturday's direction, t 0.43, n 2126, strength 0.015.
- **F2:** The continuation does not grow with Saturday's size, so the convex sizing has nothing to scale. By quintile of |Saturday's move in usual moves|, the 48-hour directional excess is -0.12 %, +0.50 %, +0.51 %, -0.52 % and -0.06 %, and the top quintile's t is -0.16. The supporting check passed by only 0.035 %.
- **F3:** Where Saturday's continuation appears, it is mixed rather than confined to one part of the data, so no narrowing would isolate it.
- **F4:** The effect the brief describes shows clearly one day later, on Sunday's 24-hour move, measured on the bar that opens Sunday 23:00.
- **F5:** At the 48-hour horizon, Sunday is the only day whose move is strongly reversed. The other days' moves are followed by between -0.19 % (Friday, t -1.55) and +0.35 % (Thursday, t 2.55). Over 24 hours, though, Tuesday's move is also reversed on Wednesday (-0.45 %, t -3.86), so a one-day reversal is not weekend-only.
- **F6:** Saturday's own move is partly reversed on Sunday (24 hours: -0.23 %, t -2.56), but this is undone by 48 hours (+0.06 %). This explains why a 48-hour bet on Saturday's move captures a total move of only +0.08 % per case, 0.4 times the 0.19 % cost of a trade. Sunday's 48-hour reversal of 0.73 % is about 3.8 times that cost.
- **F7:** The grading of Sunday's reversal is not yet shown. Sunday's top quintile of |move in usual moves| is reversed by 0.60 % over 48 hours (t -1.54, n 426), no more than the 0.73 % of all Sundays. Whether the reversal is proportional to Sunday's size is what the new idea has to establish.

## Ideas
- `026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week` (from F4, F5, F6, F7): A coin's 24-hour return over Sunday, measured against the coin's usual 30-day move, is followed over the next two days (Monday and Tuesday) by a move in the opposite direction. The larger Sunday's move in usual moves, the larger the reversal.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
