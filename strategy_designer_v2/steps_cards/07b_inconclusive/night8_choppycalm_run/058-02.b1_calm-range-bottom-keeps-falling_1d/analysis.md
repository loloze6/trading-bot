---
line: 7.b inconclusive
backtest: 058-02.b1_calm-range-bottom-keeps-falling_1d
idea tested: 058-02.b1_calm-range-bottom-keeps-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3430 USD
---
## Findings
- **F1:** The tested grading is absent inside the bottom half of the range. On choppy calm 5-day grid cases with the close below the middle, the slope of the excess return on range position is -1.99 % (t -0.58, 90 cases, 58 days), and the correlation of position with excess return is -0.064. That matches step 5's slope t of -0.68 on 281 cases: closes nearer the low are not followed by larger falls than closes just below the middle.
- **F2:** The bottom half does fall as a block, but not in a graded way. In choppy calm, the bottom bucket returns -3.19 % (t -2.06, n 18), the lower-middle bucket -1.51 % (t -1.11, n 40) and the middle bucket -2.77 % (t -2.73, n 52). Step 5's supporting mean is -0.96 % and passes. The forecast quartiles show no order: -3.10 %, -1.74 %, -1.65 %, -3.94 % from most negative to least negative.
- **F3:** The gradient that does exist runs across the whole 20-day range, in the continuation direction: the higher the close, the higher the next 5 days' excess return. On choppy calm grid bars the full-range slope is +3.89 % per unit of position (t 2.01, 178 cases, 92 days). On all bars it is +2.78 % (t 2.42, 1,364 cases, 256 days). It is positive on every coin, with t from 1.54 to 2.01.
- **F4:** Most of this full-range gradient comes from the upper end. Outside choppy calm, the top bucket returns +3.28 % (t 3.39, n 206); the upper-half slope is +3.41 % (t 1.66), against -1.20 % (t -0.38) for the lower half.
- **F5:** The continuation gradient is strongest when the trend is choppy. With the 60-day trend recomputed inside each window, the slope is +8.62 % (t 2.39, 125 cases, 65 days) in choppy markets, +5.78 % (t 2.40) in rising markets and +2.03 % (t 0.83) in falling markets.
- **F6:** The effect is uneven over the years, so the test was drowned partly by period. In choppy calm, the yearly slopes are -2.19 % (2018), -2.13 % (2019), +1.66 % (2020) and +13.8 % (2021, t 2.78). The bottom-half mean is -6.29 % in 2018 but +0.90 % in 2020.

## Ideas
- `058-02.b1.b1_calm-range-position-continues` (from F1, F2, F3, F4): In a choppy, calm market, the higher a coin's close sits within its 20-day high-low range, the larger its rise over the next 5 days.
- `058-02.b1.b2_choppy-range-position-continues` (from F3, F5, F6): In a choppy market, the higher a coin's close sits within its 20-day high-low range, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
