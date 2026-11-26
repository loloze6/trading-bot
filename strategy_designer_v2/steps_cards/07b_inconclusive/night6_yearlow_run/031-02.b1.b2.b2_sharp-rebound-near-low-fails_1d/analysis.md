---
line: 7.b inconclusive
backtest: 031-02.b1.b2.b2_sharp-rebound-near-low-fails_1d
idea tested: 031-02.b1.b2.b2_sharp-rebound-near-low-fails
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4238 USD
---
## Findings
- **F1:** The tested effect is on the predicted side but too small to tell from zero, and the 60-day return does not grade it: inside the regime the slope of the 20-day drift-adjusted return on the 60-day return is -0.023 (t -0.64, 417 cases, 65 days); the mean 20-day unusual move by 60-day-return quintile, lowest to highest, is -0.2 %, -4.9 %, -4.0 %, +1.3 % and -4.7 %, so the sharpest rebounds do no worse than the deepest falls.
- **F2:** Restricted to the short side the test was meant for (60-day return above 0), the slope is still only -0.031 (t -1.02, 143 cases, 41 days), and the mean unusual move is about the same for rebounding coins (-2.2 %, 143 cases) as for falling ones (-2.7 %, 274 cases).
- **F3:** The pooled slope is a cancellation of years with opposite signs: 2019 is +0.45 (t 5.96, 8 days), 2020 is -0.64 (t -6.77, 6 days), 2022 is -0.36 (t -4.32, 11 days) and 2025 is +0.23 (t 1.01, 8 days), so no single period carries the effect.
- **F4:** A different horizon does not find the effect either: the in-regime slope on the 60-day return is +0.026 (t 1.27) at 5 days, -0.004 (t -0.18) at 10, -0.023 (t -0.65) at 20 and +0.012 (t 0.23) at 40, and the slope on the 20-day return has |t| below 1 at every horizon.
- **F5:** Being in the regime predicts nothing by itself: the mean 20-day unusual move is -0.4 % in the regime (872 cases, day-clustered t -0.18) against +0.5 % outside it (684 cases); outside the regime the 60-day return acts as momentum, with the top quintile at +9.2 % and the bottom at -6.5 %.
- **F6:** Closes below the prior lowest close are followed by a bounce rather than a further leg down: the mean unusual move is +9.7 % over 20 days and +12.3 % over 10 days (44 cases, standard deviation 27.9 %, plain t about 2.3), against -1.4 % and -0.3 % on the other grid bars (702 cases). Caveat: the low here was measured within the window, over up to 365 days.
- **F7:** The idea's size is about zero: the unusual move is -1.07 % per case (t -0.46, 271 days, strength -0.002). The -4.51 % total move is almost all the coins' normal drift (-3.44 % in the short's direction). The test already used every coin and every fold, so no further data exists to rerun it on.

## Ideas
- `031-02.b1.b2.b2.b1_yearly-low-break-bounces-back` (from F6, F5, F1): The further a coin's daily close has fallen below its lowest close of the previous 365 days, the more it rises over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
