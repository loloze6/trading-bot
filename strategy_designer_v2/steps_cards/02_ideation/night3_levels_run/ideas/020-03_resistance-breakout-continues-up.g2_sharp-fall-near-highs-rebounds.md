---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-03_resistance-breakout-continues-up
line: 7.g patterns
backtest: 020-03_resistance-breakout-continues-up_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin that is still close to its highest close of the past 90 days falls sharply in one day relative to its 30-day volatility, it tends to rise over the next day, and the larger the fall in units of that volatility, the larger the rise.
Consequence: A sharp fall that leaves a coin near its 90-day high is a reason to buy for the next day, more than the same fall deep below that high.
Why:
- F1: On daily bars, a coin's next-day return after a fall that is large for its recent volatility runs above its normal drift. The bottom decile of the day's return divided by its prior 30-day volatility (mean z −1.93) is followed by +0.62 % next day, t 4.1 over 1440 days, strength 0.127. The second decile (mean z −0.86) gives +0.28 %, t 2.4. Deciles 3 to 10 lie between −0.20 % and +0.04 %, no t above 1.8 in size.
- F2: The rebound is graded within falls. Among the 7056 days with a negative vol-scaled return, the Spearman correlation between the size of the fall and the next day's excess return is −0.072 (p 1.6e-9): the larger the fall, the larger the rebound.
- F5: The rebound is largest when the fall comes close to the coin's 90-day high. In the shallowest third of the 90-day drawdown it is +0.91 % (t 4.5, 887 days), against +0.11 % (t 0.7) and +0.24 % (t 1.8) in the two deeper thirds.
- F8: The size of the fall rebound clears the cost of a trade. The bottom decile's unusual next-day move of +0.62 % is about 3.3 times the 0.19 % round trip of this backtest, while the tested idea's unusual 5-day move was 1.6 times it. Among the roughly 15 angles looked at, only the fall rebound (t 4.1 to 4.7) stands out. The Saturday next-day effect (+0.33 %, t 4.0) swings in sign across years (2022 −0.04 %, 2023 −0.13 %) and is a calendar condition, not a graded one.
