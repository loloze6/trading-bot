---
line: 7.e profitable but not proven
backtest: 032-02.b1.e1.e1.e1.e3_first-break-short-follow-through_1d
idea tested: 032-02.b1.e1.e1.e1.e3_first-break-short-follow-through
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3882 USD
---
## Findings
- **F1:** The book earns mainly from timing, not from the market's own rise. Its mean daily return is 0.0548 %, of which 0.0134 % is the coins' drift and 0.0415 % is timing (t of the book 1.96, Sharpe 0.98, over 1449 days).
- **F2:** First 60-day-high breaks are followed by a rise above the coin's normal drift, and the rise lasts past the plan's 3 days. The excess is +1.68 % over 3 days (t 2.57, 260 cases, strength 0.18 of a usual move) and +2.87 % over 10 days (t 2.02, 253 cases), but only +0.40 % over 1 day (t 1.02) and +1.61 % over 20 days (t 0.94).
- **F3:** The plan's grading by small margin does not hold. By margin quartile the 3-day excess is −0.32 % for the smallest margins (median 0.66 %), +2.71 % and +3.81 % for the middle two, and +0.56 % for the largest (median 8.9 %). The largest margins show a 20-day excess of −7.7 %. The gain sits in moderate overshoots, not small ones.
- **F4:** How wide the prior 60-day range was grades the follow-through, from narrowest to widest quartile:
- **F5:** The coin's 60-day rise before the break grades the follow-through the same way. The 20-day excess falls monotonically from +24.0 % in the smallest-rise quartile (median 16 %) to +12.9 %, +6.2 % and +1.0 % in the largest (median 89 %). The 10-day t is 2.71 in the smallest-rise quartile and 0.65 in the largest.
- **F6:** A break after a steep 20-day run fails. In the quartile with the largest prior 20-day rise (median 56 %), the excess is −0.98 % over 3 days and −7.2 % over 20 days. In the smallest quartile (median 12 %) it is +2.6 % and +12.8 %.
- **F7:** The gain is uneven across coins and trades.

## Ideas
- `032-02.b1.e1.e1.e1.e3.e1_narrow-range-breakout-follow-through` (from F2, F4, F1): When a coin's close rises above its highest close of the prior 60 days, the narrower the range of its closes over those 60 days, the larger its rise over the next 10 days.
- `032-02.b1.e1.e1.e1.e3.e2_quiet-climb-breakout-continuation` (from F5, F6, F2): When a coin's close rises above its highest close of the prior 60 days, the smaller its 60-day return before that close, the larger its rise over the next 20 days.
- `032-02.b1.e1.e1.e1.e3.e3_moderate-overshoot-breakout-follow-through` (from F3, F2): When a coin's close rises above its highest close of the prior 60 days by a moderate margin, its rise over the next 3 days is larger the closer that margin is to the middle of the coin's usual break sizes, and the rise is smallest for breaks that barely clear the high or overshoot it widely.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
