---
line: 7.g patterns
backtest: 058-01.g1.b1_thin-volume-fall-more-coins_1d
idea tested: 058-01.g1.b1_thin-volume-fall-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4866 USD
---
## Findings
- **F1:** Inside the falling calm profile, depth does not grade the fall that follows. On non-overlapping 5-day cells, the coin's mean 5-day excess return by 30-day-return quintile is -0.51 % for the deepest (mean 30-day return -34 %, 61 cases, t -0.40), -1.66 % for the second (t -1.72) and -3.63 % for the third (-15 %, t -2.64). The deepest falls are followed by the least further fall, against the brief's "the deeper, the more".
- **F2:** Inside the profile, among cells with a negative 30-day return, thinner volume goes with more falling, but the gap cannot be told from chance. The 5-day excess return is -0.02 %, -1.43 % and -2.43 % from the swelling-volume tercile (volume ratio 0.84) to the most-thinned tercile (ratio 2.08), with 60 cases each and t at best -1.43. This agrees with the step-5 size: unusual move +0.80 %, t 1.71.
- **F3:** In choppy markets (60-day return between -10 % and +10 %), the 30-day return measured in usual 30-day moves grades the next 5 days in its own direction, with a monotone step at every level:
- **F4:** The choppy continuation is strongest in agitated choppy markets: cells with a 30-day return between -1 and 0 usual moves fell a further -6.94 % (18 cases, 14 days, t -2.91), against -2.69 % in calm choppy ones (47 cases, t -1.76). Choppy agitated short is an empty cell of the profile map.
- **F5:** Outside the profile the 30-day return also continues over 5 days: -1.42 % and -1.86 % after the two lowest quintiles (t -1.50 and -2.84), +1.19 % and +3.16 % after the middle and fourth (t 1.70 and 3.15). The continuation is not specific to falling calm markets, which the brief names as a falsifier.
- **F6:** Patterns that did not hold up once cases on the same day were taken together, or across years, are not findings:

## Ideas
- `058-01.g1.b1.g1_choppy-market-fall-continues` (from F3, F4, F5): In a choppy market, the further a coin's 30-day return lies below zero, measured in its usual 30-day moves, the more it keeps falling over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
