---
line: 7.b inconclusive
backtest: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends_4h
idea tested: 027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3917 USD
---
## Findings
- **F1:** The main measure is on the predicted side but well short of the bar, and a few large winners carry it: the mean unusual 14-day return is +4.42 % with t 1.26 over 90 cases, while the median is only +1.07 % and 56.7 % of cases are positive. Dropping the top and bottom 5 % of cases cuts the mean to +1.63 % (t 1.05, 80 cases). The same skew shows in ZEC (mean +9.6 %, median −1.2 %, 15 cases) and in 2025 (mean +26.7 %, median +0.2 %, 9 cases).
- **F2:** The effect is strongest early and fades by the plan's horizon. On the same bets, the unusual return is +6.6 % over 3 days (t 3.54, 97 cases, strength 0.77), +5.9 % over 7 days (t 2.72, 96 cases, strength 0.43) and +4.4 % over 14 days (t 1.26, 90 cases, strength 0.20). Over 14 days the coin's usual move of 17.66 % drowns the rebound.
- **F3:** One year pulls the result down: the 6 cases of 2018 averaged −20.2 % (t −2.94, 17 % positive). Without 2018, the 14-day mean is +6.2 % (t 1.69, 84 cases) and the 7-day mean is +6.8 % (t 2.98, 90 cases).
- **F4:** The supporting check could not pass as configured: all 98 bet bars sit at the forecast cap of 20 (standard deviation 0), so 0 cases are above the median. The cube-and-cap transform saturates every panic, and the test cannot see any grading.
- **F5:** The idea's grading by fall depth is not supported. Over 14 days the deeper half of falls returned −1.55 % (25 cases) against +3.82 % for the shallower half (33 cases); over 7 days, +3.39 % against +7.87 %. Across all panics with a fall, the deepest third returned −0.47 % over 14 days against +1.42 % for the shallowest.
- **F6:** The 90-day-rise filter does not isolate a larger effect. On my recomputed panics, those with a positive 90-day return gave +5.3 % over 14 days (t 1.43, 13 cases). Those with a non-positive one gave +4.2 % (t 1.69, 107 cases).
- **F7:** Cost is not the obstacle; too few cases is:

## Ideas
- `027-02_panic-fall-depth-rebound.d1_panic-rebound-in-uptrends.b1_panic-rebound-more-coins` (from F1, F3, F7): Among 24-hour stretches where a coin's range is several times its 30-day average, the deeper the coin's fall over that stretch, the higher its return over the next 14 days, only while the coin's 90-day return is positive, and the more so the larger that 90-day rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
