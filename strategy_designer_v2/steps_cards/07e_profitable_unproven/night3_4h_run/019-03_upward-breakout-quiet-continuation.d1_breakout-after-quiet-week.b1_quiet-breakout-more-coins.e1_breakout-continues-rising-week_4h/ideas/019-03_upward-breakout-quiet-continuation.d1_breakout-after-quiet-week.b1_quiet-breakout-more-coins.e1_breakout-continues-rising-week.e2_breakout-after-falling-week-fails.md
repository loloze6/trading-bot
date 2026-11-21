---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e1_breakout-continues-rising-week
line: 7.e profitable but not proven
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e1_breakout-continues-rising-week_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin's four-hour bar closes above its high of the preceding two days, the more the coin fell over the 7 days before that bar, the more it falls below its normal drift over the next 12 days.
Consequence: A trader should refuse a long on an upward breakout that comes after a falling week, the more so the deeper that week's fall.
Why:
- F4: Among breakout cases (a close above the prior 2-day high, one per 12-day cell), the 12-day unusual move splits on the 7-day return before the breakout. Cases in the top fifth of that return (mean +22 %) rise 5.4 % more than the coin's normal drift (t 3.2, 531 cases). Cases in the bottom fifth (mean -11 %) fall 5.9 % below it (t -8.1, 531 cases). The middle three fifths sit between -1.0 % and +0.6 %, which is why the plan's mean over all breakouts is near zero while its slope check passes (slope t 7.0 on the 7-day return).
- F8: The momentum move is large next to the cost of a trade: the top fifth's +3.1 % unusual move over 12 days (F5) is about 14 times the 0.22 % that a buy and a sell cost this backtest.
