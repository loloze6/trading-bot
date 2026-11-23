---
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g2_high-volatility-hourly-shock-reversal_1h
idea tested: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g2_high-volatility-hourly-shock-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4276 USD
---
## Findings
- **F1:** A coin's 24-hour return, scaled by its 30-day hourly volatility (z24), is followed by a graded reversal over the next 24 hours. On a non-overlapping 24-bar grid, the excess return in the fade direction is -0.06 % (t -1.2, n 7793) for |z24| ≤ 0.5, +0.07 % (t 0.9, n 4287) for 0.5–1, +0.46 % (t 4.7, n 2882) for 1–2, +0.61 % (t 2.2, n 602) for 2–3 and +1.73 % (t 3.1, n 219) above 3, and the pooled slope of the excess 24-hour return on z24 is -0.28 % per unit (t -6.9, n 15806).
- **F2:** This reversal holds on every coin separately, with 24-hour slopes of -0.16 % (BTC, t -2.3), -0.28 % (ETH, t -3.3), -0.25 % (LTC, t -2.4), -0.45 % (XMR, t -4.5), -0.27 % (XRP, t -2.4) and -0.32 % (ZEC, t -2.4), about 2650 cases each. By year the slope is negative in 7 of 8 years and has t ≤ -2.5 in 2018, 2019, 2021 and 2023; 2024 is the exception (+0.05 %, t 0.6).
- **F3:** The reversal belongs to a one-day horizon. At 12 hours the |z24| 1–2 bucket fades +0.19 % (t 3.6). At 48 hours no bucket reaches t 2, and at 72 hours none reaches t 1.5 (e.g. |z24| 1–2: +0.40 %, t 1.4), with no coin's 72-hour slope beyond |t| 1.4.
- **F4:** Among cases with |z24| > 1, the 24-hour fade grows with the ratio of 24-hour to 30-day volatility: +0.04 % (t 0.2, n 562) for a ratio below 0.8, +0.41 % (t 3.1, n 1485) for 0.8–1.2, +0.72 % (t 4.4, n 1334) for 1.2–2 and +1.46 % (t 3.0, n 322) above 2.
- **F5:** The reversal is larger after drops than after rises. With |z24| > 1, a 24-hour drop is followed by a +0.84 % excess rebound over 24 hours (t 5.7, n 1774), against a +0.30 % excess pullback after a rise (t 2.5, n 1929).
- **F6:** The tested 1-hour shock signal is small and not graded at its extremes.
- **F7:** The book's losses come from shorts held long. Short trades average -3.53 % before fees (5182 trades, 38 % winners) against +0.92 % for longs, and shorts held over 168 hours average -18.6 % (n 540). The book loses in 6 of 8 years, including -0.30 % a day in 2020 while the coins rose +0.42 % a day.

## Ideas
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g2_high-volatility-hourly-shock-reversal.g1_one-day-move-reverses-next-day` (from F1, F2, F3, F6): The larger a coin's 24-hour return relative to its 30-day hourly volatility, the more its return over the next 24 hours runs the opposite way.
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g2_high-volatility-hourly-shock-reversal.g2_volatile-day-move-reversal` (from F4, F1): The higher a coin's 24-hour volatility is relative to its 30-day volatility, the more its large 24-hour return, measured against its 30-day volatility, reverses over the next 24 hours.
- `017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g2_high-volatility-hourly-shock-reversal.g3_sharp-daily-drop-rebounds` (from F5, F1, F7): The larger a coin's 24-hour drop relative to its 30-day hourly volatility, the larger its rise over the next 24 hours.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
