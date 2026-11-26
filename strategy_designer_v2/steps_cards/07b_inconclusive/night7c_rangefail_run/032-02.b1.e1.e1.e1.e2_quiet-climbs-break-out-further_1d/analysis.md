---
line: 7.b inconclusive
backtest: 032-02.b1.e1.e1.e1.e2_quiet-climbs-break-out-further_1d
idea tested: 032-02.b1.e1.e1.e1.e2_quiet-climbs-break-out-further
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3957 USD
---
## Findings
- **F1:** The tested grading does not show. In folds B and C, the slope of the 20-day excess return on the run-up weight is -0.040 (t -0.37, 47 cases), and on the raw 60-day run-up itself it is -0.034 (day-clustered t -0.19, 34 days); step 5's slope t over all folds is -1.03, which is on the side opposite to the prediction.
- **F2:** The run-up quartiles show no order. Mean 20-day excess returns from the lowest to the highest run-up are +15.6 %, +8.5 %, +22.5 % and +9.7 % (11 to 12 cases each), and the run-up slope stays flat at 10 days (t 0.45) and 40 days (t 0.22), so no other horizon rescues the idea.
- **F3:** What does show is that 60-day-high breakouts rise whatever their run-up. Their mean 20-day excess return is +14.4 % (t 3.79, 47 cases), and both groups are positive: steep climbs (weight 0) +10.1 % (t 1.57, 15 cases) and modest climbs +16.4 % (t 3.48, 32 cases). Step 5 also measured an unusual move of +5.48 % (t 1.90, 110 days) over all folds.
- **F4:** A different gradient appears in how far the close goes past the prior high, and it runs the other way to the brief: the smaller the break, the larger the rise. In volatility units, the 20-day excess falls from +22.1 % for small breaks (strength 0.80 of a usual move, t 2.66, 16 cases) to +10.9 % for mid breaks (t 2.41, 15 cases) and +9.6 % for large breaks (t 1.61, 16 cases).
- **F5:** That break-size gradient is clearest at the longer horizon. On the raw percentage break, the day-clustered slope is -1.31 (t -1.25, 34 days) at 20 days and -4.16 (t -3.75, 23 cases, 16 days) at 40 days; on the break in volatility units it is -0.134 (t -2.77) at 40 days.
- **F6:** The small-break premium holds in every year with more than one case. Small breaks against large breaks at 20 days: 2019 +26.8 % vs +10.8 %, 2020 +38.4 % vs +15.8 %, 2021 +10.7 % vs -0.1 %. Modest-climb breakouts, by contrast, earned nothing in 2021 (+0.1 %, 11 cases).

## Ideas
- `032-02.b1.e1.e1.e1.e2.b1_narrow-breakouts-run-further` (from F3, F4, F5, F6): When a coin closes above its highest close of the prior 60 days, the less far that close lies beyond the prior high, the larger its rise over the next 40 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
