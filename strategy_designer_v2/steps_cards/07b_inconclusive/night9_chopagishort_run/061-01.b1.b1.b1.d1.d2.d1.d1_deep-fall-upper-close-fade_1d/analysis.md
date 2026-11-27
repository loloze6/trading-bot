---
line: 7.b inconclusive
backtest: 061-01.b1.b1.b1.d1.d2.d1.d1_deep-fall-upper-close-fade_1d
idea tested: 061-01.b1.b1.b1.d1.d2.d1.d1_deep-fall-upper-close-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4123 USD
---
## Findings
- **F1:** The tested measure is on the predicted side but just short of the bar: the mean unusual 5-day move in the short's direction is +3.17 % (t 1.96, 139 cases on 99 days, all folds A to D on every available coin), and the test already used all the daily data there is, so more data cannot be added.
- **F2:** The depth grading the idea claims is absent: the top third minus the bottom third by |forecast| is −1.67 % (check failed), and in folds B and C the deepest third of 5-day falls gives +7.0 % (t 0.99, 11 cases) against +15.7 % for the middle third (t 2.16, 12 cases) and +7.6 % for the shallowest (t 1.28, 11 cases).
- **F3:** The effect in folds B and C rests mostly on one window: w16 gives +32.8 % per case (t 10.1, 10 cases on 4 days), while w15, w17 and w18 give +1.7 %, −1.4 % and +3.5 % (t 0.38, −0.67, 0.43), and ZEC goes the wrong way (−2.8 %, t −0.97, 8 cases) while the other coins are positive.
- **F4:** The fall is graded by how near the close sits to the day's high, as the brief said, rather than by the depth of the 5-day fall: on in-profile 5-day grid bars the unusual move rises with close location (Spearman 0.215, 86 cases), closes in the top tenth of the range give +7.1 % (t 2.70, 10 cases on 7 days), and without w16 they give +8.2 % (t 3.11, 9 cases), against −0.2 % to +2.7 % for the lower bands.
- **F5:** The negative 5-day return does sharpen the upper-close fade: among in-profile closes in the upper half, those after a 5-day fall lose +12.1 % unusual over 5 days (t 1.83, 22 cases), against +2.5 % (t 1.19, 25 cases) after a 5-day rise, while closes in the lower half give −1.3 % either way.
- **F6:** Five days is the right horizon for the tested cases: their unusual move is +6.6 % at 2 days (t 1.91), +9.9 % at 3 days (t 2.02), +9.4 % at 5 days (t 1.92) and +5.1 % at 10 days (t 1.05).

## Ideas
- `061-01.b1.b1.b1.d1.d2.d1.d1.b1_high-pinned-close-after-fall` (from F2, F4, F5, F6): In a choppy, agitated market, when a coin's daily close sits in the upper half of that day's high-low range after its 5-day return has been negative, its price falls over the next five days, and the fall grows with how near that close sits to the day's high, the closes pinned at the high carrying most of the move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
