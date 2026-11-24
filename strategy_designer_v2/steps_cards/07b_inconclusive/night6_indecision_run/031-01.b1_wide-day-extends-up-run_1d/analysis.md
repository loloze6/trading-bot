---
line: 7.b inconclusive
backtest: 031-01.b1_wide-day-extends-up-run_1d
idea tested: 031-01.b1_wide-day-extends-up-run
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3309 USD
---
## Findings
- **F1:** The test's slope is on the side the idea predicts but short of the bar. Step 5 found t 1.43 over 2907 cases, and my rebuild on the 3-day grid gives slope +0.0086, t 1.63 over 2373 up-run cases. The size is small and uncertain: unusual move +0.15 % per case (t 0.74), strength 0.016 of a usual move.
- **F2:** The effect is not graded across the range ratio. Mean excess 3-day returns by ratio quintile in up-runs are +0.44 %, +0.26 %, −0.07 %, −0.46 %, +1.16 %. Only the widest quintile stands out (t 1.87, 475 cases on 247 days), and the slope on the log ratio is weaker (t 1.12).
- **F3:** The widest days carry the effect only after the strongest 5-day rises. There the widest quintile is followed by +2.14 % excess over 3 days (t 2.28, 258 cases on 156 days). After weak rises it is −0.26 % (t −0.31) and after middling rises +0.18 % (t 0.32).
- **F4:** The effect changes sign from year to year. The up-run slope t is −2.49 in 2018, −1.55 in 2023 and +2.27 in 2024. In the widest quintile the mean excess is −4.30 % in 2018 against +2.73 % in 2024. Across coins the slope t runs from −0.90 (XMR) to +2.07 (ETH).
- **F5:** The 5-day-rise condition adds little. The 3-day slope is also positive after 5-day falls (t 1.22, 2342 cases) and reaches t 2.01 over all days (4715 cases). Other horizons are no clearer: up-run t 1.39 at 1 day, 0.69 at 5 days, 1.46 at 10 days.

## Ideas
- `031-01.b1.b1_wide-day-extends-run-more-coins` (from F1, F4): After a coin has risen over the past 5 days, the wider that day's high-low range compared with its average daily range over the past 20 days, the more the coin rises over the next 3 days.
- `031-01.b1.b2_wide-day-extends-strong-run` (from F2, F3): After a coin has risen over the past 5 days, the larger that 5-day rise and the wider that day's high-low range compared with its average daily range over the past 20 days, the more the coin rises over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
