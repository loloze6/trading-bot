---
line: 7.b inconclusive
backtest: 054-03_deep-pierce-reclaim-continuation_1d
idea tested: 054-03_deep-pierce-reclaim-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4004 USD
---
## Findings
- **F1:** Step 5's own result points the other way from the idea. Over 5 days the short-side unusual move is -1.72 % per case (t -0.93, 66 cases on 42 days), which means the coin rose. My recount of pierce-and-reclaim days inside the falling agitated profile in folds B and C agrees: the long-side unusual move is +3.9 % over 5 days (t 1.29, 30 cases, 15 days) and +6.6 % over 10 days (t 1.35, 27 cases).
- **F2:** Inside the profile the depth grading has the shape the idea predicts but sits on the rebound side, so there is no clear fall to amend toward. Over 5 days, shallow pierces rise +11.9 % (t 1.76, 9 cases), mid pierces rise +3.7 % (t 1.52), and deep pierces fall only -1.3 % (t -0.55, 12 cases); the Spearman correlation between depth and the 5-day move is -0.33.
- **F3:** The continuation the idea describes appears outside the falling agitated profile. Pierce-and-reclaim days there are followed by an unusual move of -4.1 % over 5 days (t -1.98, 113 cases, 75 days) and -5.8 % over 10 days (t -2.89, 93 cases, 62 days). Ordinary days in the profile drift +0.7 % over 5 days (t 0.52).
- **F4:** Split by the 60-day trend alone, the fall over 10 days is concentrated where the coin was not falling:
- **F5:** Across all profiles the fall over 10 days is graded by pierce depth:
- **F6:** Even where the effect shows, its size is far above the cost of a trade: about 11 % to 15 % over 10 days against 0.19 % per round trip. The tested book was in a position on only 2 % of the coins' days, so the tested profile was both the wrong place for the effect and a rare one.

## Ideas
- `054-03.b1_rising-market-reclaimed-low-continuation` (from F3, F4, F5, F6): In a rising market, when a coin's day trades below its lowest price of the past 30 days but closes back above that low, it falls over the next 10 days, and the fall is larger the deeper the day's low went below the 30-day low.
- `054-03.b2_choppy-market-reclaimed-low-continuation` (from F3, F4, F5, F6): In a choppy market, when a coin's day trades below its lowest price of the past 30 days but closes back above that low, it falls over the next 10 days, and the fall is larger the deeper the day's low went below the 30-day low.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
