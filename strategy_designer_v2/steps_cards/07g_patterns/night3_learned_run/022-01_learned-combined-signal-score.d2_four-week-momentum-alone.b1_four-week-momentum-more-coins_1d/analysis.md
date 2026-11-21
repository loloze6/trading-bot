---
line: 7.g patterns
backtest: 022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins_1d
idea tested: 022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4947 USD
---
## Findings
- **F1:** Over the next 20 days, a coin's one-day return points the other way, and strongly. The slope of the 20-day excess return (in units of the coin's usual 20-day move) on the ranked one-day return is -0.157 per standard deviation (t -6.1, 1456 non-overlapping cases). It holds when returns are clipped (t -6.3) and when the day's return is scaled by its 20-day volatility (t -5.4).
- **F2:** The book's gain is all on the long side. Long bars earned +0.21 % per bar (17987 bars, sum 38.0), short bars -0.0085 % (18868 bars, sum -1.6). Shorts paid only in falling years (2018 +0.14 %, 2022 +0.11 % per bar) and lost in 2020, 2023 and 2024 (-0.11 % to -0.14 % per bar).
- **F3:** The deepest falls are not where the losses continue, which fits F1. In the forecast's quintiles:
- **F4:** The 28-day momentum effect is larger over 10 days than over the tested 5.
- **F5:** Momentum works in calm markets and fades in volatile ones, but the pattern is not robust enough to act on.
- **F6:** The book's largest days are followed by gains whichever way they went, so they mark volatility, not direction.
- **F7:** Other angles looked at showed nothing to count.

## Ideas
- `022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins.g1_deep-down-day-weeks-long-rebound` (from F1, F2, F3): The larger a coin's fall on its last day, the higher its return over the next 20 days, the gain growing with the depth of the day's fall.
- `022-01_learned-combined-signal-score.d2_four-week-momentum-alone.b1_four-week-momentum-more-coins.g2_four-week-momentum-two-week-horizon` (from F4): The higher a coin's 28-day return, the higher its return over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
