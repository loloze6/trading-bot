---
line: 7.b inconclusive
backtest: 024-03_uprun-volume-fade-depth-giveback.d1_up-run-give-back-in-downtrends_4h
idea tested: 024-03_uprun-volume-fade-depth-giveback.d1_up-run-give-back-in-downtrends
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3841 USD
---
## Findings
- **F1:** The result is unclear for a mechanical reason, not a weak effect. The main measure is on the predicted side, +0.55 % unusual move over 18 bars with t 3.74 over 2891 cases. But the cube-and-pivot transform saturates the forecast: 61 % of cases sit at -20 and the median |forecast| is 20.00, so the above-median group was empty (0 against 2891 cases) and the supporting check could not be computed.
- **F2:** Inside the cases the grading the idea claims is missing, and for the strongest situations it is reversed.
- **F3:** The situation is rarely a run. The streak length is 1 bar at the median of three of the four length quartiles and 2 bars in the top one. The cases are mostly "one 4h up-close while below the 30-day average", not an extended streak.
- **F4:** The move builds slowly rather than as a quick give-back.
- **F5:** The effect sits mostly in the early years.
- **F6:** Volume works against the brief's claim. Among the 606 cases with streaks of 2 or more bars:
- **F7:** The effect is broad but faint across coins. All six coins are positive, from +0.29 % (XMR) to +0.81 % (ETH), and only ETH reaches t ≥ 2 (t 2.49).
- **F8:** The idea's size does not cover a trade. The total move per case is +0.14 % against a 0.19 % cost (0.7 times the cost), and the book's Sharpe is -0.09. A larger move per case would be needed for any book on it to pay, whatever the holding or the sizing.

## Ideas
- `024-03_uprun-volume-fade-depth-giveback.d1_up-run-give-back-in-downtrends.b1_rising-volume-relief-rally-fades` (from F6, F2, F3, F4): A four-hour up-close made on volume rising across the streak, while the coin's price is below its average of the past 30 days, is followed by a fall relative to the coin's usual drift over the next three days; the larger the rise in volume across the streak, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
