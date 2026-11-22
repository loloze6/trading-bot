---
line: 7.b inconclusive
backtest: 027-02_panic-fall-depth-rebound_4h
idea tested: 027-02_panic-fall-depth-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3695 USD
---
## Findings
- **F1:** The tested grading is absent at every horizon. The slope of excess return on the 24-hour fall depth is 0.0059 with t 0.49 at 84 bars (14 days, 142 cases), -0.0065 with t -0.41 at 18 bars (3 days, 151 cases), 0.0011 with t 0.08 at 42 bars (7 days, 149 cases) and -0.0019 with t -0.14 at 126 bars (21 days, 137 cases); the rank correlations are 0.01 to 0.03.
- **F2:** The quartiles of fall depth do not rise with depth. Falls of 2.0 %, 5.1 %, 10.7 % and 20.5 % are followed by 14-day excess returns of 0.24, 0.29, -0.17 and 0.24 usual moves. At 3 days, the terciles of 2.7 %, 8.5 % and 18.3 % falls give 0.41, 0.28 and 0.41, so a deeper fall does not bring a larger rebound.
- **F3:** The panic premium is real as a level, and it is concentrated in the first few days. On each horizon's own grid, the cases' mean excess return is 0.55 usual moves (t 4.92, 205 cases) over 1 day and 0.51 (t 4.53, 184 cases, unusual move +4.56 %) over 3 days. It decays to 0.25 (t 2.42, 165 cases) over 7 days and to 0.15 (t 1.60, 142 cases) over the plan's 14 days, so the 14-day test measured the effect after most of it had faded.
- **F4:** Over 3 days the premium is positive in every coin, from 0.25 (LTC, t 1.58) to 0.82 (ZEC, t 2.10), and in every year except 2018 (-0.28, t -1.11, 21 cases); without 2018 it is 0.62 (t 5.06, 163 cases).
- **F5:** At 14 days, 2018 alone weighs heavily on the cases. Its 13 cases have a mean excess return of -1.03 usual moves (t -5.92); the median excess return of all cases is 0.03 and only 49 % are positive, so the 14-day mean of 0.15 is a small, mixed result.
- **F6:** None of the grades tried here carries the premium significantly:

## Ideas
- No ideas: The tested grading, a deeper fall followed by a larger rebound, is absent at every horizon from 1 to 21 days (F1, F2), so narrowing it to a shorter horizon or a part of the data would not make it show; the panic premium appears only as a flat level over 1 to 3 days (F3, F4), with no grade that carries it (F6), and that is the clear answer.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
