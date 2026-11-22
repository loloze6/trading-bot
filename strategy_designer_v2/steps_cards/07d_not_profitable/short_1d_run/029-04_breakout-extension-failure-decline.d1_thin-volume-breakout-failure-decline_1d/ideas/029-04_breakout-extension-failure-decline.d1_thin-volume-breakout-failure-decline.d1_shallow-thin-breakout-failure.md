---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-04_breakout-extension-failure-decline.d1_thin-volume-breakout-failure-decline
line: 7.d not profitable
backtest: 029-04_breakout-extension-failure-decline.d1_thin-volume-breakout-failure-decline_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its prior 20-day high, reaches further above it within the next 3 days, and then closes back below the old high, the coin falls over the next 5 days, only while that close sits just under the old high, and the nearer to the old high the failed close and the lower the breakout day's volume against its 20-day average, the larger the fall.
Consequence: Short failed breakouts that slip only just back under the old high on a thin breakout day, and refuse those that have already dropped well below it, because those tend to bounce.
Why:
- F2: Failed 20-day breakouts as a whole carry almost no edge: the short-signed 5-day unusual move after a close back below the old high within 4 bars is +0.53 % (t 0.63, 128 cases), against −0.02 % on all other grid bars (3,291 cases).
- F3: The useful effect lies in how far below the old high the failure closes: shallow failures (close within 2.3 % below the old 20-day high) give +2.09 % (t 1.96, 64 cases), deep ones −1.03 % (t −0.80, 64 cases). The quartiles run monotonically from +2.19 % (shallowest) to −2.35 % (deepest), and the Spearman correlation of closeness with the move is 0.125.
- F4: The book's trades show the same split: trades entered on deep failures average −3.37 % net (37 trades), those entered on shallow failures −1.31 % (65 trades).
- F5: Thin volume adds to the effect only on top of shallowness. Shallow and thin (breakout-day volume below its 20-day mean) gives +6.55 % (t 2.57, 14 cases), shallow and heavy +0.84 % (50 cases), deep and thin −1.54 % (14 cases). Volume alone is not monotone: a ratio of 0.7–1.0 gives +3.98 % (18 cases), below 0.7 gives −0.14 % (10 cases).
- F6: The trap acts fast and fades. Failures 4–6 days after the breakout give −0.92 % (115 cases), and widening the failure window to 10 days drops the mean to −0.14 % (352 cases). Breakouts that pushed furthest above the old high (more than 6 %) give −1.10 % (118 cases).
