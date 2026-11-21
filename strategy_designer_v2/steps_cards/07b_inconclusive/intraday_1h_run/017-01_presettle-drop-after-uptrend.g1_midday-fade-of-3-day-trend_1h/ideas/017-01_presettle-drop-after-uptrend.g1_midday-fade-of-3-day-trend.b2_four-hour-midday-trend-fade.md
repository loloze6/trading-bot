---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend
line: 7.b inconclusive
backtest: 017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 3-day return, the lower its return over the 4 hours following 12:00 UTC: a stronger 3-day rise is followed by a larger decline over those 4 hours, and a stronger 3-day fall by a larger rebound.
Consequence: A trader would fade the coin's 3-day trend from 12:00 to 16:00 UTC, sized to the trend, rather than over the single hour after 12:00.
Why:
- F2: The same fade measured over a longer hour count from 12:00 UTC is clear: by the sign of the 3-day return it earns 0.000095 over 1 hour (t 1.08), 0.000588 over 3 hours (t 4.04) and 0.000744 over 4 hours (t 4.25, 16,932 coin-days), then vanishes over 6 hours (t −0.24) and 24 hours (t −1.53), so the test's 1-hour horizon caught only the first part of the move.
- F3: The 4-hour fade from 12:00 UTC is broad: positive in all 6 coins (XMR t 4.12, ZEC 1.79, LTC 1.69, ETH 1.22, XRP 0.83, BTC 0.75), in 7 of 8 years (2022 t 3.57, 2025 t 3.40, only 2020 −0.18), and on both sides (after a 3-day fall 0.000716, t 2.69; after a 3-day rise 0.000772, t 3.38).
- F4: It is graded mostly on the falling side: the next-4-hour excess return from 12:00 UTC falls from +0.30% in the lowest 3-day-return decile (mean −14%) to +0.08% in the third decile, and sits near −0.04% to −0.11% across the rising deciles, with the top decile (+16%) only −0.03%; the Spearman correlation is −0.048.
