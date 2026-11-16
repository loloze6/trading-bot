---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades.b3_near-high-drift-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the more negative its 30-day return, the further it falls below its usual return over the next 10 days.
Consequence: A trader would refuse longs, or lean short, in a coin still above its long average whose last month has been falling, more so the deeper the fall.
Why:
- F2: In the same regime, the bottom 30-day-return deciles (−55% to −4%) trail the coin's average over the next 10 days by −0.042 (t −3.35, 117 cases) and −0.037 (t −3.15, 116 cases), the clearest one-sided effect found.
- F5: The 10-day return carries the same trend persistence above the 200-day average: the raw slope is 0.1637 (t 5.94, 1165 cases), the rank slope is positive in 12 of 15 coins (80%) and in 6 of 8 years (2024 t 3.82, 2020 t 2.52). Below the 200-day average it is absent (rank slope 0.0025, t 0.19, 1489 cases).
