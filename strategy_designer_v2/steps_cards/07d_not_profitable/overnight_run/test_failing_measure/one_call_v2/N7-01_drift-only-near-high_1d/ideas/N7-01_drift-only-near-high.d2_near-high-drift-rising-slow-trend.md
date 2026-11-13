---
brief: 002_moving-average-cross-trend-persistence
source-idea: N7-01_drift-only-near-high
line: 7.d not profitable
backtest: N7-01_drift-only-near-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a new 20-day closing high, while the close stays near that high and above its 20-day average, the coin rises more than its average over the following days, only while its 50-day average has been rising over the last ten bars.
Consequence: Stand aside from fresh highs that occur inside a falling longer trend, since in the early windows those days lost and produced the long fall.
Why:
- F1: The Calmar failure comes from one fall: the book's deepest drawdown is -67.5%, running 1,160 days from w1 to its trough in w10. Over those 1,162 days the book's mean daily return was -0.00075, against +0.00297 over the remaining 1,736 days. No other fall is deeper than -43.7% (w11 to w13).
- F2: In w1–w10, active coin-days whose 50-day average had fallen over the prior 10 bars lost on average (-0.0013 per day, 503 days, sum -0.65). Active days with a rising 50-day average earned +0.0022 (1,125 days). In w11–w24, both groups earned (+0.0075 on 675 days, +0.0086 on 1,357 days), so the falling-trend days are what carried the early fall.
- F4: Requiring a rising 50-day average instead cuts the deepest fall further, to -34.4% (or -28.5% with a 10-bar rise above 1.45%), and Calmar reaches 0.78 or 0.85. It costs about half the mean daily return (0.0007–0.0008) and some Sharpe (0.85–0.87).
