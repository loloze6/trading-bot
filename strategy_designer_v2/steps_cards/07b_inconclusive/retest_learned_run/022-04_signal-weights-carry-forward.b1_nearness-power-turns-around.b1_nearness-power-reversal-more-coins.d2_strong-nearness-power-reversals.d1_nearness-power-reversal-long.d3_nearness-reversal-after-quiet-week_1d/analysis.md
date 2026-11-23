---
line: 7.b inconclusive
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d3_nearness-reversal-after-quiet-week_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d3_nearness-reversal-after-quiet-week
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4494 USD
---
## Findings
- **F1:** The test's slope is on the predicted side but small: t 1.33 on 2489 positive-forecast grid cases. Within those cases the forecast is not graded: mean excess 5-day returns by forecast quintile are -0.11 %, +0.52 %, +0.01 %, +0.63 % and +0.72 %, each with t ≤ 1.41. What separates is a positive forecast against a zero one: +0.35 % against -0.38 % excess, with the top 40 % of the forecast minus flat at Welch t 2.50.
- **F2:** The supporting check passed because of the coin's own short-term reversal, not because of the idea. Over all grid bars, whatever the forecast, prior 5-day return ≤ 0 minus > 0 gives +0.35 % minus -0.40 %, Welch t 2.34 on 4602 cases. Regressing the positive cases' excess 5-day return on both the forecast and the prior 5-day return gives t -2.68 for the prior return and t 1.31 for the forecast (2372 cases).
- **F3:** The idea's modulation runs the other way. The forecast's slope t is 0.35 after a 5-day fall (1183 cases) and 1.46 after a 5-day rise (1189 cases).
- **F4:** The slope changes sign across periods and coins.
- **F5:** The idea is small against the coin's normal moves, and there is little left to scale.
- **F6:** Other horizons do not show the effect. On each horizon's own non-overlapping grid the slope t is 0.37 at 10 days (1234 cases), 0.91 at 15 days, 0.14 at 20 days (604 cases) and -0.09 at 30 days.
- **F7:** The prior 5-day return alone is graded among the positive-forecast cases. By prior-return quintile, from the lowest (mean prior return -13.8 %) to the highest (+14.2 %), the excess 5-day return is +1.11 % (t 1.99), +0.26 %, +0.77 %, -0.06 % and -0.47 %.

## Ideas
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d3_nearness-reversal-after-quiet-week.b1_nearness-reversal-all-coins` (from F1, F4): For a coin's nearness to its 90-day high, the larger both the excess of its past 365-day predictive power for 5-day returns and today's deviation of nearness from its usual level, when the reading points against a past relation that implies a fall, the larger the coin's rise over the next 5 days. This rise is larger the lower the coin's own 5-day return before the reading.
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d3_nearness-reversal-after-quiet-week.b2_five-day-fall-reverses` (from F2, F3, F7): The lower a coin's own 5-day return, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
