---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 14-day return, the higher its return over the next 7 days, and the more so the higher its 30-day return, with the largest rises following strong two-week gains inside a rising month.
Consequence: A trader would lean long the coins with the strongest two-week rise and lean harder when the month is also up, rather than shorting the coins that fell, whose next week still drifts up.
Why:
- F1: Over its 8,559 long bars the book earned a gross sum of 15.82 for 1.55 in fees, while its 8,762 short bars lost a gross 4.21 and still paid 1.52 in fees, so the short half is a net loss of about 5.7 against the long half's net 14.3.
- F2: Shorts lose in absolute terms because the coins drift up: on short bars the coin's next-day return averaged -0.000134 against +0.002529 on long bars, and in the negative-forecast non-overlapping 7-day samples the raw forward return was near zero (+0.0034 with no 30-day history, +0.0013 when the 30-day return was positive, only -0.0033 when it was negative, 1,253 cases), even though their return net of the coin's mean was -0.0095 (t -2.69).
- F3: The long side's gain sits where the coin is already rising: long bars with a positive 30-day return earned a mean 0.002295 a bar (sum 10.99 of the 15.82), against 0.000802 with a negative 30-day return; positive-forecast samples returned 0.027 over 7 days when the 30-day return was positive (excess 0.018, 629 cases) and only 0.0107 when it was negative (excess 0.0014, 223 cases).
- F4: The forecast's top fifth (mean +17.2) was followed by a 7-day return of 0.0277 and the bottom fifth (mean -14.6) by +0.0043, so even the strongest negative forecasts came before a rise and gave no edge to a short.
- F5: Dropping the shorts in a rough rebuild of the daily book (daily mean over coins of gain minus fee) lifts the mean daily return from 0.00049 to 0.00082, the Sharpe from 0.48 to 1.08, the deepest fall from -52% to -31% and the Calmar from 0.22 to 0.96.
