---
line: 7.g patterns
backtest: 031-02.b1.b1_wide-flat-uprun-more-coins_1d
idea tested: 031-02.b1.b1_wide-flat-uprun-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4409 USD
---
## Findings
- **F1:** After a 5-day rise, a wide-range day (range at least 1.5 times its 20-day mean) with a bullish body (close-open over 50 % of the range) is followed by an unusual 10-day move of +3.70 %, with t 2.76 over 874 cases on 429 days and a strength of 0.172. This is the clearest effect in about 40 cuts examined, so it is still near the edge of what multiple testing allows.
- **F2:** The flat body the tested idea requires adds nothing after a 5-day rise. Wide-range days after a 5-day rise are followed by similar unusual 10-day moves whatever their body: flat gives +3.49 % (t 1.79, 148 cases), bullish +3.70 % (t 2.76, 874), bearish +4.14 % (t 1.28, 215). Narrow flat days after a rise give only +0.26 % (t 0.21, 606).
- **F3:** Among wide bullish days after a 5-day rise, the follow-through grows with the range width, by range-ratio tercile:
- **F4:** The size of the prior run does not grade it. By 5-day-rise tercile the move is +5.43 %, +3.59 % and +5.00 %. The Spearman correlation between the day's net move (in mean ranges) and the unusual 10-day move is 0.011 over 2,687 up-run up-days.
- **F5:** The effect is broad across coins but uneven over time and skewed:
- **F6:** Large up days after a 5-day rise (net move at least one mean daily range, r5 > 0) are followed by an unusual 10-day move of +2.79 % (t 2.47, 1,047 cases, 475 days). The down-side mirrors are weaker:
- **F7:** Over all bars on the 10-day grid, there is no reliable gradient in the next 10 days' unusual move by the day's range ratio, close location, volatility level or 5-day standardised return. The quintile extremes reach t 2.11 at most (most bearish body quintile, +0.24 usual moves), which is not distinguishable from chance among this many cuts.

## Ideas
- `031-02.b1.b1.g1_wide-day-extends-up-run` (from F1, F2, F3, F5): After a coin has risen over the past 5 days, a day whose high-low range is wide compared with its mean daily range over the past 20 days is followed by a further rise over the next 10 days, whatever the day's close against its open. The wider that day's range against the 20-day mean, the larger the further rise.
- `031-02.b1.b1.g2_strong-up-day-continues-run` (from F6, F1, F3): After a coin has risen over the past 5 days, a day that closes well above its open, measured against its mean daily range over the past 20 days, is followed by a further rise over the next 10 days. The longer that day's range against the 20-day mean range, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
