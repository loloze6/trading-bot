---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-02_presettle-rise-after-downtrend.g3_daily-move-reversal
line: 7.g patterns
backtest: 017-02_presettle-rise-after-downtrend.g3_daily-move-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 24 hours, a coin moves against its 24-hour return. The size of the reversal grows with that return measured in one-week volatility units multiplied by the ratio of the coin's one-week hourly volatility to its one-month median.
Consequence: A trader would fade daily moves only in proportion to how unusually volatile the coin currently is, and leave calm-period moves alone.
Why:
- F1: The 24-hour reversal works only when recent volatility is high for the coin. Split by the coin's 168-hour volatility relative to its 720-hour median, the reversal slope has t=7.53 in the top fifth (relative volatility 1.81) and t=3.20 in the fourth, but is slightly negative in the three lower fifths (t = -0.88, -0.13, -0.78). A predictor of the negated z-score times relative volatility reaches t=8.23, against t=5.20 for the negated z-score alone (n=15230 non-overlapping 24-hour cases).
- F2: In the high-relative-volatility fifth the reversal holds over time: the slope is positive in all 8 years and has t≥2.1 in 6 of them (2018 3.43, 2019 3.76, 2020 2.39, 2021 4.79, 2023 2.12, 2025 3.21). 2022 (t=1.23) and 2024 (t=0.33) are weaker.
