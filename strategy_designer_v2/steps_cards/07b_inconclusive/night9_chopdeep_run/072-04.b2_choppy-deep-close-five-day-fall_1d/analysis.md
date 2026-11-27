---
line: 7.b inconclusive
backtest: 072-04.b2_choppy-deep-close-five-day-fall_1d
idea tested: 072-04.b2_choppy-deep-close-five-day-fall
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3587 USD
---
## Findings
- **F1:** Step 5's slope t is 0.04 on 721 cases over 352 days, which is about zero rather than short of the bar. The cause looks like the forecast's standardisation over its past 60 values, not the depth itself. On the same choppy 5-day grid of folds B and C, the excess return regressed on the plan's own measure (close against the 20-day high, divided by the 20-day return std, unstandardised) gives a slope t of 2.11 (249 cases, 128 days). The standardised forecast gives only 1.38 (223 cases, 121 days), although the two correlate at 0.91.
- **F2:** The depth effect grows with the horizon. On raw depth in choppy markets the clustered slope t is 1.01 at 1 day (1,250 cases), 0.98 at 3 days (409), 2.11 at 5 days (249) and 2.61 at 10 days (126). Over 10 days the deepest depth quintile returns -7.9 % against drift (30 cases), while the quintile nearest the high returns +2.7 % (22 cases).
- **F3:** The graded effect is carried by up days. At 5 days the raw-depth slope t is 3.05 after an up day (121 cases, 76 days) but only 0.79 after a down day (128 cases, 79 days). The mean excess return is negative on both sides (-1.95 % after up days and -2.31 % after down days, on the signal cases), so the up-day cases add the grading the down-day cases lack.
- **F4:** The effect is uneven across periods and coins, and this mixed picture is what dilutes the whole-sample test. At 5 days the raw slope t is 0.78 in fold B (153 cases) and 2.52 in fold C (96 cases). Over 10 days by coin it is 2.56 for XRP, 2.33 for ZEC, 1.85 for BTC and 1.76 for LTC, but 0.21 for ETH and 0.07 for XMR.
- **F5:** The book cannot pay at its 5-day horizon. The total move per case is +0.08 %, 0.4 times the 0.19 % trade cost, because the short pays the coins' normal rise (-0.56 % per case) against an unusual move of +0.64 % (t 2.00, 702 days). A move per case that grows with horizon and depth, as in F2, is what could cover the cost.

## Ideas
- `072-04.b2.b1_choppy-deep-close-ten-day-fall` (from F1, F2, F5): In a choppy market, the further a coin's close sits below its 20-day high, in units of its 20-day daily-return standard deviation, the larger its fall over the next ten days.
- `072-04.b2.b2_choppy-deep-up-day-fade` (from F1, F3, F4): In a choppy market, when a coin closes up on the day but its close still sits far below its 20-day high, in units of its 20-day daily-return standard deviation, the further below the high it sits, the larger its fall over the next five days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
