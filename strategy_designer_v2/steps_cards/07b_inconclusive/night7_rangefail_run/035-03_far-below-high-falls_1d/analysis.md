---
line: 7.b inconclusive
backtest: 035-03_far-below-high-falls_1d
idea tested: 035-03_far-below-high-falls
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3559 USD
---
## Findings
- **F1:** The effect shows only in a choppy market (60-day return between -10 % and +10 %). In folds B and C, deep-below-high closes there are followed over 5 days by an unusual fall of 5.04 % in the short direction (strength 0.38, t 2.33, 99 cases on 52 days). In falling markets it is 1.18 % (t 0.82, 388 cases) and in rising markets 2.20 % (t 1.18, 157 cases).
- **F2:** Outside the choppy market the idea is not graded. Over all cases the correlation between depth and the 5-day unusual move is 0.009, and the depth quartiles are flat: deepest 1.33 % (t 0.70), q2 0.93 %, q3 1.62 %, shallowest 0.85 %. This is why the test's overall t (1.99, mean +0.68 %) falls short of the bar.
- **F3:** Inside the choppy market the effect is graded the way the idea predicts. The correlation of depth with the 5-day unusual move is -0.29. The deeper half falls 7.92 % (t 2.18, 50 cases) against 2.09 % for the shallower half (t 1.84, 49 cases), and over 10 days 11.93 % (t 3.84) against 3.05 % (t 1.10).
- **F4:** The choppy-market effect holds in every year of folds B and C: 9.6 % in 2018, 3.2 % in 2019, 3.5 % in 2020 and 7.7 % in 2021, over 5 days. It is positive on the 9 coins with at least 5 cases, from ETH's 1.4 % to XRP's 7.8 % (t 2.85).
- **F5:** In the choppy market the effect is not drowned by the coins' drift. The total 5-day move in the short direction is 3.67 % (t 1.69), and over 10 days it is 5.01 % (t 1.94), about 17 to 23 times the 0.22 % cost of a trade. Over all cases the total 5-day move is -0.07 %, because the coins' upward drift cancels the unusual move.
- **F6:** The tested idea already used every fold and every coin with daily bars, so no more daily data is available. A 426-case group whose 60-day return cannot be computed (the first 60 days of each window) has a mean of -0.09 % (t -0.06) and dilutes the overall result.

## Ideas
- `035-03.b1_choppy-far-below-high-falls` (from F1, F2, F3, F4, F5): In a choppy market, a daily close many daily swings below the coin's 20-day high is followed by a fall over the next 5 days, larger the more daily swings it sits below that high.
- `035-03.b2_choppy-far-below-high-ten-day-falls` (from F1, F3, F5): In a choppy market, a daily close many daily swings below the coin's 20-day high is followed by a fall over the next 10 days, larger the more daily swings it sits below that high.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
