---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: On a coin's high-volatility days, measured by its 20-day volatility, the next day's return runs against the day just closed. The larger that day's return relative to its 20-day volatility, the larger the move back over the next 1 day.
Consequence: After a large daily move in a volatile spell, a trader leans against it for one day and refuses to chase it, and does not carry that lean beyond the next day.
Why:
- F1: A coin's one-day return, scaled by its 20-day volatility, reverses on the next day. The Spearman correlation with the next day's excess return is -0.075 (p = 1.5e-7, n = 4834 non-overlapping days). It holds in each coin (BTC -0.070, p = 6e-4; ETH -0.079, p = 9e-5) and in each half of the windows (w1-12: -0.101; w13-24: -0.054, p = 0.008).
- F2: The one-day reversal sits almost entirely in the coin's most volatile third of days, by 20-day volatility. There the correlation is -0.166 (p = 2e-11, n = 1612) and the slope on the raw return is -0.149. In the low and middle volatility thirds it is only -0.027 and -0.027 (p ≈ 0.27–0.28).
- F3: The reversal lasts one day only.
- F4: The one-day reversal is stronger in some years than others. It is significant in 2018 (-0.137), 2019 (-0.086), 2020 (-0.155) and 2023 (-0.138). It is near zero in 2022, 2024 and 2025 (-0.016 to -0.027, p > 0.49), so it varies with the period. Its sign is negative in all 8 years.
