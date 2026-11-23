---
line: 7.b inconclusive
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3955 USD
---
## Findings
- **F1:** The main measure is on the side the idea predicts but just short of the bar: the forecast-weighted mean excess 5-day return is +0.575 % with t 1.97 over 2490 cells. The test already used every coin and every fold available, so more of the same data cannot be added.
- **F2:** The coin's own market move drowns the effect. In windows where the coin rose overall, cells with forecast > 0 earn +2.14 % excess (t 5.11, 1226 cells). In windows where it fell they earn −0.85 % (t −2.11, 1264 cells). By year, 2022 is −1.97 % (t −2.44, 284 cells) against 2024 at +1.12 % (t 2.20, 577 cells).
- **F3:** The effect shows only after the coin has been rising, split by the coin's past 30-day return:
- **F4:** A closely related split, by nearness to the 30-day high, tells the same story. The third of cells closest to the high carries +1.41 % weighted excess (t 2.30, 536 cells). The middle third is −0.63 % (t −1.35).
- **F5:** The effect is not graded strongly inside the forecast:
- **F6:** The plan's horizon is the right one, as longer horizons are weaker: t is 1.08 over 10 days (1235 cells) and 0.66 over 20 days (604 cells). The size measure gives an unusual move of −0.07 % per case (strength −0.003), against a total move of +0.63 % that is mostly the coin's drift (+0.71 %) over a 0.23 % trade cost.
- **F7:** Positive-forecast cells still beat zero-forecast cells by 0.82 % over 5 days (Welch t 2.60; 2490 against 2290). Among zero-forecast cells, a positive 30-day return earns +0.16 %, against +1.59 % for positive-forecast cells in the top 30-day-return third. The forecast therefore adds something beyond the rise itself.

## Ideas
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins.b1_nearness-reversal-after-rises` (from F1, F2, F3, F4, F7): For a coin's nearness to its 90-day high, the higher that signal's predictive power for the coin's 5-day returns over the past 365 days, the lower the same signal's predictive power over the following 90 days. The turn shows on the rising side, only while the coin's own 30-day return is positive: the more strongly this reversal points up, the higher the coin's return over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
