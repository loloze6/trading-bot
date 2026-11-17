---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The nearer a coin's daily close sits to its highest close of the past 52 weeks, measured as the percent it sits below that high rather than against the coin's usual distance from it, the higher its return over the next 7 days, with the effect concentrated in the closes closest to that high.
Consequence: A trader should hold coins long in proportion to their raw closeness to the yearly high and should not go long, or short, merely because a coin far below its high is less far below than usual.
Why:
- F1: The book earns too little to pay because it barely holds anything: its mean position is 0.017 of the book, the median absolute position is 0.08, and 27 % of bars are flat. That leaves a mean daily return of 0.000114, against the 0.0005 required, and a Sharpe of 0.52, against holding's 0.58. Its gain from the market's own rise is only about 0.00002 to 0.00004 a day per coin, against coin mean daily returns of 0.0007 to 0.0019.
- F2: The short side costs money. Short bars are 36 % of all bars and their mean gain is -0.00005, summing to -0.29, because the coins still rose 0.00065 a day on those bars. Long bars (37 %) carried a gain sum of +2.18.
- F3: The forecast standardises the distance against the coin's own past distance, so it is only 0.61 correlated with the raw percent below the 52-week high. Far from the high (more than 15 % below), 41 % of grid bars still had a positive forecast, yet those bars returned -0.0042 over 7 days against holding (n=1908).
- F4: The 7-day gain sits in the raw closeness to the high, and only in the closes nearest it:
