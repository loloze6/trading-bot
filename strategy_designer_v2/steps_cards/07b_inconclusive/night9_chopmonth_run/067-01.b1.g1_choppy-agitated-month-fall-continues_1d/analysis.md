---
line: 7.b inconclusive
backtest: 067-01.b1.g1_choppy-agitated-month-fall-continues_1d
idea tested: 067-01.b1.g1_choppy-agitated-month-fall-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3641 USD
---
## Findings
- **F1:** Inside the tested choppy agitated profile, on folds B and C, the slope of the 7-day excess return on the 30-day fall is zero (slope 0.0000, t 0.00, 58 grid cases), and the mean short unusual move is +1.71 % with t 0.45 over the cases' days, so the full-data slope (t 1.09) has no support in these windows.
- **F2:** In choppy markets that are not agitated (choppy calm), deeper 30-day falls are followed by weaker excess returns. The slope is 0.0045 at 7 days (t 2.31, 36 cases) and 0.0114 at 10 days (t 3.50, 29 cases), and the mean short unusual move is +2.8 % and +4.4 % (day-clustered t 1.13 and 0.97).
- **F3:** Over all choppy coin-days, calm and agitated together (the trend condition only, the brief's own profile), the continuation is clearest. The slope is 0.0047 at 7 days (t 3.34, 54 cases) and 0.0095 at 10 days (t 5.19, 39 cases), with a mean short unusual move of +5.7 % and +7.7 % (day-clustered t 1.68 and 1.67).
- **F4:** Restricting to the agitated half removes the effect rather than sharpening it, so the narrowing to choppy agitated measured the idea where it is weakest.
- **F5:** The choppy slopes rise with the horizon up to 10 days. Beyond that the case counts drop (23 at 14 days, 12 at 21 days) and the mean short move turns negative (-1.6 % and -12.3 %), so 10 days is the horizon where the graded continuation shows most clearly.
- **F6:** The slope t-statistics in F2 and F3 are not clustered by day, while the day-clustered t of the mean short move stays below 2. Cases from several coins on the same days carry part of the evidence, so the effect is suggestive and needs the held-out folds to settle.

## Ideas
- `067-01.b1.g1.b1_choppy-month-fall-continues` (from F3, F4, F5, F6): In a choppy market, the larger a coin's fall over the past 30 days, the more it keeps falling over the next 10 days.
- `067-01.b1.g1.b2_choppy-calm-fall-continues` (from F2, F4, F5, F6): In a choppy, calm market, the larger a coin's fall over the past 30 days, the more it keeps falling over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
