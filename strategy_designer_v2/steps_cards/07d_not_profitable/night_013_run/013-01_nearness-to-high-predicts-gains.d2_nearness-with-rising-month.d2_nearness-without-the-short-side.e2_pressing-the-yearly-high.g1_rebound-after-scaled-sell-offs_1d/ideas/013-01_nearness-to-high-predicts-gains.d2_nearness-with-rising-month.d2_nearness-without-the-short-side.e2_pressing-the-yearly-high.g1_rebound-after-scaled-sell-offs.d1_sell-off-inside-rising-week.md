---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high.g1_rebound-after-scaled-sell-offs
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high.g1_rebound-after-scaled-sell-offs_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall measured in units of its own 30-day daily volatility, the larger its rebound over the next 3 days, only while the coin's 5-day return up to that fall was positive, the rebound growing with the size of that prior 5-day rise.
Consequence: A trader would buy a volatility-scaled sell-off that interrupts a rising week, and refuse one that extends a flat or falling week, which is where the deep losses came from.
Why:
- F1: The book's worst moments come from being fully loaded into falls that keep going: on its 100 worst held bars the position averaged 0.98 against 0.45 on all held bars, the bar lost 6.6% on average and the coin fell a further 7.7%; on the book's 60 worst days the book lost 5.7% and the coin 8.7% while the position averaged 0.72 against 0.22 overall.
- F2: Those worst bars followed larger entry falls, a one-day return of −1.59 volatility units against −0.69 on all held bars, after a slightly falling prior 5 days, a scaled return of −0.17 against +0.06 on all held bars; so the deepest scaled falls are where the book is largest and where it is hit hardest.
- F3: By the coin's prior 5-day return before the fall, measured in units of its 30-day volatility, held bars in the top quartile (+0.60 to +4.75, a dip inside a rising week) earned 0.0056 per bar with only 3.5% of bars losing more than 3%. The two middle quartiles lost −0.0017 and −0.0009 per bar, with 7.5% and 5.1% of bars losing more than 3%.
- F4: On the 3-bar grid with forecast > 0, the slope of the excess 3-bar return on the forecast is positive and significant only in that top prior-5-day quartile (slope 0.0026, t 2.46, n 167, mean excess +2.25%); in the other three quartiles it is negative (t −0.65, −0.54, −1.40), while the pooled slope is t 0.90 over 5723 grid bars.
