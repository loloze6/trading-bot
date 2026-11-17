---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 14-day return while its 30-day return is positive, the larger its 7-day return over the next 7 days, measured above the coin's usual 7-day return.
Consequence: A trader would size up longs on coins whose two-week and one-month moves are both up, and size them down where the month is falling, since momentum there adds almost nothing above the coin's drift.
Why:
- F3: The long side's gain sits where the coin is already rising: long bars with a positive 30-day return earned a mean 0.002295 a bar (sum 10.99 of the 15.82), against 0.000802 with a negative 30-day return; positive-forecast samples returned 0.027 over 7 days when the 30-day return was positive (excess 0.018, 629 cases) and only 0.0107 when it was negative (excess 0.0014, 223 cases).
- F4: The forecast's top fifth (mean +17.2) was followed by a 7-day return of 0.0277 and the bottom fifth (mean -14.6) by +0.0043, so even the strongest negative forecasts came before a rise and gave no edge to a short.
- F6: The book's deepest fall, -52%, ran 1,001 days from w2 to w10 while holding the coins lost 23% over the same span, so the book fell further than the market. Its daily returns had a correlation of -0.016 with holding's, its mean daily return was 0.000498 against holding's 0.00118, and its Sharpe was 0.49 against 0.55. Together with F1 and F2, this points to a book that kept shorting through the coins' rebounds.
