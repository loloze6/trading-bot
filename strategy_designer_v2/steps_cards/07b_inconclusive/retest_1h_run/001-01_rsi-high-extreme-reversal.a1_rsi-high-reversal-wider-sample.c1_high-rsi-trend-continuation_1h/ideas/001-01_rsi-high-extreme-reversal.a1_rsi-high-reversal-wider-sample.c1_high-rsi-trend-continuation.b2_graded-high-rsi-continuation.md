---
brief: 001_rsi-extremes-predict-next-move
source-idea: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation
line: 7.b inconclusive
backtest: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The higher a coin's 14-day RSI stands above 50, the more its price rises above its usual move over the next 10 days, and the larger that excess rise is the further RSI stands above 50.
Consequence: Treat a high 14-day RSI as a graded reason to hold or add to a long for about ten days, and refuse RSI-based shorts against it.
Why:
- F1: The main measure is clearly on the side the idea predicts: the pooled slope of the 240-bar excess return on the forecast is 0.00280 with t 4.74 over 1,674 grid cases. The same positive slope holds at 24, 120, 480 and 720 bars (t 2.54, 3.72, 3.96 and 4.22), so the horizon is not the issue.
- F2: The effect is graded. Among the 821 positive-forecast cases, the mean 240-bar excess return rises steadily across forecast quartiles, from -0.0101 to 0.0026, 0.0131 and 0.0391 (about 205 cases each). The positive-only slope is 0.0036 (t 3.59).
- F5: The book's loss comes from trading costs, not from the signal. Gross daily return is 0.00077 (t 3.10), of which 0.00035 is the market's own rise. Fees are 0.00218 a day on a daily turnover of 1.99, which turns the book to a mean of -0.00144 a day (Sharpe -2.07).
