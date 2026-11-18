---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-02_thin-volume-drop-rebounds
line: 7.g patterns
backtest: 003-02_thin-volume-drop-rebounds_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin rises sharply over one day on volume above its own 30-day average daily volume, it keeps rising over the next 5 days. The larger the rise and the heavier its volume against that average, the larger the continuation.
Consequence: A sharp rise on heavy volume is a reason to join the move for the next 5 days rather than fade it.
Why:
- F2: The strongest up days on the heaviest volume are followed by the largest excess return. The top quintile of one-day return within the top volume tercile averages +2.13% excess over 5 days (t=2.61, n=293). The same quintile on the thinnest volume averages +0.47% (t=0.47, n=99). This is one cell out of about fifty that were examined, so on its own it is only marginal.
- F3: Up days in the top half of standardised size and the top quartile of volume ratio do not hold up as a stable group. They show positive excess in five of six coins (+0.3% to +3.5%; LTC is −0.95%) but no single coin reaches t>1.2. They are positive in both halves of the windows (+0.83% with t=0.88, then +1.66% with t=1.39). The z×volume interaction in OLS has t=1.00.
- F1: Across all six coins, a day's volume against its prior 30-day mean volume ranks positively with the coin's excess return over the next 5 days. On the non-overlapping 5-day grid the Spearman correlation is 0.0595 (p=0.0015, n=2843 independent cases). This holds on both sides of the day's move: on up days the volume ratio's Spearman is 0.061 (p=0.024, n=1365), and on down days it is 0.0565 (p=0.030, n=1476). On down days the OLS coefficient on the log volume ratio is 0.0110 (t=2.04).
