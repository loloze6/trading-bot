---
line: 7.d not profitable
backtest: 025-03_bounce-falling-versus-rising-regime_1d
idea tested: 025-03_bounce-falling-versus-rising-regime
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3815 USD
---
## Findings
- **F1:** The short side carries the book's whole loss. Short positions summed −5.08 of bar gain against +12.17 for longs, over 7235 and 8034 bars. Short trades averaged −3.11 % net with a 37.5 % win rate, against +3.93 % net and 48.2 % for longs (2319 and 2510 trades). Fees of 2.74 were then taken from a gross of 7.09.
- **F2:** Inside short cases, the fade is graded by the coin's own 30-day return (in usual daily moves), not by the rise:
- **F3:** Among long cases (90-day return positive), the 5-day excess return also rises with the 30-day return. It goes −1.43 % (t −2.45), +0.56 %, +1.33 % (t 2.14) and +0.90 % from lowest to highest quartile, 279 cases each. Both sides together say the 5 days after a sharp rise follow the 30-day trend, with a spread of about 1.5 to 3 % per case between extremes, well above the 0.19 % cost of a trade.
- **F4:** The rise's size grades the move only on the long side. Long-case gain grows from −0.79 % to +1.79 % (t 2.59) across rise quartiles. On the short side the smallest rises fade most: +1.54 % (t 2.86) in the smallest quartile against +0.46 % in the largest. The tested sizing therefore puts most short weight where the fade is weakest.
- **F5:** The fade depends on the year, which explains the leave-one-window-out failure:
- **F6:** Overall the idea's size barely covers its cost. Short cases lost the coin −0.41 % versus drift (t −1.58, 1319 cases), and long cases −0.07 % (t −0.21, 1510 cases). Per case the total move is 1.1 times the cost and the unusual move 0.9 times.

## Ideas
- `025-03_bounce-falling-versus-rising-regime.d1_bounce-fade-graded-by-depth` (from F1, F2, F4, F5): In one coin, the 5-day return after a one-day rise of several usual daily moves is lower when its 90-day return is negative than when its 90-day return is positive. In the negative case, the shortfall grows the deeper its 30-day return lies below zero in usual daily moves, rather than with the size of the rise.
- `025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend` (from F2, F3, F6): In one coin, the 5-day return after a one-day rise of several usual daily moves is higher the higher its 30-day return, measured in usual daily moves.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
