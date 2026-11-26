---
line: 7.b inconclusive
backtest: 069-02.d2_agitated-below-high-up-day-fade_1d
idea tested: 069-02.d2_agitated-below-high-up-day-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2179 USD
---
## Findings
- **F1:** Across folds B and C (1,884 cases), up-day closes in agitated markets were followed by a mean next-day fall of +0.53 % beyond the coin's drift in the short direction (t 3.67), but the grading is weak: the slope of the next-day excess return on the forecast's size is -0.000535, with a correlation of only -0.051. This matches step 5's slope of -0.000409 (t -1.70 over 1,517 case days), which has the predicted sign but falls short of -2.
- **F2:** The grading is a step, not a slope: the shallowest fifth of closes (mean forecast size 1.8) is followed by -0.17 % (t -0.48), while the four deeper fifths give +0.60 %, +0.42 %, +0.92 % and +0.85 % (t 2.35, 1.55, 3.17, 2.13). Beyond a shallow depth, a deeper close adds little.
- **F3:** Every one of the six coins points the predicted way, with a positive short mean (+0.31 % to +0.87 %) and a negative slope (-0.00027 to -0.00101). Each coin's t is between 0.66 and 2.30, so each coin alone is too few cases to show the effect clearly.
- **F4:** The effect varies a lot by window, which drowns the grading.
- **F5:** The effect sits in falling trends and is absent in rising ones.
- **F6:** The largest up days (top quarter, a rise of 1.66 of the 20-day swing) are not given back (-0.30 %, t -0.85), while the three smaller quarters give +0.65 % to +0.71 % (t 2.38 to 2.79).
- **F7:** The idea's size is large against its cost: the unusual move is +0.55 % per case (t 2.93 over 979 days, strength 0.119), the total move is +0.42 %, and a trade costs 0.19 %. The open question is only whether the grading is real, and the folds' six coins give too few cases to tell; 13 more coins have daily data in some or all of the folds.

## Ideas
- `069-02.d2.b1_agitated-up-day-fade-more-coins` (from F1, F3, F7): In an agitated market, when a coin closes up on the day, the further that close sits below its 20-day high, measured in units of its 20-day daily swing, the larger its fall over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
