---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d1_ninety-day-breakout-twenty-day-continuation
line: 7.b inconclusive
backtest: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d1_ninety-day-breakout-twenty-day-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's daily close stands above its highest close of the previous 90 days, the more it rises over the next 10 days.
Consequence: A trader who sees a close beyond the 90-day high should expect the continuation within about ten days, and should not count on it lasting three weeks.
Why:
- F1: The test measured the idea almost nowhere. The forecast is positive for a median of 1 day (mean 1.9 days) after a close beyond the 90-day high, so the 20-day grid fell on only 41 positive-forecast bars. Those 41 give a drift-adjusted mean of −3.5 % (t −0.98) and the plan's measure t −0.14. The same data hold 184 first closes beyond the high that lie at least 20 days apart.
- F2: On those 184 separate breakout closes, the coin's drift-adjusted rise is clearest over the first 10 days. It is +2.4 % over 5 days (t 2.52, n 184) and +4.2 % over 10 days (t 2.43, n 182, strength 0.169, t 2.55). The rise fades from there: +3.8 % over 20 days (t 1.49, n 169) and +5.5 % over 40 days (t 1.31, n 136). The plan's 20-day horizon is past the point where the move shows.
- F3: The move is carried by a few large cases. Median drift-adjusted returns are +0.3 % over 10 days and −1.0 % over 20 days, against means of +4.2 % and +3.8 %. By coin over 10 days, XRP shows +18.8 % on 19 cases but a median of only +0.4 %, and LTC shows −1.1 % (t −0.46).
- F4: Grading by the distance beyond the high is weak. Over 10 days, the lowest, middle and highest terciles of the forecast give +3.1 %, +4.7 % and +4.6 % (about 56 cases each). The Spearman correlation with the 10-day move is 0.04, and with the 20-day move it is −0.11. Only the 5-day move separates by forecast: +1.0 %, +0.8 % and +5.4 %.
- F5: The effect varies by period but is positive in most years over 10 days. Seven of eight years are positive, from +1.7 % to +7.9 %, and 2023 is −1.1 % (t −0.77, 29 cases). Over 20 days on all breakout closes, 2021 (−8.6 %, t −3.02) and 2023 (−3.3 %, t −2.93) turn clearly negative.
- F6: The size is not what limits the book. The plan's 152 cases give a total move of +7.47 % per case against a trade cost of 0.19 % (38.7 times the cost). The book still has a Sharpe of 0.64 and a Calmar of 0.50.
