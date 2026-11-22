---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-03_panic-rebound-in-downtrend.d2_deep-one-day-fall-rebound
line: 7.d not profitable
backtest: 027-03_panic-rebound-in-downtrend.d2_deep-one-day-fall-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The deeper a coin's 24-hour fall against its usual 24-hour move, the higher its return above its normal drift over the next 14 days, only while its last 24 hours' bar range is wider than its usual 30-day bar range, and the more so the wider that range relative to usual.
Consequence: Treat a one-day drop as a reason to go long for two weeks only when it comes in a wide-range, panicky day, sized by depth times range expansion, and stay out of calm drops; this cuts the always-long exposure that sinks the book's Calmar.
Why:
- F2: The forecast does not decide when the book is in the coin. The forecast is 0 on 51 % of bars, yet the allocation stays positive on 98.8 % of those bars at a mean of 1.07, because each signal is held for 84 bars (14 days). So the book sits through every market fall, with no link to whether a panic happened.
- F3: Fall depth alone carries no unusual move. Across 1152 cases the unusual move is -0.06 % per case (strength -0.005) and the pooled slope t is -0.87. Among the 441 grid falls, the slope of the 14-day excess return on depth has t 1.13.
- F4: The effect appears only where the fall comes with an unusually wide range, and it is graded by that width. Falls in the lowest quartile of 24-hour range against the 30-day range (ratio 0.53) have a 14-day excess of -2.3 %, while the top quartile (ratio 1.64) has +1.2 %. The slope on the range ratio has t 2.24, and depth × range ratio has t 1.76 (n 441).
- F6: The book's falls are the market's falls. Its 200 worst 30-day spells average -32.7 % against holding's -31.4 % over the same spells. In the five worst windows it was long on 98–100 % of bars, mostly after 30-day declines (mean 30-day return when long -5 % to -17 %).
