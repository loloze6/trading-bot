---
line: 7.g patterns
backtest: 060-01_volume-shrink-fall-continues_1d
idea tested: 060-01_volume-shrink-fall-continues
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4445 USD
---
## Findings
- **F1:** In the falling profile, the drop after volume shrinkage sits almost entirely in the strongest shrink. The lowest quintile of the 30-day log volume ratio (mean −0.76) is followed by an excess 5-day return of −3.6 % (day-clustered t −1.83, 81 non-overlapping cases). The other quintiles show −0.9 %, −0.3 %, +1.8 % and +0.5 %, none with |t| above 1.4. This makes the idea's average size small: an unusual move of +0.72 % with t 1.46 and a total move of +0.13 %, against a cost of 0.19 % per trade.
- **F2:** In rising markets (60-day return above +10 %), volume shrinkage is followed by the opposite of the tested effect: the coin rises more.
- **F3:** The rising-market effect shows in both agitation states, at each end of the volume ratio.
- **F4:** Read across both trends, volume shrinkage goes with continuation of the coin's 60-day direction. The trend-signed excess 5-day return on the volume ratio has a slope of −0.029 (t −1.70, 719 cases). Over all bars, with no trend split, the slope is −0.0005 (t −0.03, 846 cases): the effect only appears once it is signed by the trend.
- **F5:** Inside the falling profile, the shrinkage effect leans on calm markets.
- **F6:** The book's gain depends on a few windows and a few days.
- **F7:** No other angle stood out against the many looked at. None of these reached |t| ≥ 2 in any quintile:

## Ideas
- `060-01.g2_calm-fall-volume-dry-up` (from F1, F5): In a falling, calm market, the more a coin's trading volume over the past 30 days has shrunk against the 30 days before, the larger its fall over the next 5 days.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `060-01.g1_rising-volume-dry-up-continuation` (from F2, F3, F4): In a rising market, the more a coin's trading volume over the past 30 days has shrunk against the 30 days before, the larger its rise over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
