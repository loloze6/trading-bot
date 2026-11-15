---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.b inconclusive
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close is above its 200-day average, it rises more than its usual drift over the next 20 days, only in the cases where its close sits furthest above that average relative to its own past distances.
Consequence: A trader would treat only the most stretched cases above the 200-day average as a reason to be long, and treat milder cases as no better than holding.
Why:
- F2: That small positive mean rests on a few extreme up-moves: skew is 7.4, the five largest cases sum to 4.1 times the total of all 399, and without ZEC the mean turns to −0.0035 (t −0.29).
- F3: The plan's grading does not hold. By distance above the average, the four quartiles give mixed means (+0.005, −0.019, +0.031, +0.004) with all medians negative. Only the top forecast quartile is positive (+0.072, median −0.015), against −0.035, −0.004 and −0.013 for the other three.
