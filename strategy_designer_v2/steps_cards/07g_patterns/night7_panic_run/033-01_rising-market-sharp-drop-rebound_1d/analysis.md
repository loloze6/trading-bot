---
line: 7.g patterns
backtest: 033-01_rising-market-sharp-drop-rebound_1d
idea tested: 033-01_rising-market-sharp-drop-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5603 USD
---
## Findings
- **F1:** In rising markets, the bars where the coin's 30-day swing is in its lowest third were followed by a 3-day return +1.97 % above the coin's normal drift (day-clustered t 2.83; 282 cases on 132 days; strength 0.21, four times the usual 0.05). The middle and top thirds earned only +0.13 % and +0.15 % (t 0.21 and 0.17), and outside rising markets the lowest third earned −0.66 % (t −1.23).
- **F2:** Inside rising markets the move is graded by how calm the last 30 days were compared with the last 90 days (the ratio of the 30-day to the 90-day swing). Going from the calmest quartile to the most agitated, the unusual 3-day move falls from +2.47 % (t 2.29, 133 cases) to +1.52 % (t 1.45), then +0.42 % (t 0.40), then −0.34 % (t −0.25).
- **F3:** The calm-and-rising excess holds across most of the sample:
- **F4:** Per case the calm-rising unusual move (+1.97 %) is about 10 times the cost of a trade (0.19 %). The tested idea's unusual move (+0.24 %) is only 1.2 times that cost.
- **F5:** The tested idea's grading is absent. In rising markets the slope of the 3-day unusual return on the day's scaled return is −0.0008 (day-clustered t −0.14, 981 cases, 270 days), and the falls of 2 or more usual swings earn +0.46 % (t 0.41, 14 cases).
- **F6:** The down days do better only in calm rising markets:
- **F7:** Two other angles did not stand out once checked properly, given the many angles I looked at:

## Ideas
- `033-01.g1_calm-uptrend-dip-rebound` (from F1, F6, F5, F4): In a rising, calm market, a down day is followed by a rise over the next 3 days, and the rise is larger the more that day's fall exceeds the coin's usual daily swing (the standard deviation of its daily returns over the past 30 days).

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `033-01.g2_quieting-uptrend-keeps-climbing` (from F1, F2, F3, F4): In a rising market, the lower the coin's swing over the last 30 days compared with its swing over the last 90 days, the more it rises over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
