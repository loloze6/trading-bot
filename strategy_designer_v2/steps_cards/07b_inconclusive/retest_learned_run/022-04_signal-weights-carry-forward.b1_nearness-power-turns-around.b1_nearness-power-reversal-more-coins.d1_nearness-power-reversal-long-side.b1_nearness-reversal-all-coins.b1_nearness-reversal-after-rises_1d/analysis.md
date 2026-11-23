---
line: 7.b inconclusive
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins.b1_nearness-reversal-after-rises_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins.b1_nearness-reversal-after-rises
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4031 USD
---
## Findings
- **F1:** The test's main measure is on the predicted side but just short of the bar: the pooled slope of the 5-day return minus drift on the forecast is +0.000627 with t 1.99 over 4,875 grid cases (1,127 with a forecast above 0). The test already used every coin and all four folds, so no more data is available.
- **F2:** The forecast's own grading carries almost none of that slope. Among the 1,127 active cases the rank correlation of forecast with 5-day excess return is −0.014 (p 0.64). The forecast quartiles are not monotonic (+0.46 %, +1.71 %, +0.93 %, +0.54 %). Within the trending regime the slope on the forecast is +0.000326 with t 0.89 over 2,444 cases.
- **F3:** The effect rests on one year. 2021 alone gives a slope t of 3.67 over 474 cases with an active mean of +5.35 %. Without 2021 the pooled slope is +0.000278 with t 0.88 over 4,401 cases, and the active mean is +0.45 % with t 1.43 over 1,021 cases. 2018, 2022, 2023 and 2025 have negative slopes, and only 10 of 16 coins have a positive slope, none with t above 1.6.
- **F4:** What separates good from bad active cases is the size of the 30-day rise, not the reversal reading:
- **F5:** The same grading by the 30-day rise shows in trending bars where the forecast is 0:
- **F6:** Active cases beat trending cases with a zero forecast by only +0.88 % (Welch t 1.89). Across horizons the slope t is 2.61, 1.78, 1.99, 1.65 and 2.77 at 1, 3, 5, 10 and 20 days, so no horizon isolates the reversal reading clearly.

## Ideas
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins.b1_nearness-reversal-after-rises.b1_thirty-day-rise-carries-forward` (from F4, F5, F2, F3): Among coins whose 30-day return is positive, the larger the coin's 30-day return, the higher its return over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
