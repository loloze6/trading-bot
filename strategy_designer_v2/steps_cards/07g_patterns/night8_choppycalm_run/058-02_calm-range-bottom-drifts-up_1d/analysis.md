---
line: 7.g patterns
backtest: 058-02_calm-range-bottom-drifts-up_1d
idea tested: 058-02_calm-range-bottom-drifts-up
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3966 USD
---
## Findings
- **F1:** In choppy calm bars the tested side runs the wrong way. Excess 5-day returns rise with the close's position in its 20-day range (slope 0.0385, t 2.81, 178 non-overlapping cases), so the theme's pull back to the middle is reversed.
- **F2:** In choppy calm bars, closes in the bottom fifth of the 20-day range lose -3.07 % against the coin's drift over 5 days (strength -0.23, t -1.72, 18 cases). The next band loses -1.38 % (40 cases) and the middle -2.66 % (t -2.16, 52 cases). This matches step 5's size of -1.20 % per case (t -2.78, 322 days).
- **F3:** In the same choppy calm bars, closes in the top two fifths of the range rise +1.67 % (38 cases) and +2.38 % (30 cases) above drift, against -2.66 % in the middle. That meets the brief's own condition for being wrong: top closes rise more than middle ones.
- **F4:** Range-position continuation also holds outside the profile. The slope is 0.0268 (t 4.33, 1,186 cases). It is 0.086 (t 4.40, 125 cases) in choppy 60-day trends and 0.058 (t 3.88, 318 cases) in rising ones, against 0.020 (t 1.78, 369 cases) in falling ones.
- **F5:** In choppy 60-day trends, closes in the lower 40 % of the range lose -5.57 % against drift over 5 days (42 cases), while those in the upper 40 % gain +3.52 % (44 cases).
- **F6:** The positive slope holds in all six coins over all bars (t from 1.61 for ZEC to 3.72 for XRP). It is positive in 8 of 12 windows. Inside the profile it is strongest in XRP (slope 0.267, t 4.52, 20 cases).
- **F7:** Two strong patterns are already held. Rising-trend closes in the top fifth of the range gain +5.30 % over 5 days (t 2.30, 96 cases), already held as range-top continuation in rising markets. Friday and Saturday daily coin returns are +0.53 % (t 3.68) and +0.57 % (t 4.11) against -0.35 % on Thursday, already held as the late-week gain. Neither is proposed again.
- **F8:** The agitation split could not be measured on these short windows: the 365-day swing percentile came out missing for every case. Choppy agitated outside the profile has only 24 cases, all with negative means, too few to read.

## Ideas
- `058-02.g1_calm-range-bottom-keeps-falling` (from F1, F2, F5, F6): In a choppy, calm market, the nearer a coin's close sits to the bottom of its 20-day high-low range, the larger its fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
