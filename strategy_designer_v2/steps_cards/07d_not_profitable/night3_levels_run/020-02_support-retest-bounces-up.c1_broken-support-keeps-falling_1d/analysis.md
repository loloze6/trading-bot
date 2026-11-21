---
line: 7.d not profitable
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling_1d
idea tested: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3629 USD
---
## Findings
- **F1:** The book loses because it is short most of the time in coins that rise. It is short on 69 % to 80 % of bars, with a mean position of -0.41 to -0.58. Its gain from the market's own rise is negative on every coin (-0.031 % to -0.069 % per bar). Its timing gain is positive on 5 of 6 coins (+0.018 % to +0.060 % per bar) but smaller. So the idea's total move per case is -0.47 % over 5 days, against a cost of 0.19 %.
- **F2:** The book stays short even where no cluster of past lows sits near the close. On bars with no swing low within 3 % above the close, its mean position is -0.36 and it is short 68 % of the time (13,384 bars), losing 0.039 % per bar. The standardised, negated forecast turns any low above the close, however far, into a short.
- **F3:** The short gains only where the level is close. With the nearest past low within 1 % above the close, the book gains +0.13 % per bar (1,932 bars). With it 7 % to 15 % above, it loses 0.10 % per bar (1,612 bars). With it more than 15 % above, it loses 0.13 % per bar (1,008 bars).
- **F4:** The count of swing lows within 3 % above the close grades the next 5 days' move (unusual move, non-overlapping cases):
- **F5:** The graded fall is broad. With 3 or more such lows, the 5-day unusual move is negative on all 6 coins (-0.8 % to -6.1 %) and in 7 of 8 years (-1.7 % to -7.2 %; 2020 is the exception at +4.5 %).
- **F6:** The fall is concentrated when the close is below its 50-day average.
- **F7:** The book's own forecast is graded but too wide. Short cases in the top half of |forecast| have an unusual short-side move of +0.86 % (t 3.09, n 1,179). The weakest quarter has -0.44 % (n 590). The weak cases dilute the edge toward the verdict's +0.12 %, and each one pays the coin's rise.

## Ideas
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d1_clustered-broken-support-in-downtrend` (from F1, F2, F4, F5, F6): When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 5 days, and the more such past turning-up lows lie within a few percent above the close, the larger the fall, only while the close is below its 50-day average price.
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.d2_tight-cluster-of-broken-lows` (from F1, F2, F3, F4, F5, F7): When a coin's daily close sits just below prices where it turned up several times in the past 90 days, it tends to fall over the next 5 days, and the more such past turning-up lows lie within a few percent above the close and the nearer the closest of them, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
