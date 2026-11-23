---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g2_high-volatility-hourly-shock-reversal
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g2_high-volatility-hourly-shock-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 24-hour return relative to its 30-day hourly volatility, the more its return over the next 24 hours runs the opposite way.
Consequence: A trader would fade a coin's sharp one-day moves for one day, with a move per case several times the cost of a trade at the large end.
Why:
- F1: A coin's 24-hour return, scaled by its 30-day hourly volatility (z24), is followed by a graded reversal over the next 24 hours. On a non-overlapping 24-bar grid, the excess return in the fade direction is -0.06 % (t -1.2, n 7793) for |z24| ≤ 0.5, +0.07 % (t 0.9, n 4287) for 0.5–1, +0.46 % (t 4.7, n 2882) for 1–2, +0.61 % (t 2.2, n 602) for 2–3 and +1.73 % (t 3.1, n 219) above 3, and the pooled slope of the excess 24-hour return on z24 is -0.28 % per unit (t -6.9, n 15806).
- F2: This reversal holds on every coin separately, with 24-hour slopes of -0.16 % (BTC, t -2.3), -0.28 % (ETH, t -3.3), -0.25 % (LTC, t -2.4), -0.45 % (XMR, t -4.5), -0.27 % (XRP, t -2.4) and -0.32 % (ZEC, t -2.4), about 2650 cases each. By year the slope is negative in 7 of 8 years and has t ≤ -2.5 in 2018, 2019, 2021 and 2023; 2024 is the exception (+0.05 %, t 0.6).
- F3: The reversal belongs to a one-day horizon. At 12 hours the |z24| 1–2 bucket fades +0.19 % (t 3.6). At 48 hours no bucket reaches t 2, and at 72 hours none reaches t 1.5 (e.g. |z24| 1–2: +0.40 %, t 1.4), with no coin's 72-hour slope beyond |t| 1.4.
- F6: The tested 1-hour shock signal is small and not graded at its extremes.
