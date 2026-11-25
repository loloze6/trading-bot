---
line: 7.g patterns
backtest: 032-01_choppy-upside-break-fades_1d
idea tested: 032-01_choppy-upside-break-fades
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3926 USD
---
## Findings
- **F1:** Over 5 days, the higher a coin's close sits in its prior 20-day high-low range, the more it rises beyond its normal drift: the slope of strength on range position is +0.40 of a usual move per unit of range (OLS t 4.77, 1422 non-overlapping cases). The same slope holds at 3 days (+0.23, t 3.64, 2358 cases) and at 10 days (+0.38, t 3.19, 702 cases).
- **F2:** The pattern is graded through the range at 5 days. The unusual move is -2.37 % in the bottom quarter (t -1.56, 312 cases, 123 days), -0.97 % in the second quarter, +0.73 % in the third, +1.75 % in the top quarter (t 1.63, 263 cases, 108 days) and +5.01 % above the range (t 2.30, 66 cases, 39 days).
- **F3:** The top quarter minus the bottom quarter is positive on all 6 coins, from +0.23 (XMR) to +0.74 (XRP) of a usual move, and in 9 of the 12 windows shown. The pattern is not carried by one coin or period.
- **F4:** Closes above the prior 20-day high keep rising instead of failing, which is the opposite of the tested idea's side. Over 5 days they gain +5.10 % above drift (t 2.34, 66 cases, 39 days); over 10 days they gain +11.75 % (t 2.97, 33 cases, 18 days).
- **F5:** Those upward breaks are not graded by their overshoot. The unusual move by size tercile is +6.30 %, +2.33 % and +6.67 % (t 2.52, 1.54, 1.29), matching the verdict's slope of -0.009 on the overshoot.
- **F6:** In a choppy market, the few upward breaks seen also continue: +10.66 % over 5 days (t 4.03, but only 6 cases). Closes in the bottom quarter of the range in a choppy market fall -9.44 % (t -1.85, 22 cases, 17 days).
- **F7:** Other angles show no pattern beyond what multiple testing would produce: weekday (|t| ≤ 1.33), the 20-day vs 60-day volatility ratio (|t| ≤ 0.44), range width (|t| ≤ 0.78) and the 60-day profile alone (|t| ≤ 1.04).
- **F8:** Against the cost of a trade (0.19 %), the size of the range-position effect is large. Top quarter minus bottom quarter is about 4 % of price per 5 days (0.23 to 0.74 of a usual move of 9 to 16 %), more than 20 times the cost.

## Ideas
- `032-01.g2_choppy-upside-breaks-continue` (from F4, F6): In a choppy market, when a coin's daily close is above the highest high of its prior 20 days, its price rises over the next 10 days, and the further the close sits above that high, the larger the rise.

## Discoveries (off the brief's theme: each becomes a brief, `discoveries/`)
- `032-01.g1_range-position-predicts-continuation` (from F1, F2, F3, F8): The higher a coin's daily close sits within its range of the prior 20 days (from its lowest low to its highest high, a close beyond the high counting as highest), the more the coin rises over the next 5 days, and the lower it sits, the more it falls.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
