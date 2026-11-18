---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-01_thin-volume-rise-reverses.g1_sharp-rises-carry-on
line: 7.d not profitable
backtest: 003-01_thin-volume-rise-reverses.g1_sharp-rises-carry-on_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin rises over one day by more than its usual daily move (its 20-day volatility), it gives part back on the next day and then keeps rising over the following 4 days. The larger the rise in units of that volatility and the heavier that day's volume against its 20-day average volume, the larger this further rise from the second to the fifth day.
Consequence: Lean long on a sharp up day only after its first day has passed, with conviction growing with both the size of the rise and its volume, instead of buying at the close of the up day itself.
Why:
- F1: The book loses on the day right after the rise. Across all 8848 active bars, the coin's next-day return minus its own mean is -0.154% (t -3.01). This holds at every forecast size, from -0.18% in the 0-2 bucket to -0.36% in the 15-20 bucket. Yet the book's position is largest on exactly that day, rising from 0.02 to 0.90 as the forecast grows.
- F2: The carry the verdict found arrives only on days 2 to 5 after the rise. In the 15-20 bucket the mean coin return is +0.30% on day 3 and +0.34% on day 4, after -0.36% excess on day 1. The 5-day return of the 6-10 and above buckets (+0.44% to +0.51%) sits only about at the coins' unconditional 5-day mean (+0.43% in the 0 bucket).
- F3: Volume separates the two parts of the move. After rises in the top volume tercile (volume against its prior 20-day average), the next day is flat (-0.02% excess, t -0.20) and days 2 to 5 carry on (+0.54% excess, t 2.72, n 2713). After rises in the bottom tercile, the next day reverses (-0.22%, t -2.58) and days 2 to 5 also lose (-0.14%, t -0.75).
- F4: Fees exceed the gross gain. The position changes on 54% of days (mean absolute change 0.34 of the book), and the per-bar fee shares sum to 6.42 against summed gross position gains of 4.39. Three of six coins (LTC, ETH, XMR) have a negative mean daily book return, down to -0.068% for XMR.
