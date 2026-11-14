---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-01_breakout-drift-lasts
line: 7.f real and profitable
backtest: N4-01_breakout-drift-lasts_1d
instruments: SOL, ADA, DOGE, LINK, BCH, DOT, AVAX
bar: 4h
period: folds A, B, C, D
---
Idea: The same rise after a coin's new 20-day closing high appears in other liquid crypto coins and on 4-hour bars, and not only in the few coins and years that carried this book.
Consequence: A trader would trust the breakout drift only if it holds outside the XRP, ETH, ZEC and 2020/2021/2024 cases that made this result.
Why:
- F1: The book's gain rests on a few days: the best 1% of its 2898 daily returns (mean over coins) carry 104% of the summed daily return, and without them the sum is -0.20 instead of +4.93.
- F2: The confirmed drift rests on a few events: on 445 non-overlapping new-20-day-high events the mean excess 10-bar return is 0.0214 (t 2.49), but without the 10 largest it is 0.0035 (t 0.56, n 435), and the median event is -0.0128.
- F6: The gain is spread unevenly across coins: XRP, ETH and ZEC give 78% of the summed book return (Sharpe 0.82, 0.98, 0.69). LTC gives 3% with Sharpe 0.11, below its holding's 0.26, and BTC and XMR also trail holding (0.47 vs 0.65, 0.34 vs 0.44). No single coin's event excess reaches t 1.6 (n 59 to 82).
