---
line: 7.g patterns
backtest: 054-01_deep-reclaimed-low-pierce-rebound_1d
idea tested: 054-01_deep-reclaimed-low-pierce-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5186 USD
---
## Findings
- **F1:** Outside the falling agitated profile, a day that pierces the prior 30-day low and closes back above it is followed by an unusual 5-day move of -4.43 % (96 de-duplicated cases on 65 days, t -2.22 with same-day cases taken together). Inside the profile the same event gives +4.72 % (21 cases, 11 days, t 1.15), so the tested idea's sign holds only in its own profile and is not reliable there.
- **F2:** The underperformance after a reclaimed 30-day-low pierce depends on the 60-day trend. It is -16.0 % in rising markets (10 cases, 9 days, t -2.87), -10.1 % in choppy markets (15 cases, 12 days, t -1.67) and -0.27 % in falling markets (57 cases, 35 days, t -0.10). The rising cell is small.
- **F3:** Outside the profile, the fall after a reclaim is concentrated in reclaims that close in the upper half of the day's range: -5.97 % (68 cases, 43 days, t -2.33), against -0.69 % for closes in the lower half (28 cases, 25 days, t -0.28). Deeper pierces are not graded: depth terciles give -2.0 %, -6.2 % and -5.1 %, Spearman -0.06 (p 0.57). The strength of the reclaim, not the depth of the pierce, is what goes with the fall.
- **F4:** The mirror event, a day that trades above the prior 30-day high but closes back below it, is followed by an unusual 5-day rise of +3.24 % (190 cases, 126 days, t 2.49). The rise is strongest in rising markets: +6.11 % (77 cases, 52 days, t 2.53). Closes above the 30-day high give +3.35 % (161 cases, t 2.91). This is the near-high and breakout continuation the map already holds in rising profiles (034-01.b1, 034-01.e1, 033-03.b2), so it is not a discovery.
- **F5:** On all bars, the days with the largest down move scaled by 20-day volatility (lowest decile) are followed by a next-day rise of +1.01 % (696 days, t 4.22, not clustered by day). This is the agitated-fall rebound the map already holds in falling agitated and agitated profiles (038-01, 047-01, 051-01).

## Ideas
- `054-01.g1_rising-market-reclaimed-low-fades` (from F1, F2, F3): In a rising market, when a coin's day trades below its lowest price of the past 30 days but closes back above that low, it falls over the next 5 days, and the fall is larger the higher the day closes within its own range.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
