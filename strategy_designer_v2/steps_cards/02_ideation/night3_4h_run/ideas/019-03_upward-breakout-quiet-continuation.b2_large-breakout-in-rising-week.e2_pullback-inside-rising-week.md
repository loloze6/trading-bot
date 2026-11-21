---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week
line: 7.e profitable but not proven
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: While a coin's 7-day return is positive, the farther its 4h close sits below the highest high of the preceding two days, measured in its 30-day average 4h range, the more the coin rises over the next three days.
Consequence: A trader would buy deep pullbacks inside a rising week instead of breakouts above the recent high, taking a move many times the cost of a trade.
Why:
- F3: The break itself adds nothing over the regime. On non-overlapping 3-day grid bars with a positive 7-day return, bars in an upward break show +0.49 % unusual move (n 292, t 0.79). Bars not in a break show +0.19 % (n 2394, t 1.10).
- F8: In a rising week, the deepest pullback below the prior 2-day high is followed by the largest rise. On grid bars with a positive 7-day return, the lowest quartile of (close minus 2-day high) in 30-day mean 4h ranges (mean -3.65 ranges) shows +1.81 % over 3 days (t 4.23, strength 0.21, n 557). That is 9.5 times the 0.19 % cost of a trade. The middle quartiles give -0.23 % and -0.50 %, and the break quartile +0.50 % (t 1.24).
