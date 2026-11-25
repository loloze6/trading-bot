---
line: 7.g patterns
backtest: 034-02_rising-break-swings-continues_1d
idea tested: 034-02_rising-break-swings-continues
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4372 USD
---
## Findings
- **F1:** In a choppy market, coins far below their prior 20-day closing high keep falling over the next 5 days, and the fall deepens with the distance. Measured in swings below the high (the 20-day standard deviation of daily returns), the 5-day excess return is:
- **F2:** That choppy-market fall below the high points down in every year seen. For cases more than 2 swings below the high, the 5-day excess return is:
- **F3:** Across all profiles together, the nearer the close sits to its 20-day high in swings, the larger the 5-day excess move:
- **F4:** In rising markets, the gain comes from being at or above the high, not from how far above it the close stands:
- **F5:** The book's trades still rank by entry forecast. Median net gain rises from +0.66 % in the lowest entry-forecast quarter to +5.80 % in the highest (about 170 trades each).
- **F6:** Several other angles stood out at first but did not hold once the cases of one day were taken together:

## Ideas
- `034-02.g1_choppy-deep-below-high-keeps-falling` (from F1, F2): In a choppy market, a coin whose daily close stands many of its own daily swings (over the last 20 days) below its prior 20-day high falls over the next 5 days, more the more swings below that high it stands.
- `034-02.g2_nearness-to-high-every-market` (from F3): A coin's move over the next 5 days is larger the nearer its daily close stands to its prior 20-day high, measured in its own daily swings over the last 20 days: higher near or above the high, lower deep below it.
- `034-02.g3_rising-approach-to-high` (from F4, F5): In a rising market, a coin's rise over the next 5 days is larger the fewer of its own daily swings over the last 20 days its daily close stands below its prior 20-day high, with the largest rise once the close reaches the high.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
