---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-03_resistance-breakout-continues-up
line: 7.g patterns
backtest: 020-03_resistance-breakout-continues-up_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes a day with a fall that is large relative to its volatility over the past 30 days, it tends to rise over the next day, and the larger the fall in units of that volatility, the larger the rise.
Consequence: A sharp, volatility-sized one-day fall is a reason to take a one-day long trade rather than to sell into it, and a reason to refuse a short after it.
Why:
- F1: On daily bars, a coin's next-day return after a fall that is large for its recent volatility runs above its normal drift. The bottom decile of the day's return divided by its prior 30-day volatility (mean z −1.93) is followed by +0.62 % next day, t 4.1 over 1440 days, strength 0.127. The second decile (mean z −0.86) gives +0.28 %, t 2.4. Deciles 3 to 10 lie between −0.20 % and +0.04 %, no t above 1.8 in size.
- F2: The rebound is graded within falls. Among the 7056 days with a negative vol-scaled return, the Spearman correlation between the size of the fall and the next day's excess return is −0.072 (p 1.6e-9): the larger the fall, the larger the rebound.
- F3: The rebound is not one stretch or one coin. For the bottom two deciles it is +0.45 % (t 3.1) in w1–8, +0.40 % (t 2.2) in w9–16 and +0.49 % (t 3.0) in w17–24. It is positive on all 6 coins, from BTC +0.20 % (t 1.1) to XMR +0.81 % (t 3.8). It is positive in all 8 years, strongest in 2020 (+1.31 %, t 3.7) and 2021 (+1.14 %, t 3.4).
- F4: The rebound does not depend on the 20-day trend. It is +0.46 % (t 3.6, 1763 days) after a falling 20 days and +0.44 % (t 3.1, 1111 days) after a rising 20 days.
- F6: The book's worst days are followed by a rising coin. After its bottom 5 % of daily returns, the coin gains +0.90 % next day (t 4.6, 864 days), against +0.05 % to +0.21 % after its other extreme bins. This is the same rebound as F1, which a 5-day long book that re-buys nothing leaves on the table.
- F8: The size of the fall rebound clears the cost of a trade. The bottom decile's unusual next-day move of +0.62 % is about 3.3 times the 0.19 % round trip of this backtest, while the tested idea's unusual 5-day move was 1.6 times it. Among the roughly 15 angles looked at, only the fall rebound (t 4.1 to 4.7) stands out. The Saturday next-day effect (+0.33 %, t 4.0) swings in sign across years (2022 −0.04 %, 2023 −0.13 %) and is a calendar condition, not a graded one.
