---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g3_no-wick-heavy-fall-rebound
line: 7.b inconclusive
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g3_no-wick-heavy-fall-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: The larger the share of a day's fall that remains at the close, measured as how small the lower wick is against the day's range, the more the coin rises over the next day. This holds on down days whose volume is heavy against the prior 20-day average, and more so when 20-day volatility is high.
Consequence: A trader buys for one day after heavy-volume down days with no intraday bounce, and skips the ones already bought back within the day.
Why:
- F1: The step-5 result was inconclusive only because the supporting check could not be computed: the forecast is capped at its ceiling, with the median forecast at 20.0 and 50.2 % of the 3,272 active cases sitting at 20. That left 0 cases above the median against 1,629 below, while the main measure itself is on the idea's side with mean +0.089 and t 5.40.
- F3: The close's distance below the day's high is graded on heavy-volume down days, at −0.66 %, −0.03 %, +0.29 % (t 1.94), +0.79 % (t 4.59) and +0.86 % (t 2.90) for distance-from-high bins ≤0.25, 0.25–0.5, 0.5–0.75, 0.75–0.9 and >0.9. On ordinary-volume down days the same bins show no gradient (−0.08 % to +0.20 %, all |t| < 1.1), as the brief's control requires.
- F6: The uncapped raw product of the three parts ranks the next-day move monotonically at the extremes, with a Spearman of 0.118 with excess return. Its top quintile gives +1.22 % (t 2.80) and its bottom quintile −0.42 %. Cases above its median give +0.75 % against +0.35 % below, so a graded check would have passed.
- F7: The effect is positive on every coin, from BTC at +0.09 % (t 0.57) to XMR at +0.77 % (t 3.41). It is positive in 7 of 8 years, the exception being 2022 at −0.19 % (t −0.69). Its size is +0.30 % unusual and +0.42 % total per case, which is 1.5 and 2.2 times the 0.19 % trade cost.
