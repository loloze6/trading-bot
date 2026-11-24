---
line: 7.b inconclusive
backtest: 031-01_wide-flat-day-ends-uprun_1d
idea tested: 031-01_wide-flat-day-ends-uprun
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4100 USD
---
## Findings
- **F1:** The tested result points the wrong way for the idea. Step 5's main measure gives a mean 5-day unusual move in the short direction of -1.24 % (t -0.93, 86 cases on 74 days). My recomputation of the up-run, wide-flat days gives the coin rising: +2.33 % unusual over 5 days (t 1.67, 68 cases), +2.89 % over 3 days (t 2.41, 71 cases) and +1.36 % over 1 day (t 1.93). The fall the idea predicts is not there; what follows is continuation, strongest at 3 days.
- **F2:** The continuation grows with the size of the prior run. By tercile of the 5-day rise, the 5-day unusual move is -0.19 %, +1.88 % and +5.28 % (t 1.80, 23 cases in the top tercile), and the 3-day figures are +0.04 %, +3.03 % and +4.79 %. The Spearman correlation with the 5-day rise is 0.20.
- **F3:** Inside the wide-flat cases, a wider range and a flatter close do not deepen the fall the idea predicts. By range-ratio tercile, the 5-day unusual move is +4.31 %, +1.64 % and +1.01 % (Spearman -0.19). Flatness terciles are all near +2.3 % (Spearman 0.005). Neither of the idea's grading variables carries a reversal.
- **F4:** The effect is fragile. It is concentrated in 2021 (+10.2 % over 5 days, t 3.68, 10 cases) and in ETH (+9.6 %, t 2.54, 7 cases). Without 2021 the 3-day move is +1.76 % (t 1.52, 61 cases) and the 5-day move +0.97 % (t 0.65). Without ETH the 5-day move is +1.49 % (t 1.03).
- **F5:** Across all up-run days, the 3-day unusual move rises with the day's range:
- **F6:** After a 5-day fall, wide-flat days show nothing at 5 days: +0.93 % in the up direction (t 0.42, 34 cases).

## Ideas
- `031-01.b1_wide-day-extends-up-run` (from F1, F5): After a coin has risen over the past 5 days, the wider that day's high-low range compared with its average daily range over the past 20 days, the more the coin rises over the next 3 days.
- `031-01.b2_wide-doji-continues-strong-run` (from F1, F2, F4): After a coin has risen over the past 5 days, a day whose range is wide compared with its average daily range over the past 20 days but whose close lands near its open is followed by a rise over the next 3 days, and the larger the 5-day rise before it, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
