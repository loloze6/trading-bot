---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d3_nearness-reversal-after-quiet-week
line: 7.b inconclusive
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d3_nearness-reversal-after-quiet-week_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ
bar: 1d
period: folds A, B, C, D
---
Idea: The lower a coin's own 5-day return, the larger its rise over the next 5 days.
Consequence: A trader should lean long on a coin in proportion to how far it has fallen over the last 5 days, and refuse longs after a 5-day run-up.
Why:
- F2: The supporting check passed because of the coin's own short-term reversal, not because of the idea. Over all grid bars, whatever the forecast, prior 5-day return ≤ 0 minus > 0 gives +0.35 % minus -0.40 %, Welch t 2.34 on 4602 cases. Regressing the positive cases' excess 5-day return on both the forecast and the prior 5-day return gives t -2.68 for the prior return and t 1.31 for the forecast (2372 cases).
- F3: The idea's modulation runs the other way. The forecast's slope t is 0.35 after a 5-day fall (1183 cases) and 1.46 after a 5-day rise (1189 cases).
- F7: The prior 5-day return alone is graded among the positive-forecast cases. By prior-return quintile, from the lowest (mean prior return -13.8 %) to the highest (+14.2 %), the excess 5-day return is +1.11 % (t 1.99), +0.26 %, +0.77 %, -0.06 % and -0.47 %.
