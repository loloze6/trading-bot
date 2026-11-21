---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e1_breakout-continues-rising-week
line: 7.e profitable but not proven
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e1_breakout-continues-rising-week_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: The larger a coin's 7-day return, the more the coin rises above its normal drift over the next 12 days, whether or not its latest four-hour bar broke out of a range.
Consequence: A trader should hold a coin in proportion to the strength of its past week, rather than waiting for a range breakout to decide when to enter.
Why:
- F1: The book earns about as much per day as holding the coins, and most of its gain is the market's own rise: its mean daily return is 0.00138 against holding's 0.001388; 0.000849 of it (62 %) is the market's rise and 0.000531 is timing, over 2898 book days. Its Sharpe is higher (1.06) because it is out of the market part of the time.
- F2: The book earns when a coin is already rising and loses when it is falling, because its position follows the coin's trend. On coin-days split by the coin's prior 30-day return, the top two fifths (mean +13 % and +59 %) contribute +0.000493 and +0.001847 to the book's daily mean, at positions of 0.86 and 0.82. The bottom three fifths contribute -0.000563, -0.000472 and -0.000252, at positions of 0.22 to 0.74.
- F5: The 7-day return predicts the next 12 days on every bar, breakout or not. On non-overlapping 12-day grid bars (2680 cases), the slope of the unusual move on the 7-day return (scaled by the coin's usual move) has t 2.9. The top fifth gains +3.1 % (t 3.1) and the bottom fifth -0.9 %. The 185 breakout bars alone show a slope t of only 0.9, against 2.7 for the 2495 non-breakout bars.
- F7: The 7-day-return momentum at 12 days holds in most coins but in barely more than half the windows. The top fifth beats the bottom fifth in 14 of 19 coins (for example DOGE +10.2 % vs -7.3 %, XRP +6.9 % vs -4.8 %), but in only 14 of 24 windows.
- F8: The momentum move is large next to the cost of a trade: the top fifth's +3.1 % unusual move over 12 days (F5) is about 14 times the 0.22 % that a buy and a sell cost this backtest.
