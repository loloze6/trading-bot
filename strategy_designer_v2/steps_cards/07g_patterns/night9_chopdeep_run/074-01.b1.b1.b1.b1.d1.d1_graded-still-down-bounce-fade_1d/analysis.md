---
line: 7.g patterns
backtest: 074-01.b1.b1.b1.b1.d1.d1_graded-still-down-bounce-fade_1d
idea tested: 074-01.b1.b1.b1.b1.d1.d1_graded-still-down-bounce-fade
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.5126 USD
---
## Findings
- **F1:** In a falling market (60-day return below -10 %), up days whose 5-day return is still negative are followed by a weaker next day, and the narrowest fifth does not fade at all. By coin width quintile (day range over its 20-day mean range), the drift-adjusted next-day returns are +0.04 % (t 0.06, 170 cases, 85 days), -1.63 % (t -2.33, 133 cases), -1.58 % (t -2.41, 115 cases), -1.19 % (t -1.34, 94 cases) and -2.46 % (t -2.73, 86 cases, 41 days). The tested effect is there, but it is a step from narrow to everything else more than a smooth grade.
- **F2:** In falling markets the fade belongs to up days that are still down over 5 days. Wide up days with a positive 5-day return give -0.58 % (t -1.08, 207 cases) against -1.57 % (t -1.94, 153 cases) when the 5-day return is negative. Narrow up days with a positive 5-day return even give +0.65 % (t 1.21).
- **F3:** The still-down fade does not depend on agitation: -1.28 % (t -2.04, 328 cases, 118 days) in agitated markets and -1.09 % (t -2.06, 270 cases, 119 days) in calm ones. The tested idea's falling profile is already the right box, and its falling calm short cell is held by this very book.
- **F4:** After the widest fifth of still-down up days in falling markets, the second day rises by +1.73 % (t 2.38, 85 cases, 40 days). The other quintiles give -0.38 % to -1.09 % (all |t| < 1.8). The widest bounces may whipsaw rather than fade cleanly, but 40 days among more than 100 cells read is not enough to stand out from chance.
- **F5:** Falling, agitated, wide down days are followed by +1.76 % the next day (t 2.33, 273 cases, 100 days). This repeats the falling agitated long rebound family that the map already holds 16 times.
- **F6:** Up days in choppy markets lean weak but never clear chance:
- **F7:** The book's gain is concentrated in a few days and one year:
- **F8:** No weekday pattern stands out, either on all bars or in the book. The weekday next-day means range from -0.36 % to +0.39 %, all |t| < 1.5.

## Ideas
- No ideas: Outside the tested idea itself (F1 to F3), the only patterns near |t| 2 are a day-2 whipsaw after the widest bounces (F4, 40 days), which is too thin to stand out after more than 100 cells were read, and the falling agitated wide down-day rebound (F5), which the profile map already holds; the empty choppy agitated short cell shows only a lean that does not clear chance (F6).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
