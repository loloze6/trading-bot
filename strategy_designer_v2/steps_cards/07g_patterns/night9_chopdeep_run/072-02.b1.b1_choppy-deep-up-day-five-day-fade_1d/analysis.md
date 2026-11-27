---
line: 7.g patterns
backtest: 072-02.b1.b1_choppy-deep-up-day-five-day-fade_1d
idea tested: 072-02.b1.b1_choppy-deep-up-day-five-day-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4245 USD
---
## Findings
- **F1:** On up days across all profiles, the next-day move is graded on the depth below the 20-day high in 20-day std units: slope +0.00166 per unit, day-clustered t 2.33, over 5,247 cases on 929 days. The deepest depth quintile then moves -1.05 % beyond drift in calm markets (t -4.87, n 617, mean depth -6.2) and -1.07 % in agitated markets (t -3.42, n 433). That is about 5 times the 0.22 % cost of a trade.
- **F2:** The tested five-day horizon throws the effect away. Over 5 days, shallow up days near the high rise strongly: +3.45 % beyond drift in trend profiles (t 3.36, n 232) and +10.7 % in choppy markets (n 49). Only the deepest choppy up days fall (-8.5 %, t -3.18, n 24). The step-5 slope over 5 days is t 0.94, so the depth signal lives at the next day.
- **F3:** Inside up days, the depth slope is positive in every calm trend class: choppy calm t 1.09 (1,618 cases), falling calm t 2.30 (542), rising calm t 2.03 (743). In the agitated classes it is near flat: choppy t 0.97, falling t 0.06, rising t 0.29. The grading lives in calm markets.
- **F4:** The depth slope has the same sign in all 12 windows w7 to w18 (t 0.08 to 1.07 each) and in every year 2018 to 2021 (t 0.50 to 1.47). The effect is spread out, not carried by one period.
- **F5:** On down days, depth predicts nothing for the next day: slope t 0.73 in calm markets and -0.10 in agitated ones, on 5,028 cases. This contradicts the brief's claim that the effect holds whatever the day's sign.
- **F6:** In the choppy profile itself, the deepest up-day quintile falls -1.50 % the next day (t -2.95, n 125), but the other quintiles sit between -0.11 % and -0.26 % with no order. The brief's choppy profile adds no grading of its own beyond the deepest tail.
- **F7:** Other angles produced no pattern I treat as a finding.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `072-02.b1.b1.g1_calm-deep-up-day-next-day-fade` (from F1, F2, F3, F4, F5): In a calm market, on a day that closed up, the further the close sits below the coin's 20-day high, in units of its 20-day daily-return standard deviation, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
