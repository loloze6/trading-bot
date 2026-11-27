---
line: 7.g patterns
backtest: 074-01.b1.d1_wide-lower-close-calm-rebound_1d
idea tested: 074-01.b1.d1_wide-lower-close-calm-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4284 USD
---
## Findings
- **F1:** In the rising calm profile, the day after a close-to-close fall of 1 to 2 times the coin's 30-day swing beats the coin's drift by 0.29 of a usual daily move (t 2.41, 149 cases on 86 days). The excess shrinks as the day's return rises: 0.26 after falls of 2 to 3 swings (t 1.31, 23 cases), 0.09 after falls under 1 swing (t 1.89, 560 cases), 0.01 after rises under 1 swing (t 0.14, 624 cases) and -0.02 after rises of 1 to 2 swings (t -0.27, 245 cases).
- **F2:** The same grading holds on all bars in folds B and C, every profile together, but it is weaker. The next-day excess is 0.70 of a usual move after falls beyond 3 swings (t 0.97, 37 cases), 0.21 after 2 to 3 swings (t 1.85, 145 cases), 0.16 after 1 to 2 swings (t 2.11, 780 cases), 0.02 after falls under 1 swing (t 0.51) and -0.05 after rises under 1 swing (t -1.68, 3,090 cases). The rising calm reading in F1 (0.29) is about twice the all-profile one (0.16).
- **F3:** Inside the profile, where the day closes in its range does not order the next day the way the tested idea needs. Days 1 to 1.5 swings wide that close near their high (top 20 % of the range) are followed by -0.21 of a usual move (t -2.26, 125 cases). Days of that width that close in the lower part are followed by -0.03 (t -0.31, 143 cases) and -0.04 (t -0.36, 52 cases). The close-to-close fall of F1 carries the rebound more clearly than the close's place in the range.
- **F4:** Outside the profile, wide days ordered by close location point the same way, but no single cell is sure. Days 3 to 5 swings wide are followed by +0.27 of a usual move when they close in the bottom fifth of the range (t 1.84, 88 cases) and by -0.27 when they close in the top fifth (t -1.40, 62 cases). At 2 to 3 swings the readings are +0.15 (t 1.57) and -0.13 (t -1.46). This is the agitated wide low close rebound the map already holds in all three agitated profiles, so it is not a discovery.
- **F5:** Neither the weekday nor the 60-day trend bucket separates the next day on its own in folds B and C. Every weekday's mean excess has |t| at most 1.17 (about 1,180 cases each), and every trend bucket has |t| at most 1.63.
- **F6:** The tested situation is rare and strong in these folds. It fills 206 of 9,986 bars, and its raw next-day return averages +1.91 % and its 3-day return +3.46 % (171 cases). That is well above the +0.53 % total move per case step 5 measured over all folds, so folds A and D must hold much weaker cases.

## Ideas
- No ideas: every idea is a discovery

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `074-01.b1.d1.g1_rising-calm-scaled-fall-rebound` (from F1, F2, F3): In a rising, calm market, a coin's down day, measured as its one-day return against its 30-day swing of daily returns, is followed by a rise over the next day; the larger the fall against that swing, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
