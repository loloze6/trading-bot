---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d3_nearness-to-ninety-day-high
line: 7.d not profitable
backtest: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d3_nearness-to-ninety-day-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 20-day return, the more it rises over the next 20 days.
Consequence: A trader should lean long on coins with the strongest 20-day rise rather than shorting coins far beneath their highs.
Why:
- F2: The shorts lose because a close far beneath the 90-day high is still followed by a rise. Grid cases with a negative forecast gain +1.6 % over 20 days (416 cases, excess t −0.85), against +3.4 % for positive forecasts (411 cases, excess t 0.59). So the forecast's lower half bets against the coins' drift.
- F6: The idea's size is not what fails. Its total move per case is 3.39 %, 17.6 times the 0.19 % cost of a trade. But the book is small: mean absolute allocation is 0.19 and mean net allocation 0.067, with 40 % of bars short. That is too little exposure to reach a mean daily return of 0.0005.
- F7: The 20-day return grades what follows, on both forecast sides. Among positive-forecast grid cases, the 20-day return that follows rises with the past 20-day return, from +1.4 % in the second quartile to +3.6 % in the third and +6.3 % in the top (129 cases). In the top quartile even negative forecasts are followed by +4.5 % (42 cases).
