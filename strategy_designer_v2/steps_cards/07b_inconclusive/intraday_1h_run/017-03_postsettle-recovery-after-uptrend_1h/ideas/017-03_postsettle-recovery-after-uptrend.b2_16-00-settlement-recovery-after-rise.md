---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-03_postsettle-recovery-after-uptrend
line: 7.b inconclusive
backtest: 017-03_postsettle-recovery-after-uptrend_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: For a coin with a 3-day rise, the return over the 2 hours after the 16:00 UTC funding settlement is positive, and the larger the coin's 3-day return, the larger that return.
Consequence: If confirmed, a trader would go long a rising coin at the 16:00 UTC settlement and hold for 2 hours, and would not do so after the 00:00 and 08:00 settlements.
Why:
- F2: The pooled result mixes one strong settlement with two opposite ones. After the 16:00 UTC settlement (entry bar 15:00), the excess 2-hour return averages +9.7 bp, with slope t 3.60 on the forecast and 4.73 on the raw 3-day rise. After 08:00 it averages -3.7 bp (t_rise -2.66), and after 00:00 the t_rise is -3.91.
- F3: The 16:00 recovery is broad, not driven by one slice. Its slope on the 3-day rise is positive in 5 of 6 coins (ZEC t 4.03, BTC 1.59, XMR 1.64; XRP -0.65) and in 6 of 8 years (2025 t 3.82, 2020 2.94; 2022 -0.88, 2024 -1.22). It holds on weekdays (t 3.22, 6,053 cases) and weekends (t 3.91, 2,528 cases).
- F4: The grading is not specific to settlement times, which is what the brief says would make the theory wrong. Pooled over all three settlement entry hours, the slope t on the 3-day rise is -1.13 (25,782 cases), against +1.88 over the non-settlement hours (154,715 cases). Several non-settlement hours grade as strongly as 15:00 or more: 20:00 has t 6.15, 05:00 t 4.90, 04:00 t 3.68 and 21:00 t 3.43.
