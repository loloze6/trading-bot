---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the higher its close sits in its 20-day close range, the larger its rise over the next 10 days.
Consequence: A trader would scale a long in an up-trending coin by how close it is to its 20-day high, with no penalty for an extended run.
Why:
- F6: Above the 200-day average, closes at the top of the 20-day range lead the next 10 days: the top range quintile beats the coin's average by +0.054 (t 2.95, 260 cases) against −0.016 for the bottom quintile, with a slope of 0.0774 (t 4.33). The 30-day slope was not uniform: in 2018 it was −0.288 (t −3.09, only 32 cases).
- F1: Above the 200-day average, the 30-day return predicts the next 10 days with a rising slope and no fade at the top: the slope on its within-coin rank is 0.0884 (t 4.31, 1165 cases), and the top decile (30-day return 59% to 730%) still beats the coin's average by +0.038 (t 1.32), so the "extended run fades" half of the idea is not in the bars.
- F3: The extension penalty points the wrong way: the slope of excess 10-day return on ext30's post value is −0.0020 (t −2.70, 1165 cases), meaning larger penalties came before higher returns. The penalty pushed 64% of trending bars to a negative forecast (mean ext30 post −5.70).
