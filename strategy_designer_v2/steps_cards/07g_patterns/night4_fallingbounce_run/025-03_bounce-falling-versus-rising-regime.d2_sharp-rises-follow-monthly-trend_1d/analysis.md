---
line: 7.g patterns
backtest: 025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend_1d
idea tested: 025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3891 USD
---
## Findings
- **F1:** The 30-day trend effect holds only in coins whose 60-day return is positive. Regressing the 5-day excess return on the 30-day move in usual daily moves gives a slope t of 3.10 on 843 grid cases when the 60-day return is up, and t -0.13 on 848 cases when it is down. By 60-day tercile the slope t is -0.31 in the lowest third, 3.65 in the middle and 2.56 in the top, about 564 cases each.
- **F2:** The 30-day trend effect does not need a sharp up day. On ordinary days (1-day move between -1 and +1 usual moves) the slope of the 5-day excess return on the 30-day move has t 2.44 on 1858 cases, against t 1.37 on the 92 sharp-rise cases. Over all grid bars it has t 3.03 on 2555 cases. Ordinary days after a falling month have a 5-day excess return of -0.84 % (t -2.45, 928 cases).
- **F3:** The book's gain comes from its long side. Long bars earn +0.35 % per bar (t 4.45, 2440 bars) against +0.08 % for short bars (t 1.79, 1276 bars). Short trades lose 2.43 % on average after fees with 33 % winners, while long trades gain 3.85 % with 59 % winners.
- **F4:** Longs depend on the longer trend. Long bars earn +0.56 % per bar when the coin's 60-day return is up (t 3.52, 950 bars) and -0.15 % when it is down (t -1.45, 349 bars).
- **F5:** Saturday is the strongest weekday for the coins. Averaged across coins, with one value per day, the Saturday return is +0.45 % (t 3.04, 414 days). Five of six coins have a Saturday t above 2 (BTC: 1.40). Years 2022 and 2023 show none of it (t 0.42 and -0.01). The book also earns most on Saturdays: +0.15 % a day, t 3.72.
- **F6:** The book's largest days are days the coin itself moved a lot. On its top 1 % days the coin rose 8.8 % and was up 91 % of the time. On its bottom 1 % days the coin fell 5.4 %. Both groups follow a coin rise of about 3.5–3.8 % the day before, so the book's extremes are entries chasing a rise that then either runs on or reverses.
- **F7:** The brief's own claim, that sharp rises fade in falling months, is not visible. After a rise of at least 2 usual moves following a falling 30 days, the 5-day excess return is -1.43 % with t -0.83 on only 30 cases. After a rising month the same rises are followed by +4.74 % (t 2.37, 62 cases).

## Ideas
- `025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend.g1_monthly-momentum-in-rising-coins` (from F1, F2, F4, F3): In a coin whose 60-day return is positive, the 5-day return is higher the higher its 30-day return measured in usual daily moves, on any day and not only after a sharp rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
