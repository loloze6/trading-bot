---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down
line: 7.d not profitable
backtest: 023-01_flat-range-top-reverts-down_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been small relative to its 30-day high-low range, the further its close sits above the middle of that range, the more it falls over the next 5 days, only while its 90-day return is positive.
Consequence: A trader would sell the top of a flat range only after a 90-day rise, and would not short a flat range that followed a 90-day fall.
Why:
- F3: The book's falls come from shorts held against rising coins. The chained book reaches its deepest fall of −50 % (yearly return 1.4 %, hence Calmar 0.03) through w15–w19, where the drawdown goes from −12 % to −50 %. There the short days lost 0.140 % a day (sum −1.34) while the coins rose 0.53 % a day, against −0.013 % a day for shorts in the other windows.
- F4: Over the whole record, the long side made money and the short side lost it. Long trades returned +1.85 % net on average (2236 trades) and short trades −1.16 % (1491). Long book-days earned 0.057 % a day, short book-days lost 0.040 % a day.
- F6: The reversion is not graded inside flat coins. By distance from the middle, the excess 5-day move runs −0.027, 0.003, 0.018, 0.069, −0.124 (t −1.83 for the top fifth, at +9 % above the middle). Above the middle, the correlation between distance and move is −0.067, and the bottom fifth shows no rise (−0.027).
- F7: In flat coins, reversion from above the middle shows only after a 90-day rise. There it is 0.258 usual moves (t 1.83, 55 cases), against −0.165 (t −1.38, 48 cases) after a 90-day fall. From below the middle it is negative in both cases (−0.068 and −0.110).
