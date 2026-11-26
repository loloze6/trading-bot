---
line: 7.b inconclusive
backtest: 059-02.b1_falling-calm-declines-extend_1d
idea tested: 059-02.b1_falling-calm-declines-extend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3434 USD
---
## Findings
- **F1:** Step 5's result points the way the idea predicts but is too weak to decide: the slope of the drift-adjusted 5-day return on the forecast is +0.00096, with a day-clustered t of 1.06 (608 grid cases on 246 days). The mean short unusual move is above 0 (+0.25 %), and the idea's size is +0.41 % per case, t 0.84 over 420 days, a strength of 0.033 of a usual 10.60 % move.
- **F2:** On the folds I can see (B, C), the effect is graded across the whole forecast range. At 5 days the in-profile cases (forecast below 0) run from -2.40 % unusual move in the deepest forecast quartile (mean forecast -19.4) through -1.37 % and -0.25 % to +1.82 % in the shallowest (mean -2.9), 91 cases per quartile. The plain OLS slope t is 3.07 on 340 cases, and the same holds on the recomputed raw depth (t 2.76, 203 cases).
- **F3:** The slope is positive in all six coins at 5 days. Its t is 2.49 for ETH (49 cases), 1.87 for LTC (75), 1.40 for BTC (39), 1.39 for XMR (56), 0.64 for ZEC (69) and 0.35 for XRP (52). It is also positive in every year from 2018 to 2021 (t 2.16, 0.53, 2.23, 1.02). Each slice is too small to clear 2 on its own, so the effect is spread thinly rather than living in one part of the data.
- **F4:** The test measured the effect at a horizon where it is already fading. On the in-profile grid the slope t is 3.79 at 1 day (1,749 cases), 4.58 at 3 days (576), 3.07 at 5 days (340), 0.79 at 10 days (164) and 0.12 at 20 days (86). The continuation is strongest over about three days. These are plain OLS t's that do not take cases of one day together, so they overstate step 5's clustered t.
- **F5:** Outside the falling calm profile, among falling coins, deeper declines are followed by relatively larger rises, the brief's agitated-market rebound. The 5-day slope on depth is -0.0096 (t -2.02, 141 cases), against +0.0093 (t 2.76, 203 cases) for the same depth inside the profile.
- **F6:** The book barely covers its cost because the coins' normal drift works against a short. The normal drift in the short direction is -0.66 % per 5 days, so the total move per case is -0.24 %, against a cost of 0.19 % per trade. The unusual move is 2.1 times the cost, and the book's Sharpe of 0.28 trails holding by 0.29.

## Ideas
- `059-02.b1.b1_falling-calm-declines-more-coins` (from F1, F2, F3): In a falling, calm market, the further a coin's close sits below its highest close of the past 14 days, measured in units of its own 30-day daily swing, the larger its fall over the next 5 days.
- `059-02.b1.b2_falling-calm-declines-three-days` (from F2, F4, F5): In a falling, calm market, the further a coin's close sits below its highest close of the past 14 days, measured in units of its own 30-day daily swing, the larger its fall over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
