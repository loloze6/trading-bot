---
line: 7.b inconclusive
backtest: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs_1d
idea tested: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.4587 USD
---
## Findings
- **F1:** The idea as worded is present, but the test's forecast hid it. The raw situation (the 28-day return times nearness to the 60-day high, as recorded on the bars) predicts the 10-day excess return with slope t +3.42 on 1,259 non-overlapping cases. The forecast after standardising against its own past 60 values reaches only t +0.56 on the same cases (+1.09 on all 1,691), and it correlates only 0.33 with the raw value.
- **F2:** The effect is graded in the raw value. By raw quintile, the mean 10-day excess return runs -0.58 %, -1.28 %, -0.64 %, +1.19 %, +1.59 % (252 cases each). By forecast quintile it shows no order: +0.37 %, -1.33 %, -0.26 %, +0.91 %, +0.59 %.
- **F3:** Nearness to the high is what carries the momentum. With the 28-day return alone and the near-high product in one regression, the product keeps t +2.10 and the 28-day return falls to t +0.98 (1,259 cases). Split at the median distance from the 60-day high, the 28-day return's slope is t +2.39 near the high (630 cases) and t -0.18 far from it (629 cases).
- **F4:** The effect is uneven over the years but not tied to one half. By year the slope ranges from t -2.0 (2018) and -2.2 (2022) to +3.8 (2025). Over <date> and <date> the raw slope is nearly the same (0.00072 and 0.00076 per unit), with t +1.15 and +3.53 on 630 and 629 cases.
- **F5:** The plan's horizon is the right one. At 20 days the raw product's t of +2.22 falls to +0.95 once its extremes are clipped (539 cases), and the forecast's t is 0.00 (827 cases). At 10 days the clipped product keeps t +2.49.
- **F6:** The test lacked a clear measure, not size. The unusual move per case is +1.37 % over 10 days, 7.1 times the 0.19 % round trip and a strength of 0.083, above the ~0.05 of real ideas (findings F10, F11). The book paid on all six measures, with Sharpe 1.08 and timing gain +0.077 % a day.
- **F7:** No single coin carries it. The clipped product's slope is positive on 5 of 6 coins, with t from -0.14 (XMR) to +1.95 (ZEC), on about 210 cases each, so more coins would add the cases each one lacks.

## Ideas
- `022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs.b1_momentum-near-highs-more-coins` (from F1, F4, F6, F7): The higher a coin's 28-day return, the higher its return over the next 10 days, only while the coin trades near its 60-day high; the closer to that high, the stronger the continuation.
- `022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs.b2_plain-momentum-near-highs` (from F1, F2, F3, F5): The larger a coin's 28-day rise or fall, the further its price continues the same way over the next 10 days, and more so the closer its close sits to its highest close of the last 60 days. The strength of the situation is the size of the 28-day return itself, not how it compares with the coin's own recent 28-day returns.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
