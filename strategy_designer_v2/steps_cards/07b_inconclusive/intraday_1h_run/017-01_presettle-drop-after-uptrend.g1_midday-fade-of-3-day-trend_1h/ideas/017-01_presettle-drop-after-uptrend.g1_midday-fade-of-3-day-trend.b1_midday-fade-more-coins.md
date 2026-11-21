---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend
line: 7.b inconclusive
backtest: 017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 3-day return, the lower its return over the 1 hour following 12:00 UTC: a stronger 3-day rise is followed by a larger decline in that hour, and a stronger 3-day fall by a larger rebound.
Consequence: A trader would fade the coin's 3-day trend over the hour starting at 12:00 UTC, with a position sized to the size of that trend, rather than around the funding times.
Why:
- F1: The tested 1-hour fade from 12:00 UTC is tiny and mixed: the pooled timing gain is 1.86e-05 per case (t 0.42, 17,347 cases), only 3 of 6 coins are positive (BTC t −0.78, ETH −0.15, LTC −0.41 against XMR +1.14, XRP +0.52, ZEC +0.71), the years go both ways (2023 t −1.49, 2025 t +1.27), and the largest position-size quintile loses (−7.0e-05, t −0.48).
- F2: The same fade measured over a longer hour count from 12:00 UTC is clear: by the sign of the 3-day return it earns 0.000095 over 1 hour (t 1.08), 0.000588 over 3 hours (t 4.04) and 0.000744 over 4 hours (t 4.25, 16,932 coin-days), then vanishes over 6 hours (t −0.24) and 24 hours (t −1.53), so the test's 1-hour horizon caught only the first part of the move.
