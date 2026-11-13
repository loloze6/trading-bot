---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-04_dip-rebound-spans-days
line: 7.d not profitable
backtest: N4-04_dip-rebound-spans-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A sharp one-day drop is followed by a three-day rise mainly when the coin has risen strongly over the previous 20 days and its recent volatility is at or above its 60-day level. In a barely positive or calm trend, the drop is followed by no rise.
Consequence: A trader should take dip longs only inside strong, active uptrends and stay flat in weak or quiet ones.
Why:
- F4: The rebound needs a real uptrend, not the regime's bare "above 0". When the 20-day rise is under 6.2%, the 3-bar excess is -0.07% (t=-0.18, n=288). When the 20-day rise is 14.8-27%, it is +1.06% (t=2.23, n=288).
- F5: The rebound weakens when volatility is calm. In the lowest quartile of 20-day to 60-day volatility (ratio below 0.84), the 3-bar excess is -0.19% (t=-0.32, n=182). In the higher three quartiles it is +1.0% to +1.5% (t 1.39 to 1.96, n=182 each).
