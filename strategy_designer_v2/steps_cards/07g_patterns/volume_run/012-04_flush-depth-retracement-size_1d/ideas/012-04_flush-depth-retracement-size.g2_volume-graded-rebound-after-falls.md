---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-04_flush-depth-retracement-size
line: 7.g patterns
backtest: 012-04_flush-depth-retracement-size_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a day a coin falls by at least its usual daily move, the larger that day's volume relative to its prior 20-day mean, the larger its rise over the next 3 days. On such days the effect is steeper than on down days in general.
Consequence: A trader would size rebound longs after clear falls by the volume burst rather than by the fall's depth, which the book's losses show to be uninformative.
Why:
- F2: Among clearer falls (bar return of at most -1 usual move), the same slope is steeper: +0.0267 (t 4.16, n 577).
- F4: The rebound after sharp, heavy-volume falls does not need the wick. Falls of at most -1.5 usual moves with volume at least twice its mean earn a mean 3-day excess of +0.0206 without a long lower wick (n 47) and +0.0278 with one (n 35). The same falls on low volume earn +0.0002 (n 171) without a wick and -0.0115 (n 27) with one.
- F5: The tested signal is not what carries the rebound. Fall depth on flush bars has a slope of -0.0031 (t -0.75, n 73), and the book's 151 active days average -0.58% (t -1.67) with only 22.5% positive, from about 12 one-day trades per coin.
