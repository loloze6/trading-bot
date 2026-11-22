---
line: 7.g patterns
backtest: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade_1h
idea tested: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3854 USD
---
## Findings
- **F1:** Over the 6-hour grid, quiet-volume hours (0.5–1.5× the 30-day mean volume) show no grading at all: the slope of the next 6 hours' unusual return on the hour's move in 30-day mean absolute moves is +0.001 % per unit (t 0.06, 7076 cases). Large quiet rises (z 2 to 4) are followed by +0.06 % (t 0.72, 355 cases), so they continue slightly rather than give back. This matches the step-5 verdict of no effect (t 0.91, strength 0.009).
- **F2:** The brief's own claim, that surging-volume moves continue, does not stand out either. For |z| > 2 on more than 1.5× volume, the move-signed 6-hour unusual return is +0.19 % for BTC (t 1.62, 385 cases) and +0.02 % for ETH (t 0.11, 325 cases) at 1.5–3× volume, and +0.08 % / +0.20 % (t 0.37 / 0.89) above 3×. That is not distinguishable from chance.
- **F3:** The book lost because it was short into a rising market, not because of timing.
- **F4:** A coin's 24-hour return, scaled by its 30-day hourly mean absolute move × √24, predicts the next 24 hours in the opposite direction, in both coins, on non-overlapping 24-hour cases.
- **F5:** The 24-hour reversal is graded and largest in the tails, with a size above the cost of a trade (0.11 %).
- **F6:** The 24-hour reversal holds in most years but not all. Its slope is negative in 2018–2021 and 2025 for both coins (for example ETH 2019 −0.38 %, t −2.41; BTC 2025 −0.19 %, t −2.05). It is near zero or slightly positive in 2022–2024 (BTC +0.01 % to +0.02 %, ETH −0.10 % to +0.06 %).
- **F7:** The hours opening 21:00 and 22:00 UTC rise more than the coin's average hour.

## Ideas
- `028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b1_quiet-large-rise-six-hour-fade.g1_one-day-move-reverses-next-day` (from F4, F5, F6, F3): The larger a coin's 24-hour return relative to its typical hourly move over the past 30 days, the more the price moves back the other way over the next 24 hours, after both rises and falls, with the largest give-backs following the most extreme 24-hour moves.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
