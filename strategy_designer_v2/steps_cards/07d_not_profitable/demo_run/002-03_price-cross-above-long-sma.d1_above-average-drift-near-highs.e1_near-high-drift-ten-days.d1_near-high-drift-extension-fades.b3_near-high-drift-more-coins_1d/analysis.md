---
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins_1d
idea tested: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5818 USD
---
## Findings
- **F1:** The book's loss comes from the extension penalty, which goes short in the trending regime. On the 4887 trending bars held short because ext30 was at or below -1, the book lost 0.001162 per bar after fees, while the coin rose 0.00542 per bar. On every other trending bar the book earned +0.000452 (long) or +0.000115 (short at the low end of the range).
- **F2:** Extended runs keep rising rather than fading. On the 513 extended grid cases (ext30 at or below -5, mean 30-day return of 116%), the excess 10-day return was +0.0241 (t 2.63). Within them, the slope of that return on the 30-day return was flat (t -0.01), so the larger extension brings no smaller rise.
- **F3:** Over the whole trending regime, the 30-day return predicts the next 10 days with a positive slope (t 3.48, 1547 cases). The excess 10-day return rises from -0.031 in the lowest 30-day-return quintile to +0.022 to +0.032 in the top two.
- **F4:** The idea's own range part works. The slope of the excess 10-day return on range position is t 3.07 (1547 cases), and the top range quintile earns +0.0515. Combining range rank with 30-day-return rank sorts outcomes monotonically, from -0.031 to +0.032 across quintiles (about 310 cases each).
- **F5:** Because of the penalty, the book is short far more often than long: 10327 short bars against 5802 long, in coins that rose 0.0015 a day. This gives a market part of -0.000048 per bar and a book Sharpe of -0.19, against 0.51 for holding.
- **F6:** The failing measures move with the penalty removed:

## Ideas
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins.d1_extended-runs-keep-rising` (from F1, F2, F3, F4, F6): While a coin's close is above its 200-day average, the higher its close sits in its 20-day close range, the larger its rise over the next 10 days, and the larger its 30-day return, the larger that rise grows further.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins.d2_momentum-above-long-average` (from F2, F3, F5): While a coin's close is above its 200-day average, the larger its 30-day return, the larger its rise over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
