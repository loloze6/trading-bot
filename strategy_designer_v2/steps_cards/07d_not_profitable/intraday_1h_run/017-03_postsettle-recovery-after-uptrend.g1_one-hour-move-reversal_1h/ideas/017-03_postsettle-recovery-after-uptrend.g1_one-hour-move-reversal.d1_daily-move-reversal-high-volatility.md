---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-03_postsettle-recovery-after-uptrend.g1_one-hour-move-reversal
line: 7.d not profitable
backtest: 017-03_postsettle-recovery-after-uptrend.g1_one-hour-move-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's return over the next 24 hours runs against its own last 24-hour return, and the larger that move relative to the coin's recent daily volatility, the larger the reversal, only while the coin's 30-day volatility is high, the reversal growing with that volatility.
Consequence: Fade sharp one-day moves in volatile periods, rebalancing about once a day instead of every hour, so that one fee is set against a reversal of tens of basis points rather than a few.
Why:
- F1: The fade has a real edge before costs but fees eat it about eight times over: per bar the book earned 0.81 bp gross and paid 6.56 bp in fees, for −5.75 bp net; that is 0.013 % gross against 0.107 % in fees per unit of turnover, from a turnover of 0.61 of the book per hour. The result is a mean daily book return of −1.36 % over 17,381 coin-days and the failed Sharpe of −16.35.
- F3: The reversal is too small at 1 hour to pay for an hourly trade. On non-overlapping grids, fading the top quintile of 1-hour moves (sized by 720-bar vol) earns only 4.4 bp (t 8.4, n 77,569). The same fade earns 10.3 bp over 4 hours (t 5.4, n 19,378) and 50.1 bp over 24 hours (t 4.8, n 3,190). So the gain per position grows roughly with the horizon while one trade's fee stays fixed.
- F4: The reversal sits almost entirely in high-volatility periods, and most clearly at the slower horizons. Fading the two largest move quintiles in above-median 720-bar vol earns 75.6 bp over 24 hours (t 6.2, n 3,122) against 4.4 bp (t 0.6) in low vol. Over 4 hours it is 14.9 bp (t 7.0) against 0.7 bp (t 0.6), and over 1 hour 5.5 bp (t 9.6) against 1.2 bp.
- F5: The edge does not extend to every horizon. The fade is flat at 12 hours (top quintile −6.2 bp, t −1.2) and loses at 72 hours (top quintile −89 bp, t −3.0). The usable reversal is the 1-day move undone over the next day, not a longer drift.
