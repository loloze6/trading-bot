---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week
line: 7.d not profitable
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The further a coin's four-hour close lies above the highest high of its preceding two days, measured against its average four-hour range over the past 7 days, the more the coin rises over the next three days.
Consequence: A trader should treat the size of the push through a recent high, scaled by recent range, as a long signal in its own right.
Why:
- F2: The edge sits in how decisively the bar breaks out, not in how quiet the week was: with the close's distance above the prior 2-day high measured in units of the 7-day mean 4h range, the top fifth of breakouts has an unusual move of +1.31 % over 3 days (t 3.39, 590 cases), while the four lower fifths range from -0.77 % to +0.59 % (t -2.39 to 1.31).
- F3: The breakout bar's own return in units of the 7-day mean range grades the same way: the top fifth has +1.21 % (t 3.08, 590 cases) and the bottom fifth -0.54 % (t -1.79).
