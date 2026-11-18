---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-04_flush-depth-retracement-size
line: 7.g patterns
backtest: 012-04_flush-depth-retracement-size_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a day a coin closes lower, the larger that day's volume relative to its mean over the prior 20 days, the larger the coin's rise over the next 3 days. The rebound comes from the volume burst itself, whatever the size of the lower wick.
Consequence: A trader would buy into down days in proportion to how unusual their volume is, and would not require a long lower wick or a deep open-to-low drop.
Why:
- F1: On down days, more volume relative to the prior 20 days' mean goes with a larger 3-day excess return: the slope of the excess 3-day return on log volume ratio is +0.0099 (t 3.70, n 2245 non-overlapping cases), while on up days it is -0.0020 (t -0.88, n 2470).
- F2: Among clearer falls (bar return of at most -1 usual move), the same slope is steeper: +0.0267 (t 4.16, n 577).
- F3: The effect sits in the top volume fifth. Down days in the highest volume-ratio quintile have a mean excess 3-day return of +0.0179 (t 3.76, n 454), while quintiles 0 to 3 lie between -0.0031 and -0.0007.
- F4: The rebound after sharp, heavy-volume falls does not need the wick. Falls of at most -1.5 usual moves with volume at least twice its mean earn a mean 3-day excess of +0.0206 without a long lower wick (n 47) and +0.0278 with one (n 35). The same falls on low volume earn +0.0002 (n 171) without a wick and -0.0115 (n 27) with one.
- F6: The volume-on-down-days slope is stronger in later years than earlier: on all days pooled it is +0.0054 (t 2.53) in 2022–25 against +0.0016 (t 0.58) in 2018–21. By coin it is positive in 4 of 6 (ZEC t 2.05; BTC t -0.84, XMR t -0.74), so it is a pooled effect and not one each coin shows strongly.
