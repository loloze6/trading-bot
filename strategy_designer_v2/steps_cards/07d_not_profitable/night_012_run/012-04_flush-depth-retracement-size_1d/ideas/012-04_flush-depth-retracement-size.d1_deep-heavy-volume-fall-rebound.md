---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-04_flush-depth-retracement-size
line: 7.d not profitable
backtest: 012-04_flush-depth-retracement-size_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Among bars that fall sharply on a volume burst, the larger the bar's drop from its open to its low against its usual size over the last 60 days, the larger the price rise over the next 3 days. The rise is larger the nearer the bar closes to its low, rather than leaving a long lower wick.
Consequence: A trader would buy deep, heavy-volume daily falls that close near their low and hold them for 3 days, and would refuse the same falls when a long lower wick has already absorbed the selling.
Why:
- F1: The long lower wick that the tested situation requires marks the wrong falls. Sharp falls (one-day return at or below -2 of its 20-day standard deviation) with a wick of at least 0.3 of the range were followed by a next-day excess return of -1.46% (t -2.36, n=86) and a 3-day excess of -0.83%. The same falls without the wick were followed by +1.12% next day (t 3.33, n=324). The flush bars the book traded were followed by a next-day excess of -0.71% (t -1.17, n=89).
- F3: The volume burst carries the rebound. Sharp falls with volume at least 2 times the prior 20-day median were followed by a 3-day excess of +1.02% (t 2.03, n=247) and a next-day excess of +0.95% (t 2.17). Sharp falls without the burst were followed by a 3-day excess of -1.04% (t -1.70, n=161).
- F4: The rebound is graded by depth among volume-burst sharp falls with no wick condition. Regressing the 3-day excess return on the open-to-low drop, scaled by its own 60-day mean, gives a slope t of 2.18 (220 independent cases). Return-depth terciles were followed by 3-day returns of +0.67%, +0.98% and +1.55%. The book's own wick-filtered flush bars showed no such grading (slope t -0.72, n=84).
- F6: The wick condition also makes the book trade too rarely. The book trades 0.005 per bar. Volume-burst falls of at least 2 standard deviations without the wick rule give 0.0127 independent cases per bar. Volume-burst falls of at least 1.5 standard deviations give 0.0186 per bar, with a 3-day excess of +1.33% (t 2.77, n=320).
