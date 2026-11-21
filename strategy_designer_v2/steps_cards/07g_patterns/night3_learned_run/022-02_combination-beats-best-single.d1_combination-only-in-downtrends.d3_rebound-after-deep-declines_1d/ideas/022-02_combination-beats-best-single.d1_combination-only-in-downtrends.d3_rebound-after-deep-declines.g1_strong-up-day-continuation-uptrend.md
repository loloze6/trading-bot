---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines
line: 7.g patterns
backtest: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 90-day return is positive, the larger its 1-day rise measured against its typical daily move over the past 20 days, the higher its return over the next 5 days.
Consequence: A trader leans long after an unusually strong up day in a coin that is rising over three months, and refuses shorts against such a day.
Why:
- F1: When the coin's 90-day return is positive (the "unknown" regime), a day's return scaled by its 20-day volatility predicts the next 5 days. The slope is +0.097 usual moves per standard deviation (t 3.78, 1624 independent 5-day cases) and is positive on all 6 coins. It holds in both halves of the windows: t 2.32 on w1-w12 (716 cases) and t 3.05 on w13-w24 (908).
- F2: That effect comes from strong up days. The top quintile of scaled day returns (mean +1.54 volatility units) is followed by an unusual move of +2.68 % over 5 days (total +3.26 %, t 3.96, 326 cases), which is 14 times the 0.19 % cost of a trade. Among positive days alone the slope is +0.216 usual moves per unit (t 4.41, 824 cases), while the four lower quintiles show no slope (t -0.63). Its strength by year is uneven: t 4.63 in 2019, between -0.56 and 1.43 in the other years.
- F4: The tested rebound is absent. In the falling regime (90-day return negative), the slope on depth below the 90-day high is t 0.79 over 1652 cases. The unusual move per case is -0.44 % (-0.050 of a usual move), and the total move of +0.13 % is 0.7 times the 0.19 % cost. Short-horizon continuation measures in this regime lean negative instead: 20-day return t -1.84, nearness to the 20-day high t -1.76, each with 1 or 2 of 6 coins positive.
