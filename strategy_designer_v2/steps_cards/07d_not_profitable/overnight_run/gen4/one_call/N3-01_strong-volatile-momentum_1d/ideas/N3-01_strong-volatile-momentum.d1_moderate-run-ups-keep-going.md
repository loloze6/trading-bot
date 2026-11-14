---
brief: 002_moving-average-cross-trend-persistence
source-idea: N3-01_strong-volatile-momentum
line: 7.d not profitable
backtest: N3-01_strong-volatile-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin is up over both 20 and 60 days and its 20-day rise is moderate rather than extreme by its own standards, the next 5 days rise more than the coin's average.
Consequence: A trader would size up on moderate run-ups and refuse the extreme ones, which are where the book takes its largest positions and its deepest drawdowns.
Why:
- F5: A larger forecast does not earn more. Mean excess 5-bar return (non-overlapping) is -3.4% in the 5–10 bucket (t=-1.53, n=35) and +0.97% at 10 or more (t=1.38, n=369). Trades entered at forecast 10–15 lose 0.18% gross (n=99).
- F6: Among forecast ≥10 cases, the largest run-ups do not continue. In the top 20-day-return tercile (above +37%), the excess 5-bar return is 0.0% (t=0.00, n=108). In the lowest tercile (+4% to +22%), it is +2.1% (t=1.64, n=107).
- F1: Fees do not explain the failure: the 1118 trades, all long, earn 5.64% each on average before fees and pay 0.10% in fees (t of gross = 3.43). The Calmar failure comes from drawdowns: the deepest book drawdown is -86% on ZECUSD, -71% on both LTCUSD and XRPUSD, and -86% in 2021.
