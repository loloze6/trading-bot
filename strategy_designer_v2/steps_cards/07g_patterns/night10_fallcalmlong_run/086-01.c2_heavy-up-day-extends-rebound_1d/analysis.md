---
line: 7.g patterns
backtest: 086-01.c2_heavy-up-day-extends-rebound_1d
idea tested: 086-01.c2_heavy-up-day-extends-rebound
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3574 USD
---
## Findings
- **F1:** Over the 70 in-profile 10-day grid cases (falling calm), the coin's unusual 10-day move is -2.67 % on average (t -1.50). In this profile a long position starts from a slight headwind, and that headwind cannot be told from chance.
- **F2:** Up days on heavy volume do not beat up days on light volume, against the brief. The split is at the median 20-day volume ratio. Over 5 days, light-volume up days gain +2.64 % unusual (24 cases) and heavy-volume up days lose -2.61 % (30 cases). Over 3 days the figures are +0.66 % (52 cases) and -1.33 % (58 cases). Over 1 day they are +0.12 % (163 cases) and -0.50 % (155 cases).
- **F3:** Volume ratio does not grade the later move at any horizon tested. Its Spearman correlation with the unusual move is -0.004 at 1 day (p 0.93, 660 cases), -0.078 at 3 days (p 0.26, 216 cases), +0.109 at 5 days (p 0.23, 121 cases) and +0.115 at 10 days (p 0.39, 57 cases). This matches the verdict's own Spearman of 0.030.
- **F4:** The strongest pattern found is the prior 5-day return predicting the next 3 to 5 days, and it does not stand out once the number of tests is counted. Its Spearman is +0.154 at 3 days (p 0.018, 237 cases) and +0.175 at 5 days (p 0.040, 137 cases), with a top-minus-bottom quintile t of 2.51 at 5 days. It reverses to -0.027 at 10 days (p 0.84) and is +0.022 at 1 day (p 0.56). This is about 36 feature-and-horizon tests, so a p of 0.02 to 0.04 is what chance alone would produce.
- **F5:** Other angles show nothing beyond chance:
- **F6:** The book's result rests on few trades and is uneven across coins and windows:

## Ideas
- No ideas: In falling calm markets the brief's heavy-volume effect is absent, and at 3 to 5 days it points the wrong way (F2, F3). The only graded pattern, prior 5-day momentum at 3 to 5 days (F4), flips at 10 days and does not survive the roughly 36 feature-and-horizon angles examined (F5). No pattern stands out enough to justify a new long idea in this box.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
