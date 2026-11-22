---
line: 7.d not profitable
backtest: 023-01_flat-range-top-reverts-down_1d
idea tested: 023-01_flat-range-top-reverts-down
step 5: mismatch
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5370 USD
---
## Findings
- **F1:** The idea has no size in this data: over 1235 non-overlapping 5-day cases the unusual move is −0.16 % (strength −0.007, t −0.55) and the total move is −0.08 %, against a cost of 0.19 % per trade, so no holding, sizing or threshold could make the book pay.
- **F2:** The theory's own test fails. Reversion toward the middle of the 30-day range is nil in flat coins (mean signed excess move 0.011 usual moves, t 0.39, 917 cases). In trending coins (ratio above 0.33) the move goes the other way, away from the middle (−0.072, t −2.93, 1638 cases): a trend that continues, not a reversion.
- **F3:** The book's falls come from shorts held against rising coins. The chained book reaches its deepest fall of −50 % (yearly return 1.4 %, hence Calmar 0.03) through w15–w19, where the drawdown goes from −12 % to −50 %. There the short days lost 0.140 % a day (sum −1.34) while the coins rose 0.53 % a day, against −0.013 % a day for shorts in the other windows.
- **F4:** Over the whole record, the long side made money and the short side lost it. Long trades returned +1.85 % net on average (2236 trades) and short trades −1.16 % (1491). Long book-days earned 0.057 % a day, short book-days lost 0.040 % a day.
- **F5:** Against holding, the book loses on both gain and risk. It earns 0.0075 % a day (Sharpe 0.16), against 0.118 % a day for holding (Sharpe 0.55). Its gain splits into 0.0038 % from the market's own rise and 0.0037 % from timing, with only 22 % of the book invested on average.
- **F6:** The reversion is not graded inside flat coins. By distance from the middle, the excess 5-day move runs −0.027, 0.003, 0.018, 0.069, −0.124 (t −1.83 for the top fifth, at +9 % above the middle). Above the middle, the correlation between distance and move is −0.067, and the bottom fifth shows no rise (−0.027).
- **F7:** In flat coins, reversion from above the middle shows only after a 90-day rise. There it is 0.258 usual moves (t 1.83, 55 cases), against −0.165 (t −1.38, 48 cases) after a 90-day fall. From below the middle it is negative in both cases (−0.068 and −0.110).
- **F8:** In trending coins, the 30-day move continues over the next 5 days, more strongly the larger it is, except for the very largest moves:

## Ideas
- `023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise` (from F3, F4, F6, F7): In a coin whose 30-day net move has been small relative to its 30-day high-low range, the further its close sits above the middle of that range, the more it falls over the next 5 days, only while its 90-day return is positive.
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days` (from F2, F8): In a coin whose 30-day net move has been large relative to its 30-day high-low range, the larger its 30-day return, the further the coin moves in that same direction over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
