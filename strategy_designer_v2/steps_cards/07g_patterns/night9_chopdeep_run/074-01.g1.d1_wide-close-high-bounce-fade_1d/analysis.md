---
line: 7.g patterns
backtest: 074-01.g1.d1_wide-close-high-bounce-fade_1d
idea tested: 074-01.g1.d1_wide-close-high-bounce-fade
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4616 USD
---
## Findings
- **F1:** In the coin's falling agitated profile, a wide up day that closes in the upper half of its range is followed by a next-day excess return of -2.03 % (t -2.76; 113 cases on 66 days). The same day that closes in the lower half is followed by +0.31 % (t 0.11; 23 cases). The tested fade therefore needs the high close, as the idea states.
- **F2:** Inside that profile the fade grows with the day's width. The narrowest third of these days is followed by -1.26 % (t -1.00, 31 days), the middle third by -2.07 % (t -2.74, 27 days) and the widest third by -2.75 % (t -2.10, 23 days). This is the grading the idea claims.
- **F3:** The fade is specific to falling agitated markets. Wide up days closing high are followed by -0.64 % (t -1.15, 74 days) in falling markets outside the profile, by -0.48 % (t -0.93, 75 days) in choppy markets and by +0.78 % (t 1.82, 188 days) in rising markets. That last figure is a continuation already held by the map's rising-market breakout and range-top strategies.
- **F4:** On the second day after a wide up day closing high in the profile, the coin rises +1.36 % above its drift (t 2.23; 113 cases on 66 days), against +0.45 % (t 1.90, 453 days) outside the profile. Part of the fade is given back. With the many angles looked at, a t of 2.2 cannot be told from chance.
- **F5:** In the profile, the largest one-day falls are followed by the largest rebounds. The lowest quintile of the day's return is followed by +2.16 % (t 3.59, 133 days). Wide down days closing low are followed by +3.13 % (t 3.43, 77 days), graded by width at +2.72 %, +2.36 % and +3.61 % across terciles. Outside the profile the lowest quintile is followed by only +0.28 % (t 0.87). This falling agitated long rebound is already held by 16 strategies in the map.
- **F6:** Weekday shows no pattern. No weekday's next-day excess return reaches |t| 2, either in the profile (largest t 1.88, Tuesday) or over all days (largest |t| 1.46).

## Ideas
- No ideas: The only patterns that stand out are the tested fade itself (F1–F3) and the falling agitated down-day rebound (F5), which the profile map already holds 16 times; the second-day give-back (F4, t 2.23) does not stand out after this many angles, and weekdays (F6) show nothing.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
