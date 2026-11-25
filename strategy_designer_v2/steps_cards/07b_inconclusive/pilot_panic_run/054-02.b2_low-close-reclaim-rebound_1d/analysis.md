---
line: 7.b inconclusive
backtest: 054-02.b2_low-close-reclaim-rebound_1d
idea tested: 054-02.b2_low-close-reclaim-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2063 USD
---
## Findings
- **F1:** The tested result is on the side the idea predicts but short of the bar. Step 5 found a mean unusual 5-day move of +2.95 % with t 1.55 over 75 cases on 49 days. In folds B and C the 39 active cases gain +4.1 % over 5 days (t 1.39, 23 days, 64 % up) and +7.3 % over 10 days (t 1.86), so the rebound grows with the horizon rather than fading.
- **F2:** The grading the idea predicts is present and carries the gain. Among the active cases, reclaims closing in the lowest third of their day's range gain +12.8 % over 5 days (t 2.01, 13 cases on 11 days, 77 % up). Those closing near the high gain −0.7 % (t −0.28), and the middle third +0.3 %.
- **F3:** The falling-agitated profile is where the situation lives. Across all reclaimed monthly-low pierces, the falling-trend cases gain +0.2 % over 5 days (70 cases). The choppy cases lose −10.1 % (t −1.56) and the rising cases −14.5 % (t −2.09, 10 days). All reclaims together lose −2.4 % (t −1.21, 138 cases).
- **F4:** The evidence is thin because the cases are few, not because the effect is mixed. Each coin has only 3 to 10 cases, 23 of the 39 cases fall in two windows (w14 with 13 and w18 with 10), and four of the six coins have a positive mean. Thirteen more coins have daily data in folds A to D and the test did not use them.

## Ideas
- `054-02.b2.b1_low-close-reclaim-all-coins` (from F1, F2, F4): In a falling, agitated market, when a coin's day trades below its lowest price of the past 30 days but closes back above that low, it rises over the next 5 days, and the rise is larger the lower the close sits within the day's range.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
