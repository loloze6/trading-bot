---
line: 7.b inconclusive
backtest: 022-02_combination-beats-best-single_1d
idea tested: 022-02_combination-beats-best-single
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3103 USD
---
## Findings
- **F1:** The combined score and the best single score are nearly the same number (correlation 0.84 over 3,254 cases, 0.80 to 0.88 in every coin), and both line up slightly against the coming 5-day return (correlation -0.032 and -0.034), so the test's difference between them is zero (mean 0.00025, t 0.21) rather than a weak edge for the combination.
- **F2:** The combination points the wrong way: cases where it is short end 0.46 % above the drift over 5 days (t 1.74, 1,739 cases) and cases where it is long end 0.53 % below it (t -1.99, 1,515 cases); its correlation with the return is negative in 5 of 6 coins and 6 of 8 years; its size is -0.23 % per case (-0.020 of a usual move), against 0.19 % for a buy and a sell.
- **F3:** What each signal predicts does not carry from one year to the next: the year-by-year 5-day correlation of closeness to the 90-day high has a -0.38 correlation with the previous year's, the 1-day return's -0.17, the 30-day volatility's 0.06. A weighting learned on the past 365 days is therefore re-weighting noise.
- **F4:** The 28-day return alone lines up with the coming return, more clearly at 10 days than at 5: correlation 0.059 (t 2.9, 2,432 cases) over 5 days, 0.086 (t 3.0, 1,199 cases) over 10 days, 0.026 (t 0.6, 514 cases) over 20 days. Over 5 days its top fifth ends 0.86 % above the drift (strength 0.073) and its bottom fifth 0.49 % below it, against a round trip of 0.19 %.
- **F5:** The 28-day return's effect depends on the period: its 5-day correlation is -0.22 in 2018, -0.12 in 2022 and 2023, and +0.12 and +0.19 in 2024 and 2025. Across coins it ranges from -0.05 (XMR) to +0.12 (ZEC). A single signal held fixed is steadier than the learned weights (year-to-year persistence +0.27), but it is not uniform.

## Ideas
- `022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days` (from F3, F4, F5): The higher a coin's 28-day return, the higher its return over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
