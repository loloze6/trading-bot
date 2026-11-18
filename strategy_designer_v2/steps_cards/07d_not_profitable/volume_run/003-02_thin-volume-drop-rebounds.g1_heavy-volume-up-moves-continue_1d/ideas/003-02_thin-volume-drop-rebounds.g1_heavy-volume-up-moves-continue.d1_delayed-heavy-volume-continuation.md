---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue
line: 7.d not profitable
backtest: 003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin rises sharply over one day relative to its own 20-day volatility, it keeps rising over the next 5 days, and the larger the volatility-scaled rise and the heavier its volume against the coin's 30-day average, the larger the further gain, with that further gain coming from the second to the sixth day after the rise rather than the first day.
Consequence: A large up day on heavy volume is a reason to hold the coin through the following week, not only for the next day, so that the position is in place when the continuation actually arrives.
Why:
- F1: The book holds its full position only on the day after the rise, when the coin earns nothing extra; the continuation comes on the following days, when the book has mostly left. After bars with forecast ≥ 10 (n≈1,600), the coin's excess over its mean is 0.00077 on day 1 (t 0.56) at a mean position of 1.02. It is 0.0053 on day 2 (t 4.0), 0.0045 on day 4 (t 3.3) and 0.0036 on day 6 (t 2.7), while the mean position is only 0.15–0.23.
- F2: Because the forecast follows each bar, the book trades in and out around one-day holds, and fees eat the gain. There are 2,988 trades with a median length of 1 day and a mean of 3.3 days. Fees cost 0.00016–0.00023 of the book per bar, against a timing gain of −0.00034 to +0.00051 per coin. The book's mean daily return is 4.9e-05 and its Sharpe is 0.10, while holding gives Sharpe 0.26–0.65 per coin.
- F5: What edge there is sits in the strongest readings, and it grows with the horizon. The forecast bucket 10–20 carries 91% of the summed position gain. Its excess over the coin's mean rises from 0.0008 at 1 day to 0.0130 at 5 days and 0.0230 at 10 days.
