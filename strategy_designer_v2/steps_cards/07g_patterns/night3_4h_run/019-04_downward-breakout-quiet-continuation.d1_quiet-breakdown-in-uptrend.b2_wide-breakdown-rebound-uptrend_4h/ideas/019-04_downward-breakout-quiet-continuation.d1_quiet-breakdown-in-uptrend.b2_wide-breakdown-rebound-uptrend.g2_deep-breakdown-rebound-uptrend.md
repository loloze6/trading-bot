---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend
line: 7.g patterns
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b2_wide-breakdown-rebound-uptrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: In a coin whose 30-day return is positive, a four-hour close below the lowest low of the preceding two days is followed by a rise over the next three days. The more of the broken two-day range the close falls through, measured in the coin's 30-day average four-hour range, the larger the rise.
Consequence: Treat a deep break below a recent range in a rising coin as a three-day buying chance, more firmly the deeper the break goes in usual bar ranges.
Why:
- F1: A sharp four-hour fall in a coin whose 30-day return is positive is followed by a rise over the next three days. Falls were taken as a bar's return of at most -2 times the coin's 30-day standard deviation of four-hour returns, de-overlapped to one per three days in each window. They are followed by a mean 18-bar return of +1.06 % above the coin's drift (t 2.61, 606 cases). The same falls when the 30-day return is negative give +0.14 % (t 0.37, 636 cases). Given the many angles examined, this t is only borderline.
- F2: Over all de-overlapped sharp falls, the deepest falls are followed by the largest three-day excess rise, and the grading is weak and uneven. Falls of -4 standard deviations or more give +1.36 % (t 2.26, 167 cases), against +0.45 % to +0.72 % for -4 to -2.5 and +0.35 % (t 0.80, 568 cases) for -2.5 to -2. The Spearman correlation between fall size and the excess return is 0.039 (p 0.17, 1243 cases). The mean strength is 0.067 (t 2.05).
- F4: On the 4h grid, the break below the prior two-day low in an uptrend gains more after a wider broken stretch. The narrow, middle and wide terciles give -0.24 % (36 cases), +3.84 % (t 2.19, 24 cases) and +7.15 % (t 2.22, 16 cases) of 18-bar excess return. These samples are small and much smaller than the verdict's 1182 cases.
