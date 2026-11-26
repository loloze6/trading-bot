---
line: 7.g patterns
backtest: 058-02.b1.g1.b2_agitated-falling-rally-fades_1d
idea tested: 058-02.b1.g1.b2_agitated-falling-rally-fades
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4074 USD
---
## Findings
- **F1:** In the falling agitated profile, the higher a coin closes within its day's range, the lower its next-day unusual return: the slope is -3.15 % per unit of close position, t -2.95 with errors clustered by day (1298 bars, 467 days). Read by fifths, the next-day return runs from +1.24 % for the lowest fifth (t 2.03, 118 days) through +0.37 %, +0.08 % and -0.64 % to -0.57 % for the highest fifth (t -1.21, 110 days). Both ends are well above the 0.19 % cost of a trade.
- **F2:** The same slope is not there outside the agitated falling market. In falling calm it is -0.11 % (t -0.13, 371 days). In rising markets it is +0.06 % (t 0.08). In choppy markets (calm and agitated together) it is -1.10 % (t -1.20, 345 days). So the reversion to the middle of the day's range lives in the agitated falling market, not in the choppy calm market the brief named.
- **F3:** The tested fade of up days in falling agitated is not graded by the size of the rise. On up days the slope against the scaled rise is +0.66 % (t 1.00, 225 days). Rises of 0.3 to 1 usual swings are followed by -1.63 % (t -4.84, 234 bars), while rises of 1 to 2 swings are followed by +0.64 % (t 0.76, 90 bars). The fall concentrates on moderate up days that close in the upper half of their range: -1.37 % (t_day -3.07, 114 days), against -0.04 % for larger rises closing high (54 days).
- **F4:** Year by year, the up-day slope in falling agitated is unstable: +0.60 (t 0.54) in 2018, +0.35 (t 0.38) in 2019, -1.27 (t -1.45) in 2020 and +3.95 (t 2.65) in 2021. This matches the step-5 t of -0.49 and the book's yearly return of +1.2 % with a Calmar of 0.10.
- **F5:** Down days in falling agitated are followed by next-day rises at every size. Falls of 0.3 to 1 swings give +1.50 % (t 5.13, 262 bars), falls of 1 to 2 swings give +1.82 % (t 2.82, 110 bars), and falls beyond 2 swings give +4.48 % (t 3.02, 32 bars). This rebound is already held on the profile map (falling agitated scaled fall next day rebound and its family).
- **F6:** The weekday pattern does not hold year to year, given the seven weekdays looked at. Wednesday's next-day return is -0.50 % (t -2.78), and Thursday and Friday give +0.41 % and +0.38 % (t 2.80, 2.74). By year, Wednesday is -1.60 % (t -3.29) in 2019 but +0.21 % in 2021. A late-week gain is already on the map (045-01).

## Ideas
- `058-02.b1.g1.b2.g1_falling-agitated-close-in-range-reversion` (from F1, F2, F3): In a falling, agitated market, the higher a coin's close sits within that day's high-to-low range, the lower its return over the next day.
- `058-02.b1.g1.b2.g2_agitated-falling-high-close-fade` (from F1, F3): In a falling, agitated market, the nearer a coin's up day closes to the day's high, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
