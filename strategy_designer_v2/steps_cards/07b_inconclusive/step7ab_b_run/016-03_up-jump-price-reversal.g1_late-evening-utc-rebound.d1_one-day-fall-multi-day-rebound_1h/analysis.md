---
line: 7.b inconclusive
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_one-day-fall-multi-day-rebound_1h
idea tested: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_one-day-fall-multi-day-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3199 USD
---
## Findings
- **F1:** The test's slope is on the side the idea predicts but falls short of the bar (slope +0.00031, t 1.92, 5,683 grid cases). Half of those cases (2,873) have a forecast of 0 after a 24-hour rise. On the 2,810 cases with a positive forecast alone, the slope is +0.00069 with t 2.90.
- **F2:** The forecast scales the fall against the coin's last 60 hours, and that measures the idea poorly. Measured as the raw depth of the 24-hour fall, the same 72-hour excess return has a slope of 0.263 with t 6.04 over 2,720 falls. Scaled by the coin's 30-day hourly volatility, the slope is 0.0105 with t 4.32 over 2,516 falls.
- **F3:** The effect sits in the deepest falls only. Falls beyond -5 % in 24 hours (548 cases) are followed by a 72-hour excess return of +1.54 %, about 8 times the 0.19 % cost of a trade. The four shallower fall quintiles are all negative (-0.16 % to -0.85 %). The deepest tenth of all cases earns +1.49 % (t 3.38, 556 cases).
- **F4:** The rebound is a 1-to-3-day effect that fades by a week. The deepest tenth earns +1.06 % over 24 hours (t 3.80) and +1.49 % over 72 hours (t 3.38). Over 168 hours it earns +1.19 % with t only 1.68. The test's own slope has t 3.93 at 24 hours and t 0.59 at 168 hours.
- **F5:** The effect is stronger when the coin's 30-day return is positive. There the raw-fall slope is 0.572 (t 5.84, 950 falls), and the deepest tenth earns +3.00 % over 72 hours (t 3.08, 163 cases). When the 30-day return is negative, the deepest tenth earns +0.98 % (t 1.80, 233 cases).
- **F6:** The effect is mixed across years and drowned in some of them:

## Ideas
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_one-day-fall-multi-day-rebound.b1_one-day-fall-more-coins` (from F1, F6): The more a coin has fallen over its last 24 hours, the more it rises over the next 3 days.
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_one-day-fall-multi-day-rebound.b2_deep-fall-rebound-in-uptrend` (from F2, F3, F4, F5): The larger a coin's fall over its last 24 hours, measured against its typical daily move over the last 30 days, the more it rises over the next 3 days, more so while its 30-day return is positive.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
