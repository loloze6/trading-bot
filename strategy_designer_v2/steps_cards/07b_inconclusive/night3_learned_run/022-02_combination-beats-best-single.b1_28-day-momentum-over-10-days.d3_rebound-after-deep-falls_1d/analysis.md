---
line: 7.b inconclusive
backtest: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d3_rebound-after-deep-falls_1d
idea tested: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d3_rebound-after-deep-falls
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3168 USD
---
## Findings
- **F1:** The test's result points the other way from the idea, not short of it. The pooled slope of the 10-day unusual return on the forecast is −0.0010 (t −1.49, 1,691 grid cells). Cells with a positive forecast average −0.67 % unusual over 10 days (1,036 cells), against +1.06 % for cells with a zero forecast (655 cells). The cases' unusual move is −0.92 % per case (931 cases).
- **F2:** The idea's situation is followed by continuation, not rebound, and most clearly over the shortest horizon. The slope is −0.0017 over 5 days (t −3.66, 1,728 cells), −0.0010 over 10 days (t −1.49) and −0.0012 over 20 days (t −1.05, 1,547 cells). Five of the six coins have a negative 5-day slope (ETH t −2.66, XRP t −1.92, BTC t −1.68); XMR is the exception (t −0.04).
- **F3:** Sorted by the 28-day return, the 10-day unusual return rises steadily from the deepest falls to the largest rises: about 250 cells per quintile.
- **F4:** Sorted by the close's position in its 60-day range, the 10-day unusual return is lowest near the low and highest near the high.
- **F5:** The rebound shows in no stable part of the data. Its slope is positive in 2018 (t +2.46) and 2023 (t +2.21), but negative in 2019 (t −3.01) and 2025 (t −1.58). After 90-day falls it is weak (t +1.12, 191 cells). After 90-day rises it is negative (t −0.91), and the cases there average −2.7 % unusual. Volatility does not help either: every volatility tercile has a negative slope (t −0.73, −1.69, −1.11).
- **F6:** The book earns only the coin's drift. The total move per case is +0.26 %, 1.3 times the 0.19 % cost of a trade, while the unusual move is −4.8 times that cost. The book's Sharpe is 0.26, 0.30 below holding the coins.
- **F7:** The 28-day return used as a straight line is a weak predictor. Its raw pooled slope on the 10-day unusual return is positive but small (t +1.50), and positive in each volatility tercile (t +1.84, +0.30, +2.24). This is weaker than the quintiles of F3 suggest, probably because a few very large 28-day rises dominate the straight line.

## Ideas
- `022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d3_rebound-after-deep-falls.b1_continuation-near-60-day-highs` (from F1, F2, F3, F4, F7): The higher a coin's close sits within its 60-day close range and the larger its 28-day return, the higher its return over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
