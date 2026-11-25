---
line: 7.b inconclusive
backtest: 054-04_weak-reclaim-low-continuation_1d
idea tested: 054-04_weak-reclaim-low-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4062 USD
---
## Findings
- **F1:** Inside the profile (the recorded falling-agitated regime), the coin rose after a reclaimed 30-day-low pierce rather than fell: over 5 days the long-direction unusual move was +4.7 % (strength +0.45, t 1.40, 26 cases on 15 days), and over 10 days +6.0 % (t 1.12, 12 days). This is the same side as the verdict's -2.16 % in the short direction (t -1.21), the opposite of what the idea predicts, and too thin to be clear.
- **F2:** The idea's grading by nearness is absent. Inside the profile the Spearman correlation of nearness with the long-direction unusual move was +0.08 at 5 days and +0.15 at 10 days. By nearness tercile the coin rose in all three: far +2.0 %, mid +6.7 %, near +5.1 %. Closes nearer the low did not fall more.
- **F3:** The same pierce-and-reclaim was followed by a fall when the market was agitated but not falling.
- **F4:** The fall after a reclaimed pierce is graded by the coin's 60-day return.
- **F5:** The fall in markets that are not falling is spread across coins and years, at 10 days.

## Ideas
- `054-04.b1_reclaimed-low-after-rise` (from F3, F4, F5, F1): In an agitated market, when a coin's day trades below its lowest price of the past 30 days but closes back above that low, it falls over the next 10 days, and the fall is larger the higher the coin's 60-day return before that day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
