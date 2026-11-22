---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b2_near-high-momentum-three-days
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b2_near-high-momentum-three-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The calmer a coin's past 20 days relative to its own past 4 months, the larger its move over the next 3 days in the direction of its distance from its 20-day mean, measured in units of its daily volatility.
Consequence: A trader reads a quiet coin that has pulled away from its 20-day mean as the start of a move to follow for a few days, not as a stretch that will snap back.
Why:
- F1: Over the next 3 days a coin follows its own past 3 days only when it has been calm. On non-overlapping 3-day cases, regressing the standardised excess return on the 3-day return scaled by the 20-day daily volatility gives slope 0.067 with t 3.70 (n 1716) in each coin's lowest-volatility tercile, against t 0.80 and 0.84 in the middle and highest terciles (n 1715 and 1716).
- F4: The same grading shows when calm is measured against the coin's own recent history. With 20-day volatility divided by its 120-day median, the slope on the scaled 3-day return is t 2.26 in the lowest tercile, 0.76 in the middle and −0.33 in the highest (n about 1091 each). The 20-day mean deviation in volatility units gives t 3.09 in the calm tercile and 0.83 and 1.44 in the others.
- F6: The brief's range reversion does not show in these bars. The slope of the excess return on position in the 30-day range is positive (continuation), not negative. In the flattest third of months it is +0.019 with t 0.22 (n 1428).
