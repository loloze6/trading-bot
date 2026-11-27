---
line: 7.g patterns
backtest: 072-03.b1.b1.d2_raw-depth-bounce-fade-sizing_1d
idea tested: 072-03.b1.b1.d2_raw-depth-bounce-fade-sizing
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4949 USD
---
## Findings
- **F1:** The book's loss sits almost entirely in one coin-window and a few violent days. DOGE in w10 sums to -4.97 in daily book returns, against -6.79 for the whole book over folds B and C. The 38 days with a book move beyond ±10 % sum to -5.85 of that -6.79. These shorts were lost in a squeeze, not across the many small cases the idea counts.
- **F2:** In a choppy market (60-day return within ±10 %), the 10-day unusual move falls as the close sits deeper below the 20-day high in 20-day swings. This holds over all days, up and down alike, on the 10-day grid at offset 0:
- **F3:** The same choppy grading holds on the grid shifted by 5 days. It runs from +9.2 % (2.5 to 1 swings below, n 19) through -0.5 % (4 to 2.5, n 23) to -11.8 % (6 to 4, t_cl -2.12, 9 days) and -9.0 % (below 6, n 10). The correlation of depth with the 10-day unusual move is 0.29 (96 cases) on one grid and 0.24 (80 cases) on the other.
- **F4:** Restricting to up days, as the tested idea does, keeps the same shape at 10 days but on fewer cases:
- **F5:** The choppy deep cases are concentrated in time, which weakens them. Of the cases deeper than 4 swings on grid 0, 11 fall in w12 (-15.9 %, t_cl -3.51, 5 days) and 5 in w16 (one day). Every other window has 0 to 2 cases.
- **F6:** In a falling market the depth does not grade the 10-day move:
- **F7:** The trade results do not grow with the forecast. Net trade P/L by |entry forecast| quartile, 138 trades each, is -5.4 %, -14.0 %, -7.3 % and -5.2 %. The book's sizing never captured the grading seen in F2 and F3, because F1's squeeze days dominate it.

## Ideas
- `072-03.b1.b1.d2.g1_choppy-depth-graded-ten-days` (from F2, F3, F4, F6): In a choppy market, the further a coin's close sits below its 20-day high, in units of its 20-day daily-return standard deviation, whether the day closed up or down, the lower its return over the next 10 days. The return is a rise when the close sits just under the high and becomes a fall that grows with each further swing below it.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
