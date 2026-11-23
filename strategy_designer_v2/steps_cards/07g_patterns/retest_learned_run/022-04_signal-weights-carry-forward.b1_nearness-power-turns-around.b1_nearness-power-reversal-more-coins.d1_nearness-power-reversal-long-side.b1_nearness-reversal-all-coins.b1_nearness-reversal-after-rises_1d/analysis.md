---
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins.b1_nearness-reversal-after-rises_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins.b1_nearness-reversal-after-rises
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.6795 USD
---
## Findings
- **F1:** Saturday is the one weekday that stands out across coins. The day-by-day cross-coin mean on Saturdays is +0.500 % (t 3.28, 414 days), against +0.045 % on the other days (Welch t 2.60, 414 against 2,484 days). It is positive in 15 of the 16 coins with Saturday data, INJ being the exception, and positive in every year 2018–2025 (from +0.11 % to +0.78 %). Its daily standard deviation is also lower, 3.91 % against 4.94 %.
- **F2:** Saturday's return is graded by the coin's 5-day return up to Friday's close, scaled by its 30-day volatility. By quartile, from bottom to top, it is −0.24 %, +0.12 %, +0.76 % and +1.10 % (rank slope t 3.46, clustered by day, 2,677 coin-days). The grading is weaker for the previous single day (slope t 1.94) and for the 30-day return (slope t 1.81).
- **F3:** Saturday's return is not graded by volatility. By 30-day volatility quartile it is +0.37 %, +0.41 %, +0.36 % and +0.57 % (slope t 0.55). Relative to the coin's usual volatility the slope is −0.72, so the Saturday gain is not a high-volatility artefact.
- **F4:** Within the tested idea, the forecast's size does not order the 5-day returns. On active cases the quartiles are +0.46 %, +1.71 %, +0.93 % and +0.54 % above drift (Spearman −0.014, p 0.64), while the trades' mean is highest in the lowest and highest entry-forecast quartiles (+9.0 % and +10.2 %).
- **F5:** Most of the book's gain comes from the 30-day-rise regime, not from the reading itself. Grid cases with a positive 30-day return earn +0.44 % above drift over 5 days (t 1.87, 2,444 cases), against −0.44 % in the other cases (t −2.13, 2,431 cases). Inside the rising regime, bars with the forecast on earn +0.77 % (t 2.15, 867 cases), against +0.17 % with it off (t 0.45, 1,020 cases).
- **F6:** No other angle cleared the bar for the number of angles examined, and none points to an idea:

## Ideas
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins.b1_nearness-reversal-after-rises.g1_saturday-continuation-after-rises` (from F1, F2, F3): On Saturdays, the higher a coin's 5-day return to Friday's close relative to its 30-day volatility, the higher its return over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
