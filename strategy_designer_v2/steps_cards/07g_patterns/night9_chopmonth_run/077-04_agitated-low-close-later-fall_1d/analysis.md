---
line: 7.g patterns
backtest: 077-04_agitated-low-close-later-fall_1d
idea tested: 077-04_agitated-low-close-later-fall
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4749 USD
---
## Findings
- **F1:** In agitated markets the close's place in the day's range is followed by the opposite move on the next day, not the same one. A close in the bottom quarter is followed by +0.81 % above drift (t 1.97, 861 cases on 337 days), and a close in the top quarter by −0.71 % (t −2.23, 1287 cases on 494 days). This is the known next-day reversal, and the map already holds it (045-01 agitated wide low close rebound, 058-02.b1.g1.b1.b1 falling agitated next day reversal).
- **F2:** The tested stretch, from the next day's close to the seventh day's close after an agitated low close, does not hold across grid offsets. On offset 0 it is −5.2 % (t −1.90, 117 cases, 47 days). Across the seven offsets it ranges from −7.2 % (t −2.10) to +3.5 % (t 1.64), and three of the seven are positive. The step-5 inconclusive verdict (+0.52 %, t 0.93) is the average of these mixed readings.
- **F3:** High-minus-low close spread, agitated (later-week return after a top-quarter close minus after a bottom-quarter close):
- **F4:** Within agitated markets split by trend, only rising agitated shows a graded later-week move from the close location: top quarter +8.7 % (t 2.32). But that rests on 36 cases on 21 days, it is one cell among about 20 compared, and rising agitated long is the map's most crowded box (10 strategies, among them range top continuation).
- **F5:** The calm-market 20-day-return quintiles give 6-day moves after drift that are not graded:
- **F6:** A large one-day fall (bottom quintile of a coin's daily returns) is followed by a next-day rebound above drift in both regimes: +1.02 % in agitated markets (t 4.70, 1140 cases) and +0.58 % in calm ones (t 3.20, 829 cases). This is the fall-rebound family the map holds 16 times in falling agitated alone.
- **F7:** The weekday effects on the next day do not stand out from the 7 groups compared:

## Ideas
- No ideas: The only patterns that stand out (the next-day reversal of close location in agitated markets and the next-day rebound after a large fall, F1 and F6) are ideas the map already holds; the rest (later-week continuation, rising-agitated high closes, calm 20-day momentum, weekdays, F2 to F5 and F7) either flip across grid offsets and coins or rest on too few days to stand out after the many angles looked at.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
