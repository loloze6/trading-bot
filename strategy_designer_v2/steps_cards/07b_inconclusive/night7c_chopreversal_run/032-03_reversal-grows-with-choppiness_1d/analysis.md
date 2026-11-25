---
line: 7.b inconclusive
backtest: 032-03_reversal-grows-with-choppiness_1d
idea tested: 032-03_reversal-grows-with-choppiness
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3429 USD
---
## Findings
- **F1:** Step 5's main slope is on the side opposite to the idea (-0.000827, day-clustered t -1.9988 over 2443 cases on 441 days), and in folds B and C the same forecast regression is also negative (slope -0.001075, t -2.78, 1219 grid cases), so larger reversal forecasts are followed by moves against them, meaning the 7-day move continues.
- **F2:** Choppiness amplifies continuation, not reversal: the slope of the next-7-day excess return on minus the scaled 7-day move is +0.0027 (t 0.34) in the calmest quartile of 1 − ER(30), against -0.021 (t -2.25), -0.032 (t -3.02) and -0.029 (t -2.43) in the three choppier quartiles; in a joint fit the scaled-move × choppiness term is +0.076 at 7 days and +0.153 at 14 days.
- **F3:** The continuation sits on the rising side: after a 7-day rise, the choppiness-weighted scaled move predicts the next-7-day excess return with slope +0.051 (day-clustered t 2.32, 437 cases on 107 days), but after a 7-day fall the slope is +0.004 (t 0.15, 422 cases); the top quintile of the weighted move is followed by +3.45 % excess (0.40 of a usual move).
- **F4:** Continuation is strongest when the coin's 30-day swings are low for that coin: the slope on minus the scaled move is -0.029 (t -4.15, 288 cases) in each coin's lowest volatility tercile, -0.012 (t -1.57) in the middle and +0.005 (t 0.55) in the highest.
- **F5:** The pattern holds at 14 days but fades at 3: the forecast slope is -0.0013 (t -2.24, 1147 cases) at 14 days and +0.00025 (t 1.07) at 3 days; in the top choppiness quartile the 14-day slope on minus the scaled move is -0.073 (t -3.57).
- **F6:** Across windows the effect is mixed: the forecast slope is negative in 7 of 12 windows and strongest in w13, w16 and w18 (t -2.49, -2.78, -3.39), while w12 is the most positive (t +1.86). Every coin is negative but none individually beyond t -1.67, so the pooled t only reaches about -2.

## Ideas
- `032-03.b1_choppy-weekly-rise-continues` (from F1, F2, F3, F5): After a coin's 7-day rise, scaled by its typical daily swing over the past 30 days, the coin keeps rising over the next 7 days, and the more so the larger that scaled rise and the more agitated and trendless the past 30 days have been.
- `032-03.b2_quiet-coin-weekly-move-continues` (from F1, F4, F6): A coin's 7-day move, scaled by its typical daily swing over the past 30 days, continues in the same direction over the next 7 days, the more so the larger the scaled move, only while the coin's daily swings over the past 30 days are small compared with its own swings over the past year.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
