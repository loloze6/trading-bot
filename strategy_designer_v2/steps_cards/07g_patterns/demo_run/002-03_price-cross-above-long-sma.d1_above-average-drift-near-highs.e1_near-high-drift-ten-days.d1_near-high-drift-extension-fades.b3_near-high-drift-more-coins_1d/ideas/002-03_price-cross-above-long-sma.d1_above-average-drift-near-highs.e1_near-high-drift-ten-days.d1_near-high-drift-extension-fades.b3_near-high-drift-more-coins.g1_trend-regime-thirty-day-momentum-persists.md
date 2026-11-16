---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the larger its 30-day return, the larger its rise over the next 10 days, including at the largest 30-day returns.
Consequence: A trader in an up-trending coin would size a long up with the strength of its 30-day run instead of cutting it back when the run grows large.
Why:
- F1: Above the 200-day average, the 30-day return predicts the next 10 days with a rising slope and no fade at the top: the slope on its within-coin rank is 0.0884 (t 4.31, 1165 cases), and the top decile (30-day return 59% to 730%) still beats the coin's average by +0.038 (t 1.32), so the "extended run fades" half of the idea is not in the bars.
- F3: The extension penalty points the wrong way: the slope of excess 10-day return on ext30's post value is −0.0020 (t −2.70, 1165 cases), meaning larger penalties came before higher returns. The penalty pushed 64% of trending bars to a negative forecast (mean ext30 post −5.70).
- F4: The book lost through that misplaced short side: trending bars held short averaged −0.000424 per bar over 9946 bars (sum −4.22), long bars averaged +0.000565 over 5555 bars (sum +3.14), and the book's Sharpe was −0.19 while holding the coins made +0.0014 a day.
- F5: The 10-day return carries the same trend persistence above the 200-day average: the raw slope is 0.1637 (t 5.94, 1165 cases), the rank slope is positive in 12 of 15 coins (80%) and in 6 of 8 years (2024 t 3.82, 2020 t 2.52). Below the 200-day average it is absent (rank slope 0.0025, t 0.19, 1489 cases).
