---
brief: 010_rsi-midline-regime-direction
source-idea: 010-07_rsi-above-streak-reversal
line: 7.d not profitable
backtest: 010-07_rsi-above-streak-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The longer a coin's 14-day RSI has stayed on one side of 50 without a break, the more its return over the next 7 days follows that side: higher after long runs above 50, lower after long runs below 50.
Consequence: A trader should lean with the side RSI has held, and refuse to short a coin whose RSI has sat above 50 for days or weeks.
Why:
- F1: The book loses on both coins, and the timing part is a loss, not only the market part: Sharpe is -1.10 and the deepest fall is -97%. BTC's mean daily gain is -0.00132 (t -3.44), split into -0.00089 timing and -0.00042 market rise. ETH's is -0.00058 (t -1.73), split into -0.00028 timing and -0.00030 market rise.
- F2: The loss sits where the short is largest, in RSI-above-50 runs of 5 to 40 days. There the daily gain is -0.0017, -0.0022 and -0.0044 at allocations of -0.30, -0.62 and -1.05. In the same runs the coin's next-day return beats its average by +0.0023 (t 1.31, n 467), +0.0030 (t 1.85, n 597) and +0.0024 (t 1.58, n 665). The coin keeps rising inside its above-50 runs instead of reversing.
- F4: The mirror side follows its RSI too: in runs below 50 the coin's next-day excess return is -0.0013, -0.0016 and -0.0021 (t -0.86, -1.32, -1.44). On the 7-day grid, runs of 5 to 20 days below 50 show an excess of -0.0187 (t -2.28, n 174).
- F6: The book lost in the windows where the coin rose and gained only where it fell. Examples: w17 coin +0.0062 against book -0.0063, w11 +0.0099 against -0.0027, w21 +0.0038 against -0.0032. It gained in w14 (coin -0.0048, book +0.0001) and w2 (coin -0.0040, book +0.0001). So no single window carries the failure, and the Sharpe with one window left out stays at -1.17.
