---
line: 7.b inconclusive
backtest: 017-03_postsettle-recovery-after-uptrend_1h
idea tested: 017-03_postsettle-recovery-after-uptrend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3786 USD
---
## Findings
- **F1:** The test's own result points the way the idea predicts but falls short of the bar. On the 25,701 settlement entry cases, the slope t on the forecast is 1.52 and the forecast-weighted mean excess 2-hour return is +3.5 bp. The forecast quintiles rise almost steadily, from +1.4 bp (t 0.79) in the lowest to +5.0 bp (t 2.09) in the highest.
- **F2:** The pooled result mixes one strong settlement with two opposite ones. After the 16:00 UTC settlement (entry bar 15:00), the excess 2-hour return averages +9.7 bp, with slope t 3.60 on the forecast and 4.73 on the raw 3-day rise. After 08:00 it averages -3.7 bp (t_rise -2.66), and after 00:00 the t_rise is -3.91.
- **F3:** The 16:00 recovery is broad, not driven by one slice. Its slope on the 3-day rise is positive in 5 of 6 coins (ZEC t 4.03, BTC 1.59, XMR 1.64; XRP -0.65) and in 6 of 8 years (2025 t 3.82, 2020 2.94; 2022 -0.88, 2024 -1.22). It holds on weekdays (t 3.22, 6,053 cases) and weekends (t 3.91, 2,528 cases).
- **F4:** The grading is not specific to settlement times, which is what the brief says would make the theory wrong. Pooled over all three settlement entry hours, the slope t on the 3-day rise is -1.13 (25,782 cases), against +1.88 over the non-settlement hours (154,715 cases). Several non-settlement hours grade as strongly as 15:00 or more: 20:00 has t 6.15, 05:00 t 4.90, 04:00 t 3.68 and 21:00 t 3.43.
- **F5:** The effect strengthens with a longer horizon than the plan's 2 hours. On the same cases the forecast slope t goes 0.20, 1.52, 1.97 and 2.20 at 1, 2, 4 and 8 hours, and the raw-rise slope t is 2.23 at 8 hours. It runs against the market in one year: in 2022 the slope t is -3.00 on the forecast and the mean is -7.4 bp.
- **F6:** The test used only the 6 default coins. Hourly bars exist for 13 more coins, in folds A and D in full and partly in B and C, so the unchanged idea can be run on more independent cases.

## Ideas
- `017-03_postsettle-recovery-after-uptrend.b1_post-settlement-recovery-more-coins` (from F1, F6): For a coin with a strong 3-day run up, the return over the 2 hours after each funding settlement time (00:00, 08:00 and 16:00 UTC) is positive, and the stronger the 3-day rise, the larger that post-settlement recovery.
- `017-03_postsettle-recovery-after-uptrend.b2_16-00-settlement-recovery-after-rise` (from F2, F3, F4): For a coin with a 3-day rise, the return over the 2 hours after the 16:00 UTC funding settlement is positive, and the larger the coin's 3-day return, the larger that return.
- `017-03_postsettle-recovery-after-uptrend.b3_post-settlement-recovery-8-hours` (from F1, F5): For a coin with a 3-day rise, the return over the next 8 hours from each funding settlement time (00:00, 08:00 and 16:00 UTC) is positive, and the larger the coin's 3-day return, the larger that return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
