---
line: 7.b inconclusive
backtest: 002-04_price-cross-below-long-sma_1d
idea tested: 002-04_price-cross-below-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3069 USD
---
## Findings
- **F1:** Below the SMA200 the coin's excess 10-day return is only slightly negative, mean -0.0034 (t -0.70, n 841 non-overlapping blocks), against +0.0037 (t 0.61, n 816) above it, and the plan's allocation × excess product stays near zero at every horizon (10 days: -0.00027, t -0.23; 3 to 40 days: |t| ≤ 0.41). The effect is weak overall.
- **F2:** The effect is mixed across periods and cancels out. Below the SMA200 the excess 10-day return is clearly negative in the bear years: 2018 -0.0395 (t -2.41, n 137), 2019 -0.0158 (t -1.87) and 2022 -0.0250 (t -2.64, n 191). It is clearly positive in the recovery years: 2020 +0.0493 (t 3.05, n 73), 2021 +0.0416 (t 1.75) and 2023 +0.0190 (t 1.67).
- **F3:** The test's grading runs against the effect. The deepest forecast quartile is followed by a rise, excess +0.0076 (t 0.71, n 211), while the shallow quartile falls, -0.0080 (t -0.84). The deepest distance bin (-72% to -36.5%) averages -0.0001 against -0.0068 for the shallowest bin. The slope of excess return on allocation is -0.0126, so the clipped standardised forecast puts its largest shorts where falls stop.
- **F4:** The fall shows where the 200-day average itself is falling fastest. The quartile with the steepest 20-day decline of the SMA200 has excess 10-day return -0.0175 (t -1.66, n 173, 54% of blocks down), against -0.0012 (t -0.11) for the quartile where it rises most. Over 20 days the same split gives -0.0159 against +0.0153.
- **F5:** The coin's recent path splits the outcome. Below the SMA200, a high 30-day return (top quartile) is followed by excess -0.0159 over 10 days (t -1.55, n 154). The lowest 30-day return is followed by +0.0064 over 10 days and +0.0479 over 20 days (t 1.58, n 67): bounces under a falling average fail, and sharp drops rebound.
- **F6:** Time spent below the average is mixed too. Excess 10-day return is -0.0185 (t -1.71) in the first 10 days below, +0.0191 (t 1.93) at 11–30 days and -0.0167 (t -1.81) after 60 days. This adds to the mixed picture rather than giving one clean side.

## Ideas
- `002-04_price-cross-below-long-sma.b1_falling-average-downside-persistence` (from F4, F2, F1): While the coin's close is below its 200-day simple moving average, it keeps falling beyond its usual drift over the next 10 days, the more so the faster that 200-day average has itself declined over the past 20 days.
- `002-04_price-cross-below-long-sma.b2_failed-rally-below-average` (from F5, F3): While the coin's close is below its 200-day simple moving average, it falls beyond its usual drift over the next 10 days, the more so the higher its 30-day return has been.
- `002-04_price-cross-below-long-sma.b3_deep-drop-rebound` (from F3, F5): The further a coin's close sits below its 200-day simple moving average and the more it has fallen over the past 30 days, the more it rises beyond its usual drift over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
