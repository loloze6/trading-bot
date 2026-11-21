---
line: 7.g patterns
backtest: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins_1d
idea tested: 020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4375 USD
---
## Findings
- **F1:** The day's range (high minus low over the close) relative to its own 30-day average predicts the coin's next days, upward. In a pooled regression of the standardised forward excess return on its per-coin rank, holding the 20-day volatility rank and the forecast rank fixed, the slope is 0.21 of a usual move at t 7.4 over 2 days (15,028 non-overlapping cases), 0.21 at t 4.8 over 5 days (5,928 cases), and 0.11 at t 1.8 over 10 days (2,928 cases).
- **F2:** The range effect is graded and large against the cost of a trade. Over 5 days, the winsorised excess return by quintile of relative range runs -1.21 %, -1.43 %, -0.47 %, +0.43 % and +1.06 % (about 1,245 cases each), so the widest-range fifth sits about 0.09 of the 12 % usual move above drift, near 5 times the 0.22 % round trip.
- **F3:** The range effect holds across coins and periods: the 5-day slope is positive in 17 of 19 coins (t above 2 in ADA, AVAX, INJ, LINK) and in 18 of 24 windows.
- **F4:** The range effect does not depend on the day's direction. In the widest-range quintile, the 5-day excess return is +0.97 % after down days (t 2.4, 663 cases) and +2.11 % after up days (t 2.4, 583 cases). In the second-narrowest quintile it is -1.09 % (t -2.7) and -1.83 % (t -4.4).
- **F5:** Days with a wide raw range rise too. The top quintile of the range rank is followed by a +1.37 % 5-day excess return (t 2.9, 1,426 cases), against -0.54 % for the bottom quintile (t -2.2); the forecast's own rank gives a slope t of 3.5, in line with the confirmed short idea.
- **F6:** The short book fights the coins' drift and loses. Its 12,134 short trades last 11.5 days on average and earn +0.10 % gross but -0.001 % net. The book's mean daily return is -0.040 %, against +0.142 % for the coins. The idea's unusual move of +0.29 % per case is outweighed by a -0.75 % drift against it.
- **F7:** Weekday and trend angles do not stand out against the number of angles tried:

## Ideas
- `020-02_support-retest-bounces-up.c1_broken-support-keeps-falling.b1_broken-support-more-coins.g1_wide-range-day-precedes-rise` (from F1, F2, F3, F4, F5): When a coin's daily range is wide compared with its own ranges of the past 30 days, the coin tends to rise over the next 5 days, more so the wider that day's range is relative to its 30-day average, whether the day closed up or down.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
