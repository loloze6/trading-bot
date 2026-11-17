---
line: 7.b inconclusive
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4108 USD
---
## Findings
- **F1:** The test fails on grading, not on direction. Among Sunday rises the next 2-day excess return is about the same at every size (bottom, middle and top thirds by |forecast|: −1.44%, −0.64%, −1.15%). The rank correlation of the rise's size with the 2-day excess is −0.008 over 2147 Sunday rises. So the top-minus-bottom check comes out at +0.0029 while the main t is 4.88 over 2574 cases.
- **F2:** The reversal after a Sunday rise acts as an on/off sign effect. All five rising Sunday deciles (mean Sunday return +0.4% to +8.7%) are followed by a 2-day excess between −0.96% and −1.46% (t −2.3 to −4.3). Pooled, Sunday rises give −1.16% over 2 days (t −6.74, n 2147) and −0.54% on Monday alone (t −4.46).
- **F3:** The other side of the weekend is graded. Sunday falls are followed by a 2-day excess of +0.57% (t 3.44, n 2086). It grows with the size of the fall: +1.25% after the largest falls (mean −7.5%, t 2.81), +1.03% after −3.4% (t 2.65), +0.83% after −2.0% (t 2.35), and about −0.14% after falls of −0.3% to −1.1%.
- **F4:** Over the full range of Sunday returns the 2-day move goes the other way and is graded. The rank correlation of the Sunday return with the next 2-day excess is −0.12 (n 4233). Rises minus falls give a Welch t of −7.24 at 2 days and −7.30 at 3 days.
- **F5:** The effect belongs to Sunday's own 1-day return, not the whole weekend. Deciles of the Saturday-plus-Sunday 2-day return show no ordering: the largest weekend rises are followed by −0.51% (t −1.09) and middle deciles by −0.98% (t −3.55).
- **F6:** The effect is concentrated around Sunday. Rises sized against the last 60 days are followed over 2 days by −1.00% when the day is Sunday (t −5.94), −0.30% on Monday (t −1.94), +0.44% on Thursday (t 2.72) and −0.03% on Saturday (t −0.22).
- **F7:** The effect does not depend on Sunday's relative volume. Among Sunday rise cases, the 2-day excess is −1.23%, −0.86% and −1.38% for low, middle and high volume against the 60-day average. So the brief's volume grading is not visible either.

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways` (from F2, F3, F4, F5, F6): A coin that moved over the weekend (its Saturday-to-Sunday close-to-close return) moves the other way over the next 2 days (Monday and Tuesday), and the larger the weekend move in either direction, the larger the move back.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday` (from F1, F3, F6): A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 2 days (Monday and Tuesday), and the larger the weekend fall, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
