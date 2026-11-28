---
line: 7.c no effect
backtest: 086-01.c2_heavy-up-day-extends-rebound_1d
idea tested: 086-01.c2_heavy-up-day-extends-rebound
step 5: no effect
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4041 USD
---
## Findings
- **F1:** The tested situation shows no effect. Falling-calm up days on volume at least 1.5x the 20-day average lost against drift at every horizon: 1.5-2.5x gave −3.0 % over 5 days (t −1.96, 29 cases) and −3.6 % over 10 days, and above 2.5x gave −1.8 % and −1.2 % (16 cases). The Spearman of volume ratio against the move after up days was negative at every horizon (−0.08 at 5 days, −0.03 at 10 days).
- **F2:** Inside the plan's own condition, a positive 5-day return before the day, the market did the opposite of the brief. Up days on light volume (under 1x the 20-day average) rose +2.9 % against drift over the next 5 days (t 2.11 with one day's cases taken together, 47 cases, 41 days). Heavier up days (1x or more) rose only +1.1 % (t 0.67, 31 cases).
- **F3:** That light-volume follow-through is graded the wrong way for the brief. In a positive 5-day rebound, the 5-day unusual move after an up day falls step by step as volume rises:
- **F4:** Without the rebound condition, falling-calm up days lose. With a negative prior 5-day return, they lost at every volume level; at 1.5-2.5x the loss was −6.6 % over 10 days (t −2.19, 20 cases). The plan's rebound condition is what separates the paying from the losing up days, not the volume.
- **F5:** Across all falling-calm days, the move over the next days grows with the strength of the 5-day return, scaled by volatility. The Spearman is 0.20 at 5 days and 0.25 at 10 days. The weakest fifth lost −4.0 % over 5 days (t −2.71, 58 cases) and the strongest fifth gained +1.3 % (t 0.87, 61 cases). On the long side the gain is small; most of the grading comes from avoiding the weakest rebounds.
- **F6:** The rebound follow-through is not stable across periods or coins. After a positive 5-day return, the 5-day move was:

## Ideas
- `086-01.c2.c1_quiet-up-day-extends-rebound` (from F2, F3, F1): In a falling, calm market, an up day that extends a positive 5-day return is followed by a further rise over the next 5 days, and the lighter that day's volume against its 20-day average, the larger the rise.
- `086-01.c2.c2_strong-rebound-up-day-continues` (from F5, F4, F6): In a falling, calm market, an up day is followed by a rise over the next 10 days that is larger the stronger the coin's 5-day return ending that day, measured against its recent daily swings.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
