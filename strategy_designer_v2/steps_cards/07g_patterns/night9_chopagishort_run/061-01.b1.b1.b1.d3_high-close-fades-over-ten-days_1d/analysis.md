---
line: 7.g patterns
backtest: 061-01.b1.b1.b1.d3_high-close-fades-over-ten-days_1d
idea tested: 061-01.b1.b1.b1.d3_high-close-fades-over-ten-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3879 USD
---
## Findings
- **F1:** Over all bars in folds B and C, the next-day move relative to the coin's normal drift falls steadily as the close moves up the day's range: +0.63 % (t 2.16, 511 days), then +0.28 %, −0.08 %, −0.26 %, and −0.35 % for closes in the top fifth (t −1.71, 692 days). The top-fifth end on its own cannot be told from 0. Over 2 days the top fifth gives −0.46 % (t −1.15, 354 days) and over 5 days +0.35 % (t 0.30), so the gradient fades within a day.
- **F2:** In the choppy agitated profile the sample is very thin: on the 10-day grid only 10 bars reached the tested regime and 37 more sat in the profile without a high close, against 919 outside it. The in-profile top-fifth close shows −15.2 % over 10 days (t −3.82), but on only 10 cases. That is the tested idea itself, not a new pattern.
- **F3:** Inside the regime, the 10-day move has no gradient with closeness to the high. By close-location tercile it is −10.0 %, −22.2 % and −15.3 % (4, 3 and 3 cases). This matches step 5's failed supporting check (stronger half minus weaker half −1.35 %).
- **F4:** Weekday effects do not hold up once the cases of one day are pooled. The largest is Sunday's 2-day move of −1.15 % (t −1.42, 111 days), and the 1-day moves by weekday range from −0.44 % to +0.37 % with |t| ≤ 1.44. Sunday's 2-day move changes sign by year (+0.93 % in 2020 against −1.4 % to −2.3 % in the other years).
- **F5:** Range size and the previous day's return show no clear pattern outside the profile. By range quartile the 2-day moves run from −0.36 % (t −2.11) to +0.55 % (t 1.83), and the in-profile cells of the prior-day-return quintiles at 10 days rest on 8 to 9 cases each.
- **F6:** In-profile weekday cells at 10 days reach t −5.56 (Wednesday), but on 3 to 12 cases per cell, among more than 60 cells examined. That cell count is too large for any single one to stand out.

## Ideas
- No ideas: Across close location, prior-day return, range size, weekday, year and profile on 1-, 2-, 5- and 10-day horizons, nothing stands out from chance given that many angles. The strongest pattern, a one-day gradient with close location (F1), is at t 1.7 on its high-close side and is already the tested situation in a wider profile. The in-profile cells rest on about ten cases each (F2, F3, F6).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
