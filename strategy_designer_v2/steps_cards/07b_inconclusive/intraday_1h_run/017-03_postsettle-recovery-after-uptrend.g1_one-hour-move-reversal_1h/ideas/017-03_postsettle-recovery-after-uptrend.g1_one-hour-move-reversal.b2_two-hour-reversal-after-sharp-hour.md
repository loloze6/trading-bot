---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-03_postsettle-recovery-after-uptrend.g1_one-hour-move-reversal
line: 7.b inconclusive
backtest: 017-03_postsettle-recovery-after-uptrend.g1_one-hour-move-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's return over the next 2 hours runs against its own last-hour return, and the larger that move is relative to the coin's recent hourly volatility, the larger the reversal.
Consequence: A trader fading sharp single-hour moves should hold the fade for about two hours rather than one, which captures twice the reversal per trade and halves turnover.
Why:
- F1: The fade is real and clearly graded by the size of the last-hour move. The pooled excess gain is 8.15e-05 per bar (t 10.23, 416,645 bars). It rises with the size of the forecast, from 0.1e-05 (t 0.74) at |forecast| ≤ 2 to 18.1e-05 (t 5.91) at |forecast| above 15. The raw fade, the next-hour return against the sign of the last hour, grows from −2.7e-05 (t −0.78) in the smallest |z| quintile to 33.1e-05 (t 7.58) in the largest.
- F5: The reversal keeps building after the first hour. On non-overlapping samples the sign-fade averages 1.77e-04 at 1 hour (t 10.77, n 416,501), 3.65e-04 at 2 hours (t 11.30, n 208,134), 3.77e-04 at 4 hours (t 5.97, n 103,944) and 4.46e-04 at 8 hours (t 3.58, n 51,843). Most of it arrives within 2 hours.
- F6: The book loses because of turnover, not because the signal is wrong. The implied fee is 6.56e-04 per bar against a gross excess of 0.81e-04, a net of −5.75e-04 per bar. Mean turnover is 0.61 of the book per bar, giving a Sharpe of −16.35.
