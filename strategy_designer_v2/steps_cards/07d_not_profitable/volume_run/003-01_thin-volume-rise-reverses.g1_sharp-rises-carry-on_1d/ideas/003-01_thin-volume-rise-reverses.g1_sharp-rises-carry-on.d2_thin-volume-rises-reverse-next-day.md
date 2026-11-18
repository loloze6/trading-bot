---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-01_thin-volume-rise-reverses.g1_sharp-rises-carry-on
line: 7.d not profitable
backtest: 003-01_thin-volume-rise-reverses.g1_sharp-rises-carry-on_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin rises over one day by more than its usual daily move (its 20-day volatility) on volume lighter than its 20-day average volume, it falls over the next day. The lighter that day's volume against its average, the larger the fall.
Consequence: A sharp up day on thin volume is a reason to fade it for one day rather than follow it.
Why:
- F1: The book loses on the day right after the rise. Across all 8848 active bars, the coin's next-day return minus its own mean is -0.154% (t -3.01). This holds at every forecast size, from -0.18% in the 0-2 bucket to -0.36% in the 15-20 bucket. Yet the book's position is largest on exactly that day, rising from 0.02 to 0.90 as the forecast grows.
- F3: Volume separates the two parts of the move. After rises in the top volume tercile (volume against its prior 20-day average), the next day is flat (-0.02% excess, t -0.20) and days 2 to 5 carry on (+0.54% excess, t 2.72, n 2713). After rises in the bottom tercile, the next day reverses (-0.22%, t -2.58) and days 2 to 5 also lose (-0.14%, t -0.75).
