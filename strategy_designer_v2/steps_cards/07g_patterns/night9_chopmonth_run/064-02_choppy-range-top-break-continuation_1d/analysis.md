---
line: 7.g patterns
backtest: 064-02_choppy-range-top-break-continuation_1d
idea tested: 064-02_choppy-range-top-break-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4358 USD
---
## Findings
- **F1:** In choppy markets (60-day return between −10 % and +10 %), the 10-day return scaled by the 30-day swing sorts the next 5 days on its down side, not its up side. The bottom quartile (z10 from −1.97 to −0.45) has a mean unusual move of −7.16 % (t −3.27, 48 non-overlapping cases, strength −0.55). The two middle quartiles sit at −1.60 % (t −1.18) and −1.19 % (t −1.04). The top quartile is +11.3 % but not sure (t 1.34). These t's are ordinary, not day-pooled.
- **F2:** The choppy down-side continuation holds across the shown data, where z10 < 0. It is negative in every year: 2018 −7.6 % (t −2.06, n 9), 2019 −3.8 % (t −3.24, n 28), 2020 −3.7 % (t −1.05, n 28) and 2021 −7.3 % (t −3.46, n 24). It is negative on all 12 coins, from −1.3 % to −11.7 %. It is negative in 9 of 12 windows, with w12 at −9.5 % (t −4.56, n 20) and w16 at −32.9 % (n 6). Three windows go against it: w10 +7.3 %, w17 +1.3 % and w18 +7.6 %. Without w16 the effect is smaller but still negative.
- **F3:** The 5-day and 1-day falls tell the same story in choppy markets. A 5-day fall scaled between −1.5 and −0.5 swings is followed by −5.2 % (t −3.00, n 31). Below −1.5 swings it is −16.0 % (t −2.43, n 10). A 1-day fall of 1 to 2 swings is followed by −5.8 % (t −2.35, n 9). The brief's claim that falls in a choppy market are not followed by more falling is contradicted.
- **F4:** The grading on the past move is strongest in choppy markets. The slope of the 5-day unusual move on z10 is 0.069 (t 2.52, n 189) in choppy markets, against 0.010 (t 2.07, n 527) in falling and 0.011 (t 1.96, n 484) in rising. On z1 the choppy slope is 0.098 (t 3.99). The choppy slope on z10 holds both when the 30-day swing is above its 90-day median (0.044, t 2.03, n 56) and when it is below (0.066, t 1.78, n 133).
- **F5:** The tested breakout's up side rests on a few outsized cases. In choppy markets, closes 1 to 2 swings above the 30-day high are followed by +9.9 % (t 1.90, n 15), and closes above 2 swings by +78 % (t 1.02, n 5). Closes far below the 30-day high (dhi below −3) are followed by −5.1 % (t −3.69, n 85). The steep dhi slope (t 4.21) comes from both tails, and only the low tail is steady. This matches the step-5 mean of +2.39 % with a day-pooled t of 1.27.
- **F6:** One calendar pattern stood out. 5-day windows starting on a Wednesday close have a mean unusual move of −3.6 % (t −3.94, n 176), negative in each year from 2018 to 2021 (−4.9 %, −3.6 %, −7.4 %, −0.9 %). It is one of many angles looked at and has no theory, so no idea is drawn from it.

## Ideas
- `064-02.g1_choppy-scaled-slide-continues-down` (from F1, F2, F3, F4): In a choppy market, a coin whose 10-day return is negative keeps falling over the next 5 days. The larger that 10-day fall in units of its 30-day daily swing, the larger the further fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
