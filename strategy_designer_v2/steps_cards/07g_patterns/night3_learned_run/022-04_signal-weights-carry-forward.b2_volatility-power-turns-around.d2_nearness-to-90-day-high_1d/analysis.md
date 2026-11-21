---
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d2_nearness-to-90-day-high_1d
idea tested: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d2_nearness-to-90-day-high
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3772 USD
---
## Findings
- **F1:** On the non-overlapping 5-day grid, a coin's 1-day return predicts its next-5-day return beyond drift when the coin's 20-day volatility is in its lower two thirds, and reverses in its upper third. The slope of the standardised 5-day move on the standardised 1-day return is 0.075 (t 3.14, 1043 cases) in the calm third, 0.081 (t 2.75, 1044) in the middle third and -0.042 (t -1.17, 1044) in the high third. Scaling the 1-day return by the 20-day volatility gives the same result (t 3.10, 2.79, -0.84).
- **F2:** In the calm and middle volatility thirds the 1-day-return effect is concentrated in the largest up days and is large next to cost. The top fifth of 1-day returns is followed by +2.29 % over 5 days beyond drift (t 3.88, 420 cases), about 12 times the 0.19 % round trip. The second-lowest fifth is followed by -0.93 % (t -2.16).
- **F3:** The calm-and-middle 1-day continuation has a positive slope on all 6 coins (0.047 to 0.150; XRP t 3.38, XMR 1.69, ETH 1.45). It is positive in 6 of 8 years (2019 t 4.06, 2021 t 2.42, 2023 t 2.18) and negative in 2018 (t -2.24) and 2025 (t -0.79). It is not a one-coin artefact, but it is not stable in every year.
- **F4:** The tested nearness forecast's edge sits on its long side. On grid cases with a positive forecast the slope is 0.046 (t 1.85, 1727 cases), with a negative forecast 0.027 (t 1.13, 1692 cases); the pooled slope is 0.036 (t 2.10). The top forecast fifth carries the gain (+1.05 % over 5 days, t 2.13), while the bottom fifth is only -0.14 % (t -0.34).
- **F5:** The book is short 47 % of its bars, and that side costs it. Long bars earn +0.038 % per bar, of which 0.018 % is market rise. Short bars lose -0.012 % per bar, mostly the -0.016 % of drift given up by shorting a rising coin. The book's mean daily return is 0.011 % against holding's 0.118 %, and it beats holding in 42 % of windows.
- **F6:** By year the forecast's slope is unstable: positive in 2019 (t 2.89), 2020 (t 1.76) and 2021 (t 1.36), and negative in 2018 (t -1.51), 2022, 2023 and 2024 (t -0.70 to -1.32). The nearness edge is concentrated in the 2019-2021 stretch.
- **F7:** Grid cases starting on Monday or Tuesday are followed by about +1.4 % beyond drift over 5 days. This holds in both the 2018-2021 half (t 2.63, 492 cases) and the 2022-2025 half (t 3.05, 481 cases); other start days give about -0.56 % in each half. It is a calendar condition, not a graded situation, so it supports no idea here.
- **F8:** Several other single signals add nothing on the 5-day grid. Neither the 20-day volatility level (slope 0.002, t 0.09) nor the 5-day return (t 0.14) predicts the 5-day move beyond drift. Neither does the 60-day nearness to high (t 0.62) or to low (t 0.84). About 40 slices were examined in all, so only F1 to F3 clear a raised bar of about t 3.

## Ideas
- `022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d2_nearness-to-90-day-high.g1_calm-market-daily-continuation` (from F1, F2, F3): The larger a coin's 1-day return against its own 20-day volatility, the higher its return over the next 5 days, while its 20-day volatility is low or middling against its own past.
- `022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d2_nearness-to-90-day-high.g2_long-only-nearness-to-highs` (from F4, F5): The closer a coin's daily close sits to its highest close of the past 90 days, the higher its return over the next 5 days, with the rise growing as nearness grows on the long side only.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
