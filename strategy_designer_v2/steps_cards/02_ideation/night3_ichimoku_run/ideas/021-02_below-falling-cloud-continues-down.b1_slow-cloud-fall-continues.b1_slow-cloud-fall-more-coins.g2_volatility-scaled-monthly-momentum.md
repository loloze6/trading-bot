---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues.b1_slow-cloud-fall-more-coins
line: 7.g patterns
backtest: 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues.b1_slow-cloud-fall-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's return over the next 26 days is higher the larger its past 26-day return is relative to its own daily volatility over the past 60 days.
Consequence: A coin with a strong volatility-scaled 26-day rise is a reason to hold it long, and one with a strong volatility-scaled 26-day fall is a reason to stay out or go short.
Why:
- F3: Across all grid bars, a coin's 26-day return scaled by its volatility predicts its next 26 days. The time-clustered rank slope was 0.25 (t 2.42, 299 cases, 24 cells), the bottom tercile ran -0.31 usual moves against +0.19 for the top tercile, and the top tercile beat the bottom in 15 of 16 coins. The unscaled 26-day return gave quintile excesses from -5.9 % (t -3.3) to +10.0 % (t 2.2), Spearman 0.098 (p 0.003, n 897, clustered t 1.92).
- F4: The book's loss came from bull years. Its mean daily return was +0.15 % in 2018 while the coins fell 0.35 % a day, and -0.06 % to -0.07 % in 2020, 2023 and 2024 while the coins rose 0.28 % to 0.44 % a day. Trending-grid forward returns were +24 % to +36 % in 2020, 2021 and 2023 (t 3.0 to 4.8).
- F2: Inside the trending regime, the past 26-day return sorts what follows far more than the cloud's slope does. The two lowest quartiles of the past 26-day return had excess 26-day returns of -15.4 % (t -6.4, 24 cases) and -16.5 % (t -3.2, 23 cases); the two highest had +3.4 % and +9.2 % (rank slope 0.37, time-clustered t 1.65 over 13 month-cells). The tested slow-fall gradient split at -0.12 Welch t.
