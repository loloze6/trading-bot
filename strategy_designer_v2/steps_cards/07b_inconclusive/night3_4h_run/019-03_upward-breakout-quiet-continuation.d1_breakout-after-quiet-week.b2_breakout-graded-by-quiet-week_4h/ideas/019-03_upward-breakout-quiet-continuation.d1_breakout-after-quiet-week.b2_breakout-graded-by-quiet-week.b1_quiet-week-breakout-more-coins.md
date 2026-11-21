---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week
line: 7.b inconclusive
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes above the highest high of a coin's preceding two-day stretch, the coin rises over the next three days. The rise is larger the quieter the coin's average four-hour range over the past 7 days was compared with its average over the past 60 days.
Consequence: A trader should size an upward four-hour breakout by how quiet the preceding week was against the past two months, rather than by how narrow the two-day stretch itself was.
Why:
- F1: The tested result is on the predicted side but small and short of the bar. The mean 18-bar unusual move is +0.20 % (t 1.29, 3109 cases), a strength of 0.023 against a usual move of 8.17 %. That is under half the 0.05 typical of real ideas, and only 1.1 times the 0.19 % round-trip cost. Other horizons are no clearer: t 0.39 at 1 day, 0.68 at 2 days and 1.18 at 6 days.
- F7: With 3109 cases, a dispersion of 8.8 % per case and a mean of +0.20 %, this data cannot show the pooled effect clearly. Thirteen more coins are available in folds A and D, and some of them in B and C, which would roughly double or triple the case count.
