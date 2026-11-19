---
line: 7.b inconclusive
backtest: 017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend_1h
idea tested: 017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3270 USD
---
## Findings
- **F1:** The tested 1-hour fade from 12:00 UTC is tiny and mixed: the pooled timing gain is 1.86e-05 per case (t 0.42, 17,347 cases), only 3 of 6 coins are positive (BTC t −0.78, ETH −0.15, LTC −0.41 against XMR +1.14, XRP +0.52, ZEC +0.71), the years go both ways (2023 t −1.49, 2025 t +1.27), and the largest position-size quintile loses (−7.0e-05, t −0.48).
- **F2:** The same fade measured over a longer hour count from 12:00 UTC is clear: by the sign of the 3-day return it earns 0.000095 over 1 hour (t 1.08), 0.000588 over 3 hours (t 4.04) and 0.000744 over 4 hours (t 4.25, 16,932 coin-days), then vanishes over 6 hours (t −0.24) and 24 hours (t −1.53), so the test's 1-hour horizon caught only the first part of the move.
- **F3:** The 4-hour fade from 12:00 UTC is broad: positive in all 6 coins (XMR t 4.12, ZEC 1.79, LTC 1.69, ETH 1.22, XRP 0.83, BTC 0.75), in 7 of 8 years (2022 t 3.57, 2025 t 3.40, only 2020 −0.18), and on both sides (after a 3-day fall 0.000716, t 2.69; after a 3-day rise 0.000772, t 3.38).
- **F4:** It is graded mostly on the falling side: the next-4-hour excess return from 12:00 UTC falls from +0.30% in the lowest 3-day-return decile (mean −14%) to +0.08% in the third decile, and sits near −0.04% to −0.11% across the rising deciles, with the top decile (+16%) only −0.03%; the Spearman correlation is −0.048.
- **F5:** The fade is tied to the midday clock and reverses later in the day: the 4-hour sign-fade earns t 3.18, 5.16 and 4.25 when it starts at 10:00, 11:00 and 12:00 UTC, but t −5.16 and −6.72 when it starts at 15:00 and 16:00 UTC (trend continuation), and t −4.1 to −5.0 when it starts at 21:00 to 23:00 UTC.

## Ideas
- `017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend.b1_midday-fade-more-coins` (from F1, F2): The larger a coin's 3-day return, the lower its return over the 1 hour following 12:00 UTC: a stronger 3-day rise is followed by a larger decline in that hour, and a stronger 3-day fall by a larger rebound.
- `017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend.b2_four-hour-midday-trend-fade` (from F2, F3, F4): The larger a coin's 3-day return, the lower its return over the 4 hours following 12:00 UTC: a stronger 3-day rise is followed by a larger decline over those 4 hours, and a stronger 3-day fall by a larger rebound.
- `017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend.b3_afternoon-trend-continuation` (from F5): The larger a coin's 3-day return, the higher its return over the 4 hours following 16:00 UTC: a stronger 3-day rise is followed by a larger further rise over those hours, and a stronger 3-day fall by a larger further fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
