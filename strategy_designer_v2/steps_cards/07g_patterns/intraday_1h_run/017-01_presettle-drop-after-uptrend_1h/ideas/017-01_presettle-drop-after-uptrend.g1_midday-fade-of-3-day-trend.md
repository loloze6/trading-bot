---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 3-day return, the lower its return over the 1 hour following 12:00 UTC: a stronger 3-day rise is followed by a larger decline in that hour, and a stronger 3-day fall by a larger rebound.
Consequence: A trader would fade the coin's 3-day trend over the hour starting at 12:00 UTC, with a position sized to the size of that trend, rather than around the funding times.
Why:
- F1: The coin's standardised 3-day return predicts the return of the hour that starts at 12:00 UTC (about 16,974 non-overlapping cases), with a slope of -10.7 bp per standard deviation (t -11.4), the strongest of all 24 hours. The slope is negative in all six coins (BTC -3.3 bp t -2.2, ETH -7.6 t -4.0, LTC -10.9 t -4.5, XMR -18.6 t -8.3, XRP -9.5 t -3.7, ZEC -14.4 t -5.0) and in six of eight years (2021 -25.1 bp t -8.7, 2022 -19.9 t -7.4). This is a clock hour with no funding settlement, which matches the brief's own failure condition.
- F3: The book loses on fees, not on its forecast. Its gross gain is -0.05 bp per bar (t -1.7) against 0.71 bp of fees per bar. Its active pre-settlement bars stamped 21:00 and 22:00 lose -3.1 bp and -1.8 bp, while those stamped 13:00 earn +2.9 bp.
