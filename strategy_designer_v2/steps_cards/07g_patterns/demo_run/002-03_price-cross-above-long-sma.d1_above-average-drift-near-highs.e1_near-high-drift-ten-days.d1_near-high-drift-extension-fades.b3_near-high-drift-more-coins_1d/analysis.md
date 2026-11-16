---
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins_1d
idea tested: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6015 USD
---
## Findings
- **F1:** Above the 200-day average, the 30-day return predicts the next 10 days with a rising slope and no fade at the top: the slope on its within-coin rank is 0.0884 (t 4.31, 1165 cases), and the top decile (30-day return 59% to 730%) still beats the coin's average by +0.038 (t 1.32), so the "extended run fades" half of the idea is not in the bars.
- **F2:** In the same regime, the bottom 30-day-return deciles (−55% to −4%) trail the coin's average over the next 10 days by −0.042 (t −3.35, 117 cases) and −0.037 (t −3.15, 116 cases), the clearest one-sided effect found.
- **F3:** The extension penalty points the wrong way: the slope of excess 10-day return on ext30's post value is −0.0020 (t −2.70, 1165 cases), meaning larger penalties came before higher returns. The penalty pushed 64% of trending bars to a negative forecast (mean ext30 post −5.70).
- **F4:** The book lost through that misplaced short side: trending bars held short averaged −0.000424 per bar over 9946 bars (sum −4.22), long bars averaged +0.000565 over 5555 bars (sum +3.14), and the book's Sharpe was −0.19 while holding the coins made +0.0014 a day.
- **F5:** The 10-day return carries the same trend persistence above the 200-day average: the raw slope is 0.1637 (t 5.94, 1165 cases), the rank slope is positive in 12 of 15 coins (80%) and in 6 of 8 years (2024 t 3.82, 2020 t 2.52). Below the 200-day average it is absent (rank slope 0.0025, t 0.19, 1489 cases).
- **F6:** Above the 200-day average, closes at the top of the 20-day range lead the next 10 days: the top range quintile beats the coin's average by +0.054 (t 2.95, 260 cases) against −0.016 for the bottom quintile, with a slope of 0.0774 (t 4.33). The 30-day slope was not uniform: in 2018 it was −0.288 (t −3.09, only 32 cases).
- **F7:** Weekday and next-day-after-large-move patterns did not stand out once days were counted as single cases. Thursday and Friday, clustered by day, gave t 2.22 and 2.84 among seven weekdays tried, which is too weak to count among the many angles looked at.

## Ideas
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins.g1_trend-regime-thirty-day-momentum-persists` (from F1, F3, F4, F5): While a coin's close is above its 200-day average, the larger its 30-day return, the larger its rise over the next 10 days, including at the largest 30-day returns.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins.g2_pullback-above-average-keeps-falling` (from F2, F5): While a coin's close is above its 200-day average, the more negative its 30-day return, the further it falls below its usual return over the next 10 days.
- `002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins.g3_near-high-drift-without-penalty` (from F6, F1, F3): While a coin's close is above its 200-day average, the higher its close sits in its 20-day close range, the larger its rise over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
