---
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day_1d
idea tested: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4504 USD
---
## Findings
- **F1:** The book's whole result rests on its long side. Long bars gained a mean +0.32 % per bar (t 6.09, 7922 bars). Short bars lost a mean −0.04 % (t −1.20, 7713 bars). The signed next-day excess move was +0.21 % after rises (t 3.14) and only +0.07 % after falls (t 1.09).
- **F2:** A coin's next-day excess return rises steadily with its own 20-day volatility quintile: −0.20 % (t −4.12), −0.13 % (t −2.32), +0.00 %, +0.14 % (t 1.49), +0.19 % (t 2.23), each quintile about 6150 bars.
- **F3:** After the largest one-day falls relative to 20-day volatility, the next day rebounds, and the rebound shrinks as the fall gets smaller. By decile of that move, the next-day excess was +0.37 % for decile 0 (t 2.23), +0.26 % for decile 1 (t 2.71) and +0.01 % for decile 2 (t 0.16), about 3070 bars each. The top decile of rises showed a weaker +0.19 % (t 1.67).
- **F4:** Five-day extremes show the same U shape. By decile of the 5-day move over its volatility, the next-day excess was +0.25 % for the lowest decile (t 2.20) and +0.33 % for the highest (t 2.80). Middle deciles ran down to −0.20 % (t −2.30).
- **F5:** The brief's range reversion shows only at the top of a flat range, on non-overlapping 5-day returns. With net move under a quarter of the 30-day range, coins near the top fell −2.36 % excess (t −2.40, 105 cases). Coins near the bottom did not rise (−0.41 %, t −0.56, 169 cases).
- **F6:** Away from flat ranges, position in the 30-day range continued over 5 days rather than reverting. In the middle band of net move, the top of the range was followed by +2.23 % (t 2.10, 157 cases) and the bottom by −3.09 % (t −3.86, 183 cases). In trending coins the top was followed by +1.87 % (t 2.44, 706 cases).
- **F7:** The book's extreme days carry its result. Its best 2 % of days (58 days, +5.90 % mean, coins −1.29 % on those days) hold 2.38 times its total gain. Its worst 2 % (−5.45 %) take back 2.19 times.
- **F8:** Next-day excess by weekday alternates sign: +0.27 % after a Tuesday bar (t 3.33), +0.26 % after a Friday bar (t 4.32), −0.27 % after a Wednesday bar (t −2.54). These are the same calendar days across all coins, so the t-statistics are inflated. I do not treat this as a pattern.

## Ideas
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day.g1_high-volatility-precedes-gains` (from F2, F4): The higher a coin's volatility over the past 20 days relative to its own usual level, the higher its return over the next day.
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day.g2_large-daily-falls-rebound` (from F3, F4): The larger a coin's one-day fall relative to its 20-day volatility, the larger its rise over the next day.
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day.g3_upside-trend-continuation-only` (from F1, F6): The larger a coin's 30-day rise when that rise spans much of its 30-day high-low range, the higher its return over the next five days.
- `023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b1_trend-continues-next-day.g4_flat-range-top-reverts` (from F5): In a coin whose 30-day net move is small next to its 30-day high-low range, the closer its close sits to the top of that range, the further it falls over the next five days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
