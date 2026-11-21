---
line: 7.b inconclusive
backtest: 017-02_presettle-rise-after-downtrend_1h
idea tested: 017-02_presettle-rise-after-downtrend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3602 USD
---
## Findings
- **F1:** The test's result leans the way the idea predicts but is weak: slope t is 1.30 and the mean-excess t is 0.36 over 25,569 cases. My recomputed cases show the same pattern, with forecast quintiles rising only from -0.2 bp (t -0.11) to +2.5 bp (t 0.95).
- **F2:** The rise appears only after the deepest raw 3-day falls. Settlement-bar cases in the deepest fall decile (mean fall -13.8%) gain +9.2 bp over 2h (t 2.70, n 5,065), while deciles 2 to 5 are all negative (-1.0 to -2.4 bp). The raw-fall quintiles show the same: the deepest is +9.5 bp (t 2.73), and the next four range from -0.3 to -3.6 bp.
- **F3:** Measured on the raw size of the fall instead of the plan's z-score against its own past 72 values, the pre-settlement 2h excess return grows with the fall depth at 136 bp per unit of fall (t 7.32, n 25,072). The plan's standardised forecast mostly measures how the fall changed recently, not how deep it is.
- **F4:** The rebound after falls is not tied to the funding clock. Over all hours the slope on raw fall is 110 bp (t 16.9, overlapping bars). Inside the deepest decile, settlement bars beat other hours only modestly (+9.2 vs +1.3 bp, Welch t 2.16), and non-settlement hours such as 04 (+14.4 bp, t 2.87) and 11 (+21.8 bp, t 3.28) are as strong as the settlement hours 05/13/21 (+6.2, +11.2, +10.2 bp, t 1.26 to 1.72).
- **F5:** A strong time-of-day pattern drowns the effect. Across all bars, the 2h excess return is -4.7 to -6.1 bp at hours 00 to 02 (t -4.2 to -5.4) and +8.3 bp at hour 20 (t 7.6), while the case hours 05, 13 and 21 sit at +0.4, -2.6 and +2.9 bp.
- **F6:** The effect is mixed across years and coins. The case slope t is 3.20 in 2018 but -3.25 in 2020. Only ZEC has a slope t above 2 (3.11); the other five coins range from -0.25 to 1.31.
- **F7:** The book loses money: Sharpe -3.49 and a mean daily return of -0.148% at 1.70 trades per day. The 2-hour edge of a few bp does not cover its trading.

## Ideas
- `017-02_presettle-rise-after-downtrend.b1_pre-settlement-rise-more-coins` (from F1, F6): For a coin with a strong 3-day run down, the return over the 2 hours before each funding settlement time (00:00, 08:00 and 16:00 UTC) is positive, and the stronger the 3-day fall, the larger that pre-settlement rise.
- `017-02_presettle-rise-after-downtrend.b2_deep-fall-pre-settlement-rebound` (from F2, F3, F4): For a coin with a 3-day run down, the return over the 2 hours before each funding settlement time (00:00, 08:00 and 16:00 UTC) is positive, and the deeper the coin's 3-day percentage fall, the larger that pre-settlement rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
