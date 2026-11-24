---
line: 7.b inconclusive
backtest: 031-03_fading-volume-after-rise-reverses_1d
idea tested: 031-03_fading-volume-after-rise-reverses
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3528 USD
---
## Findings
- **F1:** The test's result is near zero and on the side against the idea. The slope of the 30-day excess return on the forecast is -0.0076 with t -0.46 over 57 regime cases. The short-bet cases (forecast at or below -2) gained on average, +6.1 % excess over 30 days (n=16, t 0.91), where the idea says they should fall.
- **F2:** After an unusually large 90-day rise, coins kept rising rather than reversing. On the 30-bar grid, the regime cases' mean excess return was +7.3 % over 10 days (n=57, t 2.30), +5.5 % over 20 days (t 1.44) and +4.7 % over 30 days (t 0.88). The bars outside the regime had -1.7 % over 10 days (n=469, t -2.67).
- **F3:** A deeper volume drop was followed by a higher excess 30-day return, not a lower one. Where the 14-day/90-day volume ratio could be computed inside the regime, the slope of the excess 30-day return on the ratio was -0.163 (t -2.55, n=16). The highest-ratio tercile had -12.8 % against -0.1 % for the lowest, so the fading-volume short was on the wrong side.
- **F4:** The regime's lean is mixed across coins and years, so 30 days of it cannot be told from 0:
- **F5:** Across all bars, a coin's recent return predicted the same direction over the next 10 days, on the non-overlapping 10-bar grid:

## Ideas
- `031-03.b1_short-horizon-continuation-after-moves` (from F2, F3, F5): The larger a coin's 20-day return, the more its price moves further in the same direction over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
