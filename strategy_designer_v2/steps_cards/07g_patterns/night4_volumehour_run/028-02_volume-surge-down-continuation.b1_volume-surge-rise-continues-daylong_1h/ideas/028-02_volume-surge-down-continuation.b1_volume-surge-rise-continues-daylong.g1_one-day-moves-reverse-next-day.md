---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong
line: 7.g patterns
backtest: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: A coin that has risen over its last 24 hours, measured against its usual 24-hour move, tends to fall over the next 24 hours, and one that has fallen tends to rise. The larger the 24-hour move relative to usual, the larger the opposite move that follows.
Consequence: A trader would lean against a coin's unusually large one-day move for the following day, and refuse to chase it.
Why:
- F1: The coin's z-scored 24-hour return predicts the opposite move over the next 24 hours, on non-overlapping 24-hour cases: the slope is -16.3 bp per unit of z for BTC (t -2.47, Spearman -0.081, 2656 cases) and -29.0 bp per unit for ETH (t -3.41, Spearman -0.076, 2656 cases). Days in the bottom quintile of past return gained +32 bp unusual for BTC (t 1.83) and +52 bp for ETH (t 2.07). At 72 hours the slope is gone (t -0.13 and 0.06).
- F2: The reversal of F1 holds in most years. The slope is negative for both coins in 2018, 2019, 2020, 2021 and 2025 (-13 to -79 bp per unit, t down to -2.35). It is flat or slightly positive in 2022 and 2024, and mixed in 2023. It is a regime-dependent effect, not one that holds every year.
- F5: The brief's volume continuation does not appear at the 2 to 6 hour horizons.
