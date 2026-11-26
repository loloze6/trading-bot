---
line: 7.g patterns
backtest: 067-02_choppy-down-stretch-keeps-falling_1d
idea tested: 067-02_choppy-down-stretch-keeps-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4124 USD
---
## Findings
- **F1:** In choppy markets (folds B, C), a close below its 20-day average measured in 20-day standard deviations of daily returns is followed by further fall, and the fall grows with the raw stretch. Over 10 days the stretch quartiles from mildest to deepest show unusual moves of -0.4 %, -4.5 %, -6.7 % and -8.0 % (about 17 to 18 cases each). The mean continuation is +4.9 % (t 1.93 with one day's cases together, 70 cases on 40 days).
- **F2:** The same choppy below-average stretch over 5 days gives a mean continuation of +3.3 % (t 2.36 with one day's cases together, 128 cases on 80 days). Its slope on the raw stretch is 0.0151 (t 1.94), in the continuation direction. Most of the grading sits in the deepest quartile: -7.8 % against about -1.7 % to -1.9 % for the other three.
- **F3:** The tested forecast standardises the stretch over its past 60 values. On the same choppy cases it correlates 0.91 to 0.92 with the raw stretch, yet its slope runs the other way: t -0.62 at 10 days (70 cases) and t -0.94 at 5 days (128 cases). Over all folds, step 5 found an unusual move of only +0.32 % (t 0.44, 424 cases). The graded effect is in the raw stretch, not in its standardised version, and it is not yet confirmed outside folds B, C.
- **F4:** The theory claims both sides, but the carry above the average does not show in choppy markets. The mean continuation is -0.1 % at 5 days (t -0.09, 121 cases) and +0.6 % at 10 days (t 0.26, 56 cases).
- **F5:** Outside choppy markets the above-average side carries forward. At 10 days the top stretch quintile shows +4.2 % (t 2.73, 118 cases) and the slope on the stretch has t 2.56. This is a trending-market continuation that the map already holds in rising profiles (nearness to high, range-top and breakout continuation).
- **F6:** The book lost because short trades in choppy markets paid the coin's upward drift. Net trade returns were negative on all six coins, with medians from -1.3 % (BTC) to -6.4 % (ZEC). On the idea's cases the drift in the short direction was -1.15 % per 10 days against an unusual move of +0.32 %.
- **F7:** Other angles do not count toward ideas, given how many angles were looked at:

## Ideas
- `067-02.g1_choppy-down-stretch-five-days` (from F2, F1, F3, F4): In a choppy market, the further a coin's close stands below its 20-day average, measured in units of its 20-day standard deviation of daily returns, the more the coin falls over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
