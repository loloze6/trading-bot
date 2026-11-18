---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue
line: 7.g patterns
backtest: 003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin falls sharply over one day relative to its 20-day volatility on heavy volume against its 30-day average, it rebounds over the next 3 days, and the heavier that day's volume against its average, the larger the rebound.
Consequence: A sharp drop on heavy volume is a reason to buy the coin for the following few days rather than sell it.
Why:
- F1: After a sharp one-day drop (scaled return below -1 against the 20-day volatility), the next 3 days' excess return rises with the day's volume against its 30-day average. On non-overlapping 3-day samples, the quartiles of volume ratio give -0.95% (t -1.18), -0.53% (t -0.74), -0.21% (t -0.32) and +4.09% (t 3.90, n=133); the Spearman correlation of volume ratio with the 3-day return is 0.14. The brief predicts the opposite: heavy-volume drops should carry on.
- F2: The heavy-volume drop rebound starts the very next day. After drops below -1, the next-day excess return is +0.71% (t 3.90, n=1020) in the heavy-volume tercile against +0.01% (t 0.03, n=148) in the thin tercile. For drops on volume above average, the 3-day rebound is positive in 7 of 8 years (all but 2018). It is positive in LTC, XMR, XRP and ZEC (+2.1% to +3.1%, t 1.6 to 2.1) but near zero in BTC and ETH.
