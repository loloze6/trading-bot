---
line: 7.b inconclusive
backtest: 010-04_rsi-below-streak-continuation_1d
idea tested: 010-04_rsi-below-streak-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2685 USD
---
## Findings
- **F1:** The run length itself carries no continuation. At the plan's 14 days the slope of excess return on days below 50 is +0.00105 (t +1.28, 185 grid cases), which is the opposite side to the idea. The longest runs (41–60 days) are followed by +0.047 (n=14), while 1–5-day runs are followed by −0.017 (n=54).
- **F2:** The positive slope comes from fold C. There the correlation of run length with excess return is +0.38 for both BTC and ETH, against −0.15 to +0.04 in the other folds. Without fold C the 14-day slope turns to −0.00045 (t −0.57, n=134), still far from any bar.
- **F3:** Which side of 50 RSI sits on matters more than how long it has been there, and it shows at 7 days rather than 14. Over 7 days the below-50 grid bars average −0.0101 excess (t −1.90, n=406) and the above-50 bars +0.0100 (t +1.76, n=409). Over 14 days the gap shrinks to −0.0068 against +0.0063 (t −0.57 and +0.55).
- **F4:** Over 7 days the RSI level itself is graded across the midpoint. The slope of excess return on 14-day RSI is +0.00053 (t 1.95, n=719). Every bin below 50 averages −0.008 to −0.017, and the bins from 50 to 70 rise from +0.003 to +0.016. Within either side alone the slope is flat (t −0.76 below, +0.25 above).
- **F5:** The side effect holds in both coins and in most folds. Over 7 days BTC averages −0.0081 below 50 against +0.0076 above, and ETH −0.0120 against +0.0126. The below-side mean is negative in folds A, C and D (−0.018, −0.017, −0.005) and only slightly positive in B (+0.003).

## Ideas
- `010-04_rsi-below-streak-continuation.b1_rsi-level-predicts-week-ahead` (from F3, F4, F5): The higher a coin's 14-day RSI at the close, the higher its return over the next 7 days, so the lower the RSI, the lower the return.
- `010-04_rsi-below-streak-continuation.b2_rsi-depth-below-midpoint` (from F1, F2, F3, F4): The further a coin's 14-day RSI sits below 50 at the close, the lower its return over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
