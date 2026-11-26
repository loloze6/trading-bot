---
line: 7.g patterns
backtest: 058-02.b1.g1.b1.b2.b2_agitated-downtrend-sharp-fall-rebound_1d
idea tested: 058-02.b1.g1.b1.b2.b2_agitated-downtrend-sharp-fall-rebound
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4095 USD
---
## Findings
- **F1:** In the falling agitated bars (15.2 % of all coin-days), the next-day excess return falls steadily as the close moves up the day's range. Closes in the bottom fifth return +1.95 % (281 cases, t 2.64, cases of one day taken together); the middle fifth returns +0.10 %; the top two fifths return -0.76 % and -0.69 %. The slope on close location is -0.030 per unit (1510 cases, t -2.81). This low-close rebound in a falling agitated market is already held on the profile map (045-01, 039-02, 039-02.d1 in falling agitated long).
- **F2:** The tested fall-size grading shows up in falling agitated next-day returns: +1.52 % (t 1.96) for falls of 0.75 to 1.5 usual swings, +1.94 % (t 2.18) for 1.5 to 2.5 swings and +5.69 % for larger ones (only 22 cases, t 1.17). It is a one-day effect. On the 3-day grid, falls of 0.75 to 1.5 swings return +0.21 % (t 0.06), and the close-location slope over 2 days is -0.0099 (t -0.76).
- **F3:** In falling agitated markets, small up days (0 to 0.75 swings) are followed by -1.13 % the next day (451 cases, t -2.44). This is not graded:
- **F4:** Outside falling agitated markets, close location predicts weakly (slope -0.0083, 8393 cases, t -2.03). Split by trend, the slope is not significant anywhere:
- **F5:** Large up days in rising markets show a faint continuation that is not significant. Up days of 1.5 to 2.5 swings return +0.82 % (t 1.37), larger ones +1.29 % (t 1.07), and the up-day slope is +0.0046 (1094 cases, t 1.61). Rising-market momentum is already held (034-01.e1, 034-02).
- **F6:** Weekday shows no pattern. No weekday's next-day mean reaches |t| 1.5 over all bars (largest Friday +0.37 %, t 1.44). In falling agitated bars the largest is Tuesday, +1.25 % (t 1.67).

## Ideas
- No ideas: Across about 80 groupings, the only pattern that clearly stands out is the falling agitated low-close rebound (F1, t -2.81), and the portfolio already holds it in that profile. The up-day fade (F3, t -2.44) is not graded and does not stand out given how many angles were examined. The choppy close-location pull that the brief's theme needs does not reach significance in any trend (F4).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
