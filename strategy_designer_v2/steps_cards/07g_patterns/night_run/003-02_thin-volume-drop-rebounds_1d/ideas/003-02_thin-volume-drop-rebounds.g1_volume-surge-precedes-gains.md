---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-02_thin-volume-drop-rebounds
line: 7.g patterns
backtest: 003-02_thin-volume-drop-rebounds_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin trades more volume today than its own 30-day average daily volume, its price rises more than usual over the next 5 days, more so the larger that volume ratio. This holds whether the day closed up or down.
Consequence: A volume surge against the coin's own recent average is a reason to lean long for the following 5 days, and a thin-volume day is a reason to refuse a long.
Why:
- F1: Across all six coins, a day's volume against its prior 30-day mean volume ranks positively with the coin's excess return over the next 5 days. On the non-overlapping 5-day grid the Spearman correlation is 0.0595 (p=0.0015, n=2843 independent cases). This holds on both sides of the day's move: on up days the volume ratio's Spearman is 0.061 (p=0.024, n=1365), and on down days it is 0.0565 (p=0.030, n=1476). On down days the OLS coefficient on the log volume ratio is 0.0110 (t=2.04).
- F4: The tested situation goes the other way. Moderate falls (second return quintile) on the thinnest volume tercile are followed by −1.37% excess over 5 days (t=−2.00, n=221) rather than a rebound. The idea's active cases are strongly negative in 2018 (t=−2.74) and 2019 (t=−5.02), positive in 2020 (t=3.10), and flat afterwards, so their result depends on the year.
