---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high
line: 7.g patterns
backtest: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's fall on a day, measured against its own volatility over the previous 30 days, the more the coin rises over the next day.
Consequence: After a sharp down day a trader should favour a long for the following day, larger the deeper the fall, and refuse a short that bets on the fall continuing.
Why:
- F1: Over the next day, a coin rises more than its normal drift after a large down day, by an amount that grows with the fall. The fall is that day's return divided by the coin's 30-day volatility. In the lowest decile (mean -1.77 volatilities) the next day ends +0.63 % above drift (t 4.19, 1524 cases, 59 % up). The second-lowest decile (mean -0.88) ends +0.29 % above drift (t 2.48, 1523). The middle and upper deciles end between -0.30 % and +0.04 %.
- F2: The rebound comes only from down days. On down days, the next day's volatility-scaled return falls as the day's scaled return rises: slope -0.064 (t -3.06, 7529 cases). On up days there is no matching effect: slope +0.018 (t 0.98, 7691 cases). Over all days the slope is -0.026 (t -2.75, 15220 cases).
- F3: Grouping by the raw daily return gives the same result. Days in the lowest quintile of a coin's own daily returns are followed by +0.45 % above drift the next day (t 4.63, 3450 cases). The other quintiles are followed by -0.20 % to -0.01 %.
- F4: The rebound is short-lived. On the 2-day grid, the lowest quintile of the scaled day return is followed by +0.55 % over 2 days (t 2.88, 1500). On the 3-day grid it is +0.23 % over 3 days (t 0.80, 1002), so nothing is added after the first day.
- F6: The rebound's size is large against costs. The lowest-decile rebound of +0.63 % in one day is about 3.3 times the 0.19 % round trip this backtest charged.
