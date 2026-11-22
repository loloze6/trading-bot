---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b2_calm-weekend-falls-continue
line: 7.d not profitable
backtest: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b2_calm-weekend-falls-continue_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's price falls from Saturday 00:00 UTC to Monday 00:00 UTC while the coin's 30-day hourly volatility is low against its own last 6 months, it keeps falling over the next two days (Monday and Tuesday), the more so the smaller the weekend fall is against the coin's 30-day hourly volatility.
Consequence: A trader would follow modest calm-week weekend falls into Monday and Tuesday, and refuse to follow falls that are large against the coin's usual swings.
Why:
- F6: Measured against the coin's 30-day volatility, the size of the weekend fall grades the move the wrong way: the smallest falls are followed by a further fall of 1.16 % (t 2.78, 260 cases), and the largest falls by a rise of 0.54 % (t -1.07, 261 cases), with the middle quartiles in between (-0.18 % and +0.63 %).
- F7: In the strategy's own forecast buckets the grading holds only weakly: a forecast at or below -10 gives +0.88 % (t 1.95, 208 cases), -10 to -5 gives +0.53 %, and -5 to -2 gives +0.30 %; weekend rises show no reversal in the short direction in any quartile (-0.88 % to +0.36 %, all |t| < 1.9).
- F2: The losses come from positions held at other times than the signal's 48 hours: the 347 trades lasting 47 to 49 hours earn +0.28 % before fees (+0.18 % after); the 51 trades lasting over 200 hours (up to 2088 hours) lose -3.97 %; and the 422 trades of under 47 hours lose -0.70 % to -1.08 %, so all 884 short trades together average -0.46 % before fees and -0.56 % after.
