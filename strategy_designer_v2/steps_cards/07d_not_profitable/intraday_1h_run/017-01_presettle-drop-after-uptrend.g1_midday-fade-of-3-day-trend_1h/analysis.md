---
line: 7.d not profitable
backtest: 017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend_1h
idea tested: 017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3176 USD
---
## Findings
- **F1:** Fees, not the forecast, sink the book: gross gain summed over all coins and windows is +0.29 against fees of 17.67 (in book-value fractions), or 0.19 bp gross against 11.6 bp of fee per active hour, and the fees alone match the -0.001 mean daily return (about 2.95 per coin over about 2,900 days).
- **F2:** The engine charges about 10.7 bp per unit of allocation changed over 30,015 trades, so a round trip at the mean |allocation| of 0.54 costs about 11.6 bp, while the tested 1-hour fade from the 12:00 UTC close earns only 0.94 bp (t = 1.07, n = 16,932 coin-days).
- **F3:** The fade of the 3-day trend from the 12:00 UTC close builds over the following hours: 3.7 bp over 2 h (t = 3.09), 5.8 bp over 3 h (t = 4.01) and 7.4 bp over 4 h (t = 4.23, n = 16,932). It is gone by 6 h (-0.6 bp) and reversed by 12 h (-6.1 bp, t = -2.17).
- **F4:** The 4-hour fade is graded by the 3-day return scaled by its own 3-day volatility: -1.4 bp in the weakest |z| quintile (t = -0.40) against 18.4 bp in the strongest (t = 3.73, n = 3,387).
- **F5:** The 4-hour fade is positive in all 6 coins (2.2 bp BTC to 16.8 bp XMR) and in 7 of 8 years (2020 at -1.2 bp; 2022 and 2025 at about 15 bp), so it does not rest on one period.
- **F6:** By the bar's clock hour, the fade is positive on the bars starting 12:00 and 13:00 UTC (3.3 bp, t = 3.47, and 3.6 bp, t = 3.75), then flips to trend continuation on the bars starting 15:00 and 16:00 UTC (-5.0 bp, t = -5.36, and -3.8 bp, t = -4.69). The midday reversal is a short window that the US-afternoon hours undo.

## Ideas
- `017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend.d1_midday-three-hour-trend-fade` (from F1, F2, F3, F4, F5, F6): The larger a coin's 3-day return relative to its 3-day volatility, the lower its return over the 3 hours following 12:00 UTC: a stronger volatility-scaled 3-day rise is followed by a larger decline over those 3 hours, and a stronger volatility-scaled 3-day fall by a larger rebound.
- `017-01_presettle-drop-after-uptrend.g1_midday-fade-of-3-day-trend.d2_scaled-trend-midday-four-hour-reversal` (from F3, F4, F5): The larger a coin's 3-day return relative to its 3-day volatility, the more its return over the 4 hours following 12:00 UTC runs against that 3-day return, so a strong 3-day rise is followed by a larger decline and a strong 3-day fall by a larger rebound over those 4 hours.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
