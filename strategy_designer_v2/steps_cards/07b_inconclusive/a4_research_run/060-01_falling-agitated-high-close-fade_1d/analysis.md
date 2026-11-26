---
line: 7.b inconclusive
backtest: 060-01_falling-agitated-high-close-fade_1d
idea tested: 060-01_falling-agitated-high-close-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2046 USD
---
## Findings
- **F1:** The main measure is on the side the idea predicts but well short of the bar. Step 5 measured a mean short-side next-day excess of +0.20 % with t 0.78 over 1,051 cases on 534 days, and an unusual move of +0.36 % with t 1.33 over 412 days. On the explore half of this book's coins (BCH, DOGE, ZEC), the 169 cases on 129 days give +0.65 % with t 1.15.
- **F2:** Inside the falling-agitated profile, upper-half closes are followed by next-day falls and lower-half closes by next-day rises. The short-side excess is +0.73 % (t 1.09, 84 cases), +0.57 % (55) and +0.55 % (30) for locations 0 to 0.5, 0.5 to 0.8 and 0.8 to 1. It is −0.54 % (102) and −1.16 % (t −1.93, 103) in the lower half.
- **F3:** The same split appears outside the profile, about half as large. Upper-half closes give +0.46 % (t 1.38, 532), +0.31 % (345) and +0.03 % (240); lower-half closes give −0.42 % (537) and −0.17 % (388). The profile sharpens the effect but does not create it.
- **F4:** Within the upper half the move is flat rather than rising toward the high (+0.73 %, +0.57 %, +0.55 %). Step 5's supporting check still passed (+0.55 % larger-|forecast| half minus smaller half). The grading is real only across the whole range, mid to high, not inside the upper half.
- **F5:** The effect varies a lot by coin and by year, which drowns it at this sample size.
- **F6:** The effect is not hiding at a longer horizon or in wide-range days. Overlapping 2-, 3- and 5-day excesses are +0.10 %, +0.49 % and +1.23 %, with t 0.12 to 1.15. Narrow, mid and wide day ranges give +0.55 %, +0.51 % and +0.88 %, with t at or below 1.0.
- **F7:** The idea's size, +0.36 % per case (0.068 of a usual 5.16 % move), is of the usual order for a real idea but only 1.1 times the 0.32 % cost of a trade. Telling it from zero needs many more falling-agitated cases than the six core coins supply, and the idea's 19-coin daily data holds 13 more coins in folds A to D.

## Ideas
- `060-01.b1_falling-agitated-high-close-fade-wider` (from F1, F2, F5, F7): In a falling, agitated market, a coin that closes near the top of its day's high-low range falls over the next day, and the nearer the close sits to the day's high, the larger that next-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
