---
line: 7.c rejected
backtest: 069-01_low-range-up-day-fade_1d
idea tested: 069-01_low-range-up-day-fade
step 5: rejected
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4175 USD
---
## Findings
- **F1:** The rejection comes from the sign of the main measure, not from the market. The plan's measure multiplies the next-day excess return by -forecast/10, which is a positive weight, so it scores the coin rising, not the short gaining. In folds B and C that measure is -0.69 % per case (t -2.68, 1879 cases on 637 days). The short's own excess gain is the mirror: +0.69 % (t +2.68). Step 5's size agrees on every fold: the unusual move in the short's direction is +0.54 % per case (t 2.93, 911 days), 0.114 of the coin's usual move.
- **F2:** The direction the idea claims is in the data. Up days in the lowest 0.2 of their 20-day high-low range have a next-day excess return of -0.64 % (t -2.04, 385 cases). Those in 0.2 to 0.4 have -0.81 % (t -4.34, 843 cases). Up days at the top of the range (0.8 to 1) have +0.20 % (t 1.16). The supporting check also passed: deep cases minus non-short up days is -0.49 %.
- **F3:** The grading holds at the extreme of the forecast. Next-day excess returns by forecast are:
- **F4:** The effect is broad across coins and time:
- **F5:** The effect lives outside rising markets. For low-range up days, by the coin's 60-day trend:
- **F6:** The fade is a one-day effect. Low-range up days have a 3-day excess return of -1.45 % (t -1.51) and a 5-day one of +0.22 % (t 0.13). Up days at the top of the range continue over 5 days: +4.0 % (t 3.43).
- **F7:** The size covers the cost of a trade. The total move per case is +0.42 %, 2.2 times the 0.19 % cost, and the unusual move is 2.8 times it. The book still made only +3.6 % a year with Calmar 0.16, so the realised gain is diluted by the range of short sizes: the short cases' mean bar gain is +0.24 %, against the -2.0 % move concentrated below forecast -15.

## Ideas
- `069-01.c1_low-range-up-day-fade-retest` (from F1, F2, F3, F4): When a coin closes up on the day, the lower that close sits within its high-low range of the past 20 days, the larger its fall over the next day.
- `069-01.c2_falling-market-low-range-fade` (from F2, F3, F5): In a falling market, when a coin closes up on the day, the lower that close sits within its high-low range of the past 20 days, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
