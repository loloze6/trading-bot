---
line: 7.b inconclusive
backtest: 072-04_choppy-deep-close-multiday-fall_1d
idea tested: 072-04_choppy-deep-close-multiday-fall
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3569 USD
---
## Findings
- **F1:** The step 5 result is zero, not short of the bar on the predicted side. Over all folds the slope of the 3-day excess return on the forecast is -2.3e-05 with t -0.05 (1398 cases, 634 days), and the size is +0.10 % per case against the idea (t 0.41, 885 days). Even in folds B and C the 3-day slope on depth is only +0.0028 with t 0.84 (408 cases), so more data is not what the test lacks.
- **F2:** The effect grows with the horizon in the choppy profile (folds B, C, slope of excess return on depth, day-clustered t):
- **F3:** The effect sits in the deepest closes only (folds B, C, choppy):
- **F4:** The effect is mixed across periods and coins. At 3 days the deepest fifth falls in 2018 (-3.3 %), 2019 (-1.8 %) and 2020 (-9.4 %) but rises in 2021 (+1.4 %). The 3-day slope is negative for LTC (t -0.57) and ZEC (t -0.77) and positive for BTC, ETH, XMR and XRP (t 0.7 to 1.8). The 10-day deepest fifth is negative in every year and every coin.
- **F5:** The brief's claim that the effect holds after up and down days alike is borne out: 1-day slope t 1.25 after up days and 0.74 after down days; 3-day slope t 1.69 and 0.20.
- **F6:** The same deepening shows outside the choppy profile too (non-choppy slope t 1.94 at 5 days, 1.41 at 10 days). It is not a choppy-only effect, but the brief names choppy, so the profile is kept.
- **F7:** Its size against the cost: at 3 days the total move per case is -1.3 times the 0.19 % trade cost (against the short) and the unusual move 0.5 times. The deepest cases' 10-day excess fall of about 8 % is many times that cost. A clear answer needs the horizon where the move is large.

## Ideas
- `072-04.b1_choppy-deep-close-ten-day-fall` (from F2, F3, F5, F7): In a choppy market, the further a coin's close sits below its 20-day high, in units of its 20-day daily-return standard deviation, the larger its fall over the next ten days.
- `072-04.b2_choppy-deep-close-five-day-fall` (from F2, F3, F7): In a choppy market, the further a coin's close sits below its 20-day high, in units of its 20-day daily-return standard deviation, the larger its fall over the next five days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
