---
line: 7.g patterns
backtest: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall_1d
idea tested: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4946 USD
---
## Findings
- **F1:** After a one-day rise of at least 2 usual daily moves, what follows depends on the coin's 30-day return measured in usual moves, and the dependence runs one way. The Spearman correlation with the next return is +0.104 over 3 days (p 0.0016, 924 rises) and +0.106 over 7 days (p 0.0013, 908 rises). Over 1 day it is only +0.021 (p 0.52), so the grading shows over days, not the next day.
- **F2:** The continuation shows in the upper part of the 30-day range. Sorted by raw 30-day return, rises in the 3rd to 5th quintiles were followed by drift-adjusted 3-day returns of +2.23 % (t 2.69, 185), +2.25 % (t 2.25, 184) and +3.90 % (t 2.01, 187). By the scaled 30-day return, they are positive in both halves of the windows: early quartiles 2–3 +4.26 % (t 1.75) and +3.20 % (t 1.98), late quartiles 1–2 +2.17 % (t 2.36) and +2.55 % (t 1.92).
- **F3:** The tested idea's own side shows again on the bars. Rises in the deepest 30-day-fall quintile (mean 30-day return −19 %) were followed by −1.33 % the next day (t −3.09, 187) and −1.86 % over 3 days (t −2.57, 185). The next-day loss holds in both halves: −1.07 % (t −2.39, 87) early and −1.14 % (t −2.23, 144) late.
- **F4:** Plain 30-day momentum, with no jump required, carries forward. On a non-overlapping 7-day grid, the top quintile of each coin's scaled 30-day return was followed by +1.70 % (t 1.89, 340) early and +2.48 % (t 2.91, 391) late. On the 3-day grid the top quintile gave +1.00 % (t 2.14, 871) and +0.98 % (t 2.81, 931).
- **F5:** The book cannot show much of this.
- **F6:** Sharp one-day falls in the deepest 30-day falls do not reverse reliably. By raw 30-day return, the deepest quintile (mean −37 %) gained +1.95 % the next day (t 2.94, 154). By the scaled 30-day return, the deepest quartile gained only +0.44 % (t 0.51) early and +0.15 % (t 0.16) late over 3 days. I count this as no finding.
- **F7:** Some calendar and volatility patterns appeared, but I looked at many angles, so I take none of them forward.

## Ideas
- `025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall.g1_sharp-rises-extend-uptrends` (from F1, F2): In a coin that has just had a one-day rise of several usual daily moves while its 30-day return is positive, the higher that 30-day return measured in usual moves, the larger its further rise over the next 3 days.
- `025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall.g2_monthly-strength-carries-forward` (from F4, F2): In any coin, the higher its 30-day return measured in its usual moves, the larger its rise over the next 7 days.
- `025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall.g3_bounce-giveback-over-days` (from F3, F1, F5): In a coin whose 90-day return is negative and that has just had a one-day rise of several usual daily moves, the deeper its 30-day fall, the larger its fall over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
