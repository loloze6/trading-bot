---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e1_weekly-momentum-three-day-continuation
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.e1_weekly-momentum-three-day-continuation_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: The larger a coin's fall over the past day, measured against its 30-day volatility, the more the coin rises over the next three days, by more than its normal drift.
Consequence: A trader should lean long a coin over the next three days in proportion to how sharply it fell over the past day, and refuse to sell into such a fall.
Why:
- F2: A sharp one-day fall is followed by a rebound much larger than a trade's cost. The bottom decile of the past day's return over 30-day volatility (mean −1.78) is followed by a 3-day strength of +0.193 (t 6.3, 1003 non-overlapping cases), an unusual move of +1.80 % per case, about 8 times the 0.22 % round-trip cost. Over 1 day the same decile gives +0.089 (t 4.2, 3082 cases, +0.45 %). The effect is graded: the second decile gives +0.049, the third −0.047, and among all falls corr(size of fall, strength) is 0.091 over 4950 cases (t about 6.4). It holds broadly: 18 of 19 coins and 16 of 24 windows are positive, and 6 of 8 years.
