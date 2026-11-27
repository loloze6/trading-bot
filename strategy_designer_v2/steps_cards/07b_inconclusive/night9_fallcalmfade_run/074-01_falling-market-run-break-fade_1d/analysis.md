---
line: 7.b inconclusive
backtest: 074-01_falling-market-run-break-fade_1d
idea tested: 074-01_falling-market-run-break-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3464 USD
---
## Findings
- **F1:** Step 5's main measure is on the predicted side and clear (+0.92 % per case, day-clustered t 3.54, 834 cases on 426 days), but run length does not grade the effect. In folds B and C, falling-regime cases after runs of 2 average +1.79 % (t 3.21, 230 cases), runs of 3 +0.17 % (t 0.27, 121), runs of 4 +1.49 % (t 1.72, 39) and runs of 5+ +2.40 % (t 2.93, 53), with a Spearman of run length against the short-side move of -0.02; this is why the supporting check failed (-0.47 %).
- **F2:** How deep the run fell does grade the effect. Measured against the coin's 30-day daily swing, the depth quartiles from deepest to shallowest give +2.64 % (t 3.04, 93 cases, 48 days), +1.31 % (t 2.48), +1.20 % (t 1.39) and +0.15 % (t 0.22), with a Spearman of -0.22 (deeper run, larger next-day fall); the raw run return gives the same order, from +2.64 % (t 3.97) in the deepest quartile to +1.23 % in the shallowest.
- **F3:** Depth grades the effect within run lengths too. For runs of 3 or more, the deepest raw-depth quartile gives +2.66 % (t 3.91, 85 cases) and the shallowest -0.46 % (t -0.91, 27 cases). For runs of 2, the two deeper quartiles give +2.58 % and +3.65 %, against -0.32 % and +1.77 % for the two shallower ones.
- **F4:** The depth grading holds across years. The deeper half of runs is positive in every year: 2018 +3.18 % (t 4.76), 2019 +1.39 %, 2020 +0.96 %, 2021 +2.13 %. The shallower half is near zero: +0.35 %, +0.55 %, -0.92 %, +0.25 %. The Spearman of depth in swing units is negative in 3 of 4 years (-0.24, -0.12, -0.30; 2021 +0.08).
- **F5:** The effect sits in falling markets and on every coin, as the brief says. Run-ending up days give +1.36 % (t 2.58, 275 cases) in falling markets against -0.40 % (t -0.77, 176 cases) in rising ones. All six coins are positive in the falling regime, from +0.90 % (XRP, t 1.53) to +1.68 % (XMR, t 2.77).

## Ideas
- `074-01.b1_falling-deep-run-break-fade` (from F1, F2, F3, F4, F5): In a falling market, the first up day after a run of consecutive down days is followed by a fall in the coin's close over the next day, and the deeper the run's fall, measured as the coin's return over the run's down days against its usual daily swing over the last 30 days, the larger that next-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
