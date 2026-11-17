---
line: 7.d not profitable
backtest: 010-08_rsi-below-streak-reversal_1d
idea tested: 010-08_rsi-below-streak-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4240 USD
---
## Findings
- **F1:** The book loses because its long bars come when the coin does worse than usual: the book's mean gain per bar is -0.000046, made of +0.000296 from the coin's own rise and -0.000345 from timing. On long bars the next-day return is 0.000004 for BTC against a coin mean of 0.001183, and -0.000491 for ETH against 0.001368.
- **F2:** The long bars pay only when the coin is deep below its 60-day high. Split into terciles of the 60-day drawdown (574 long bars each), the mean gain is +0.001435 in the deepest tercile (summed +0.82), -0.001085 in the middle (summed -0.62) and -0.000606 in the shallowest (summed -0.35).
- **F3:** On the 14-day grid (bars with a run below 50), the run-length slope holds only in deep drawdowns. Its t is 1.97 in the deeper half of 60-day drawdowns (n=56) against 0.24 in the shallower half (n=57). Run length times drawdown depth has t 1.96, against 1.79 for run length alone (n=113).
- **F4:** The forecast's information sits in the longest runs. Long bars with runs of 40–60 days earn a mean next-day return of +0.002006 (gain +0.001277, n=225). Runs of 0–5 days earn -0.001161 (n=321) and runs of 5–10 days earn -0.001074 (n=512); none of these bins reaches |t| 0.7.
- **F5:** The book's losses follow the bear years, when holding was also negative. The book's mean daily return was -0.000407 in 2018 (holding -0.002958), -0.001228 in 2022 (holding -0.002347) and -0.000537 in 2025. It was positive in 2019–2021 and 2023–2024, while holding earned far more.
- **F6:** The losses are concentrated in a few heavy bars. The 40 worst long bars average a gain of -0.0894 and sum to 24 times the book's net total. On them the position averaged 1.10, the run averaged 35 days (19.5 on all long bars) and the 7-day return averaged -0.073 (-0.049 on all long bars).

## Ideas
- `010-08_rsi-below-streak-reversal.d1_rsi-streak-reversal-deep-drawdown` (from F1, F2, F3, F5): The longer a coin's 14-day RSI has stayed below 50 without a break, measured in days up to the current close, the higher the coin's return over the next 14 days, only while the coin's close stands well below its highest close of the past 60 days, the effect growing with the distance below that high.
- `010-08_rsi-below-streak-reversal.d2_long-rsi-runs-reverse-up` (from F1, F4, F6): The longer a coin's 14-day RSI has stayed below 50 without a break, measured in days up to the current close, the higher the coin's return over the next 14 days, with the rise coming mainly from runs lasting several weeks and growing with the run's length beyond that.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
