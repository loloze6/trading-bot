---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines
line: 7.g patterns
backtest: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 90-day return is positive, the closer its close stands to its highest close of the past 20 days, the higher its return over the next 5 days.
Consequence: A trader in a coin rising over three months favours longs when it sits near its 20-day high and refuses shorts there.
Why:
- F3: In the same rising regime, nearness to the 20-day high predicts the next 5 days on all 6 coins: slope +0.094 usual moves per standard deviation, t 3.66, 1624 cases. The top quintile is followed by +0.096 usual moves (+1.70 % total). Read together with the scaled day return (correlation 0.29), both keep their own weight (t 2.87 and t 2.79).
- F4: The tested rebound is absent. In the falling regime (90-day return negative), the slope on depth below the 90-day high is t 0.79 over 1652 cases. The unusual move per case is -0.44 % (-0.050 of a usual move), and the total move of +0.13 % is 0.7 times the 0.19 % cost. Short-horizon continuation measures in this regime lean negative instead: 20-day return t -1.84, nearness to the 20-day high t -1.76, each with 1 or 2 of 6 coins positive.
