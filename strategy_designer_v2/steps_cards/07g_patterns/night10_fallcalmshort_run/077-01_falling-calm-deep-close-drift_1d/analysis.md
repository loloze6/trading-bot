---
line: 7.g patterns
backtest: 077-01_falling-calm-deep-close-drift_1d
idea tested: 077-01_falling-calm-deep-close-drift
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3517 USD
---
## Findings
- **F1:** Over the recorded falling-calm bars (197 cases on the 3-day grid), none of the 11 measures of the bars predicts the coin's excess return over 1, 3, 5 or 10 days with a day-pooled t above 2.3. The measures were the depth below the 20-day high, the height above the 20-day low, the 1-, 3-, 5- and 10-day returns, the close's place in the day's range, range and body in usual swings, volume against its 20-day mean and the 20-day swing. Only the 5-day prior return at 5 days reaches t 2.26, a lone result among 44 tests.
- **F2:** The tested depth measure points the wrong way for a short at every horizon inside the profile, with t 0.45, 0.78, 0.43 and −1.07 at 1, 3, 5 and 10 days. Its quintiles do not climb: from shallowest to deepest the excess 3-day return is +1.52 %, +0.22 %, −1.99 %, −0.56 % and −0.72 %.
- **F3:** On the falling, calm bars rebuilt from closes (the recorded regime holds the profile on only part of the bars: 145 of 413 rebuilt-calm or unknown falling bars), deeper closes are again not followed by larger falls. Depth has t 1.05 at 3 days on 67 cases, and the mean excess 3-day return is +0.37 %, a rebound, not a continuation.
- **F4:** The one strong pattern is in the falling profile taken whole: the day's return is followed by its reverse the next day, t −2.99 on 224 cases, and still at 3 days, t −2.10. It vanishes in falling calm, with t 0.09 at 1 day and −0.61 at 3 days. It lives outside the box, and the map already holds it as 058-02.b1.g1.b1.b1, the falling agitated next-day reversal.
- **F5:** Inside the profile the coins' excess 3-day returns change sign by year and by coin, and no weekday stands out with 22 to 32 cases each:
- **F6:** The book's result is the coin's direction itself. On its best 5 % of days the coin fell 7.3 %, and on its worst 5 % it rose 7.1 %. Those days sum to +2.21 against −1.96, while the 688 active days together sum to −0.43, so there is no timing edge to rebuild from.

## Ideas
- No ideas: Across 11 bar measures, 4 horizons, weekdays, years, coins and the book's extreme days, nothing in falling calm markets on the short side stands out from chance (best t 2.26 among 44 tests); the only strong pattern, the one-day reversal in falling markets (t −2.99), lives outside the calm profile and is already held on the map.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
