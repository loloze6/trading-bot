---
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g1_weekend-post-settlement-shock-reversal_1h
idea tested: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g1_weekend-post-settlement-shock-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4103 USD
---
## Findings
- **F1:** On Saturday and Sunday, the 12-hour move to the close of the 20:00 UTC bar, scaled by 24-hour volatility, is followed by a 24-hour excess return the opposite way: the slope is 43.8 bp per unit with t 6.04 over 4854 non-overlapping cases. On weekdays at the same hour the slope is −9.7 bp (t −2.24, 12259 cases).
- **F2:** That weekend 12-hour fade holds on every coin, with slopes from +24 bp (BTC, t 1.81) to +56 bp (XMR, t 3.43; LTC t 3.07, XRP 2.40, ZEC 2.33, ETH 1.88). It holds on both weekend days: Saturday +59 bp (t 6.18), Sunday +31 bp (t 2.87). Monday to Friday are all between −17 and 0 bp, with |t| ≤ 1.8.
- **F3:** By year, the weekend 12-hour fade is positive in 7 of 8 years (2019 t 5.1, 2022 t 4.8, 2024 t 3.8), but it reverses in 2025 (−39 bp, t −2.03).
- **F4:** The same fade at other weekend anchor hours is weaker but has the same sign. At 16:00 the 12-hour fade gives +29.6 bp (t 4.07) and the 4-hour fade +21.4 bp (t 3.25). At 04:00 the 12-hour fade gives +35.5 bp (t 4.69). At the same anchors on weekdays, every slope is between −14.5 and +0.5 bp.
- **F5:** The tested 1-hour fade is not special to the 00:00 hour on weekends. Weekend 1-hour moves are followed by a 24-hour reversal at 18 of 24 hours of the day (12:00 +20.5 bp, t 3.15; 18:00 +23.8 bp, t 3.32; 20:00 +26.1 bp, t 3.85). On weekdays only 11 of 24 hours are positive, and several are negative with t below −2.5 (03:00, 06:00, 07:00).
- **F6:** The weekend fade is larger when 24-hour volatility is high against its 30-day level: +23.1 bp (t 6.3) in the top third against +5.3 bp (t 3.2) in the bottom third. On weekdays the same split runs from +7.4 bp (t 4.2) to −10.8 bp (t −6.4). These counts use overlapping returns, so the t values are inflated.
- **F7:** The book earned +7.8 bp a day in 2018 and +8.8 bp in 2025. It lost in 2023 (−0.6 bp) and 2024 (−1.6 bp), which explains a Calmar of 0.449. XMR, the coin with the strongest reversal signal, earned the book only 0.2 bp a day (Sharpe 0.04).

## Ideas
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g1_weekend-post-settlement-shock-reversal.g1_weekend-evening-12-hour-fade` (from F1, F2, F3): On a Saturday or Sunday, the larger a coin's 12-hour return up to 21:00 UTC, relative to its 24-hour volatility, the more its return over the next 24 hours runs the opposite way.
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g1_weekend-post-settlement-shock-reversal.g2_weekend-multi-hour-move-reversal` (from F4, F5): On a Saturday or Sunday, the larger a coin's 4-hour to 12-hour return at any hour of the day, relative to its 24-hour volatility, the more its return over the next 24 hours reverses it.
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g1_weekend-post-settlement-shock-reversal.g3_volatile-weekend-hourly-shock-fade` (from F5, F6): On a Saturday or Sunday, the larger a coin's 1-hour return relative to its 24-hour volatility, the more its next 24 hours run the opposite way, and the reversal is larger the higher the coin's 24-hour volatility stands against its 30-day volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
