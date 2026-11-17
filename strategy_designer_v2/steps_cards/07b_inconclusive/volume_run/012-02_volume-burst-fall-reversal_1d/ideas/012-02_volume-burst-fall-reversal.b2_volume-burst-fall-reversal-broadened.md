---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-02_volume-burst-fall-reversal
line: 7.b inconclusive
backtest: 012-02_volume-burst-fall-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A, B, C, D
---
Idea: Among bars that fall sharply, the larger the bar's volume relative to the coin's 30-day average volume, the larger the price rise over the next 3 days.
Consequence: The volume burst marks forced, self-feeding liquidation selling, which is retraced, unlike a quiet decline.
Why:
- F3: The 3-day slope changes sign from year to year, so the pooled t is diluted: it is strongly positive in 2020 (t 4.05, n 39) and 2024 (t 3.51, n 56), negative in 2021 (t -2.49, n 50) and 2022 (t -2.35, n 67), and small in the other four years.
- F4: No single coin carries the 3-day result: per-coin slopes range from -0.0014 (LTC, t -0.20) to +0.0078 (XMR, t 1.36), with 65 to 79 cases each and four of six coins positive, so the effect is small next to each coin's noise.
