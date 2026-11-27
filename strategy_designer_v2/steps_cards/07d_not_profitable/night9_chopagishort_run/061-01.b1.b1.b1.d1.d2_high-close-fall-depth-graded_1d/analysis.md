---
line: 7.d confirmed, not profitable
backtest: 061-01.b1.b1.b1.d1.d2_high-close-fall-depth-graded_1d
idea tested: 061-01.b1.b1.b1.d1.d2_high-close-fall-depth-graded
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4150 USD
---
## Findings
- **F1:** The book's gain rests on one window. Window w16 summed +0.107 of daily book return, while every other explored window summed between -0.0014 and +0.017. The book sat inside the profile's regime on only 0.6 % of bars, against 95.5 % "chop", which is why trades per day (0.0083) and the gain over holding both fail.
- **F2:** The signal is strong but rare. In the choppy agitated profile, a close in the top quarter after a negative 5-day return gave 46 non-overlapping 5-day cases on 43 days. The unusual short move was +5.5 % (t 3.68), with a total move of +4.7 % against a cost of 0.22 %, so cost is not what fails.
- **F3:** The close-location condition belongs to the idea, but its top-quarter cut is needlessly narrow. In the profile:
- **F4:** Inside the profile, among upper-half closes after a negative 5-day return, the move grows with the depth of the 5-day fall. The deep tercile gave +8.3 % (t 1.74, 35 cases), the middle +6.1 % (t 2.82, 34) and the shallow +3.1 % (t 2.01, 32). This supports grading the short by the fall's depth, not by how near the close is to the high (the upper-half band beat the top quarter in F3).
- **F5:** Outside the profile, a top-quarter close after a negative 5-day return still gave +1.4 % (t 2.09, 647 cases), and it is graded the same way. The deep tercile gave +3.9 % (t 3.56, 225 cases on 104 days), the middle +0.7 % (t 0.86) and the shallow -0.5 % (t -0.70). Bars outside the profile with a negative 5-day return and any close gave only +0.6 % (t 0.92, 1427 cases), so the high close after a deep fall is what carries the move.
- **F6:** Five days is the right horizon. Top-quarter cases in the profile gave +2.5 % over 2 days (t 1.90, 53 cases), +5.5 % over 5 days (t 3.68) and +5.9 % over 10 days (t 2.59, 42 cases). Holding longer adds almost nothing per case and halves the move per day.

## Ideas
- `061-01.b1.b1.b1.d1.d2.d1_upper-half-close-fall-graded` (from F2, F3, F4, F6): In a choppy, agitated market, when a coin's daily close sits in the upper half of that day's high-low range after its 5-day return has been negative, its price falls over the next five days, and the fall grows with the depth of that 5-day fall.
- `061-01.b1.b1.b1.d1.d2.d2_high-close-after-deep-fall` (from F1, F5, F6): When a coin's daily close sits near the top of that day's high-low range after a 5-day fall, its price falls over the next five days, and the deeper the 5-day fall, the larger the fall that follows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
