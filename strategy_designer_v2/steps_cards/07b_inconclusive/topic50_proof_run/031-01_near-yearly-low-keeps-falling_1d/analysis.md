---
line: 7.b inconclusive
backtest: 031-01_near-yearly-low-keeps-falling_1d
idea tested: 031-01_near-yearly-low-keeps-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3253 USD
---
## Findings
- **F1:** The test's slope is on the side the idea predicts but short of the bar: drift-adjusted 20-day short gain on |forecast| gives slope 0.0024 with t 1.70 over 806 cases. In the folds shown, the 5-, 10- and 20-day slopes are all positive with t 1.61, 1.88 and 1.75 (1,617, 801 and 393 cases), so a nearby horizon does not sharpen it.
- **F2:** The pooled effect is carried by the top fifth only. Those cases nearest the low have a mean short gain of +5.6 % (t 2.38, 79 cases), while quintiles 1 to 4 sit between -4.0 % and +0.5 % with no gradient. Top fifth minus the rest is +7.0 % (Welch t 2.52).
- **F3:** The top-fifth cases cluster in a few windows. 53 of 79 fall in w7 and w14, with mean short gains of +12.0 % and +10.0 %. Positive windows are 5 of 9 (56 %), and w16 shows -15.5 %.
- **F4:** Within one coin and window the sign reverses: the slope of the window-demeaned short gain on |forecast| is -0.0036 (t -2.29, 393 cases), and the top fifth minus the rest is -3.7 % (t -1.82). The pooled slope therefore comes from whole falling windows, where closes sit near the low and the market keeps falling, not from closeness to the low inside a period.
- **F5:** The idea's size is against it and cannot be told from zero: an unusual move of -1.41 % per case (t -0.75, 243 days, strength -0.063 of the usual 21.24 % move). Closes within 2 % of the yearly low show a short gain of -1.2 % (t -0.50, 125 cases), so at the low itself no extra fall shows.
- **F6:** The effect is not tied to one coin. Per-coin 20-day slopes are positive in 5 of 6 coins, with t from 0.52 to 1.21 (58 to 69 cases each), and XRP shows t -0.15. The top fifth's gain is positive in all six coins (+2.0 % to +9.1 %). The test is short of cases per coin rather than showing the effect in one place, and folds A and D hold 13 more coins it did not use.

## Ideas
- `031-01.b1_near-yearly-low-more-coins` (from F1, F2, F6): The closer a coin's daily close is to its lowest close of the past 365 days, the more it falls over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
