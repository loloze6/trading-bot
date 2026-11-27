---
line: 7.g patterns
backtest: 067-02.b1.b1_two-sided-swing-stretch-five-days_1d
idea tested: 067-02.b1.b1_two-sided-swing-stretch-five-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4643 USD
---
## Findings
- **F1:** In the choppy profile (17 % of bars), the stretch carries on the side below the average only: grid cases with a negative forecast (close below the 20-day average) had a 5-day excess return of -3.22 % (day-clustered t -2.36, 128 cases on 80 days), against +0.003 % (t 0.00, 121 cases on 69 days) for cases above the average, so the tested two-sided idea fails on its long side.
- **F2:** The choppy carry sits in agitated choppy bars, where 5-day excess returns averaged -5.50 % (t -2.91, 58 cases on 46 days) against -0.48 % (t -0.53, 191 cases on 99 days) in calm choppy bars. Agitated choppy cases more than one swing below the average averaged -7.20 % (t -1.80, 24 cases), against -1.97 % (t -1.20, 54 cases) for calm ones.
- **F3:** In choppy bars the downside is graded by the coin's own recent fall: from the lowest to the highest quintile of the 20-day return, the 5-day excess was -5.48 % (t -2.30, 32), -3.58 % (t -2.90, 57), -1.04 % (t -1.32, 72), +0.62 % (t 0.57, 61) and +0.18 % (t 0.06, 27). The lowest quintile of the 5-day return gave -6.51 % (t -2.70, 34), with nothing comparable on the rising side.
- **F4:** Inside the choppy side below the average, the stretch itself grades poorly: slope 0.015 (day-clustered t 0.97, 128 cases), and by band -6.29 % beyond 2 swings (t -1.81), -1.01 % from 1 to 2 swings (t -0.64) and -2.65 % from 0 to 1 swing (t -2.43). The 20-day return (F3) orders the fall better than the swing-scaled distance does.
- **F5:** The book's trades do not capture the short-side grid effect. Short trades lost -1.79 % net on average (t -4.12, 519 trades) while long trades earned +1.23 % (t 2.24, 402 trades). The book's daily return was positive only in 2020 (t 2.45), and its yearly return was +2.6 %.
- **F6:** Outside the choppy profile the stretch continues in rising markets, with slope 0.0105 (t 2.06, 318 cases), which the map already holds (034-01, 033-03.b2). In falling calm bars the slope was 0.0131 (t 2.14, 154 cases) and in falling agitated bars -0.0014 (t -0.22, 247 cases). Against the roughly 20 groupings examined, the falling calm result does not stand out enough to count.
- **F7:** Coin daily returns were strongly positive on Fridays (+0.54 %, t 3.75, 1237 coin-days) and Saturdays (+0.58 %, t 4.24, 1236 coin-days). This is a calendar condition that cannot be graded, and late-week gains in rising markets are already held (045-01), so I propose no idea from it.

## Ideas
- `067-02.b1.b1.g1_agitated-chop-downside-stretch-carries` (from F1, F2, F4): In a choppy, agitated market, the further a coin's close stands below its 20-day average, counted in its current 20-day standard deviation of daily returns, the more the coin keeps falling over the next 5 days.
- `067-02.b1.b1.g2_choppy-twenty-day-fall-continues` (from F1, F3): In a choppy market, the larger a coin's fall over the past 20 days, the more it keeps falling over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
