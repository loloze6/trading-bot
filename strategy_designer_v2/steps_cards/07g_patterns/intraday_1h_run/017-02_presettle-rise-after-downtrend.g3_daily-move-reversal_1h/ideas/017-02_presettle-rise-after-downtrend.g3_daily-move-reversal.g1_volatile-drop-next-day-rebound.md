---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g3_daily-move-reversal
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend.g3_daily-move-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 24 hours, a coin rebounds after a 24-hour fall. The rebound is larger the deeper the fall in units of the coin's one-week hourly volatility, and larger still the higher that one-week volatility is relative to its one-month median.
Consequence: A trader would buy a coin after a sharp daily drop during a volatile stretch, sized by the depth of the drop and the level of volatility, and would not short daily surges.
Why:
- F1: The 24-hour reversal works only when recent volatility is high for the coin. Split by the coin's 168-hour volatility relative to its 720-hour median, the reversal slope has t=7.53 in the top fifth (relative volatility 1.81) and t=3.20 in the fourth, but is slightly negative in the three lower fifths (t = -0.88, -0.13, -0.78). A predictor of the negated z-score times relative volatility reaches t=8.23, against t=5.20 for the negated z-score alone (n=15230 non-overlapping 24-hour cases).
- F2: In the high-relative-volatility fifth the reversal holds over time: the slope is positive in all 8 years and has t≥2.1 in 6 of them (2018 3.43, 2019 3.76, 2020 2.39, 2021 4.79, 2023 2.12, 2025 3.21). 2022 (t=1.23) and 2024 (t=0.33) are weaker.
- F3: The reversal is almost entirely a rebound after falls. After a 24-hour fall the slope is 0.0045 with t=4.88 (n=8179). After a rise it is 0.0005 with t=0.61 (n=8491). In the forecast quintiles the strongest long quintile earns +30.2 bp excess over the next 24 hours (t=3.21), while the strongest short quintile earns -11.8 bp (t=-1.45), so the short side adds little.
- F6: Trading costs, not the forecast, sink the book. Mean gain before fees is +0.000066 per coin-day, fees are 0.0028 per coin-day, and turnover is 0.108 of the book per hour (11.1 trades per day). The result is a mean daily book return of -0.00274, against +0.00119 for holding the coin.
