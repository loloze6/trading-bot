---
line: 7.b inconclusive
backtest: 067-02_choppy-down-stretch-keeps-falling_1d
idea tested: 067-02_choppy-down-stretch-keeps-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3778 USD
---
## Findings
- **F1:** In the folds shown (B, C), the plan's forecast lost the idea's gradient: on the 10-day grid's short cases, the 10-day move net of drift has a slope of +0.0022 on the forecast's size (t 0.61, 77 cases), the step-5 sign of reversion. On the idea's own raw stretch (the close's distance below its 20-day average in 20-day daily swings), the same cases give a slope of +0.016 (t 1.05, 70 cases), which is continuation. The standardised stretch gives -0.007 (t -0.30, 46 cases), so the 60-value standardisation in the plan is what removed the gradient.
- **F2:** On the raw stretch, the choppy below-average cases fall in steps over 10 days. By quartile of stretch, the net-of-drift move goes from -7.7 % in the deepest quartile (mean stretch -3.2 swings, 18 cases) to -6.4 %, -4.3 % and -0.1 % in the shallowest (-0.36 swings, 18 cases). This is the idea's graded fall, but with about 70 cases the regression stays at t 1.05.
- **F3:** The effect is mixed across years. On the 10-day raw slope, 2020 is strongly continuation (+0.107, t 4.6, 16 cases), while 2018 (-0.044, t -2.3, 21 cases) and 2021 (-0.054, t -1.6, 14 cases) point the other way. The 5-day slope (t 1.93, 128 cases) drops to -0.003 (t -0.44) once the 5 % largest moves are removed, so it rests on a few outliers. At 10 days, removing those moves keeps the slope at +0.013 (t 1.04, 66 cases).
- **F4:** The continuation lives in the choppy profile only. Over all profiles, the below-average raw stretch shows no gradient (10 days: -0.0003, t -0.05, 379 cases; 5 days: -0.003, t -0.87, 753 cases). In choppy markets, both sides pooled give slopes with t 3.29 at 5 days (249 cases) and t 2.33 at 10 days (126 cases). The agitated and calm subsets show the same sign, at t 1.09 (26 cases) and 0.50 (44 cases).
- **F5:** Step 5's result is near zero and on the reversion side: slope +0.0007, t 0.44, 200 cases. Its size is an unusual move of +0.32 % per case in the short direction, with a strength of 0.030 and t 0.44 over 324 days. That is 1.7 times the 0.19 % cost of a trade, while the total move is -0.82 % against the short.

## Ideas
- `067-02.b1_raw-swing-stretch-keeps-falling` (from F1, F2, F4, F5): In a choppy market, the further a coin's close stands below its 20-day average, counted in units of its current 20-day standard deviation of daily returns as it stands that day, the more the coin falls over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
