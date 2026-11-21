---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise.b1_largest-hourly-surges-continue
line: 7.g patterns
backtest: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise.b1_largest-hourly-surges-continue_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, is a fall several times its 30-day average absolute 24-hour return, the coin rises over the next 1 day by more than its usual 1-day return. The larger the fall against that average, the larger the rebound, with most of it after falls of about three times the usual size and more.
Consequence: A trader buys a coin at the hour of an exceptional 24-hour fall and holds for a day, sized up with the size of the fall, and refuses to sell into it.
Why:
- F1: The coin's 24-hour return, measured against its 30-day average absolute 24-hour return, is followed by a rebound after the largest falls. When the 24-hour fall is 3 or more times the usual size, the coin rises more than its normal drift over the next 24 hours by +1.88 % per case (strength 0.38, t 4.49, 363 cases). Over the next 48 hours the figure is +2.47 % (strength 0.39, t 3.75, 172 cases). Both are about 10 to 13 times this backtest's 0.19 % round trip.
- F2: The rebound is graded by the size of the fall. Over the next 24 hours the excess is +0.07 % for falls of 0.7 to 1.3 times usual (t 0.64), +0.45 % to +0.41 % for falls of 1.3 to 3 times (t 3.0 and 1.7), and +1.88 % beyond 3 times. The rank correlation across all falls of 1.3 times or more is weak (rho 0.040, p 0.06, 2147 cases), so most of the effect sits in the extreme falls.
- F3: The 24-hour rebound after falls of 1.3 times usual or more appears on every coin. It is +0.15 % on BTC (t 0.67) and rises through ETH and LTC (t 1.7 each) to XMR, XRP and ZEC (+0.80 % to +1.09 %, t 2.5 to 2.9).
- F5: The rebound holds in both 7-day regimes. When the 7-day return is negative it is +0.74 % (t 4.66, 1604 cases); when it is positive, +0.51 % (t 2.53, 543 cases).
- F7: The book's worst days come after the coin rose and are followed by the coin rebounding. On the book's worst-decile days the coin fell 6.13 % after a +1.34 % day before, then rose 0.69 % the next day (and the book 0.52 %). The book is long into falls and misses the rebound that F1 describes.
