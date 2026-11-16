---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days.d1_near-high-drift-extension-fades_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is above its 200-day average, the higher its close sits in its 20-day close range, the larger its rise over the next 10 days, except when its 30-day return is already extended, where the larger that 30-day return, the smaller the rise over the next 10 days.
Consequence: A trader would scale a long by how near the close is to its 20-day high above the long average, and cut it back as the coin's 30-day run grows very large, which is where the book's deepest falls start.
Why:
- F1: The tested forecast has almost no link to the next 10 days on trending bars. Its slope t is 0.91 over 833 independent cases, and it stays as weak at other horizons: t 0.44 at 5 days (1674 cases) and t 0.65 at 20 days (408 cases).
- F6: The forecast's effect is mixed across periods and coins, not just small. By year, its slope t ranges from +2.23 in 2021 to -2.75 in 2024. By coin it is under 1.3 in absolute value everywhere, with BTC negative (t -1.28) and XRP the most positive (t 1.30).
