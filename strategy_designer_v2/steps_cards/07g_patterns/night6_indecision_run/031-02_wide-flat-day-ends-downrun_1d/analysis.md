---
line: 7.g patterns
backtest: 031-02_wide-flat-day-ends-downrun_1d
idea tested: 031-02_wide-flat-day-ends-downrun
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5153 USD
---
## Findings
- **F1:** Over all six coins, the day after a coin's own worst 2 % of daily returns ends +1.79 % above its normal one-day drift (t 2.09 with the cases of one day taken together, 342 cases on 132 days). The next band (2-5 %) shows +0.43 % (t 1.13), the 5-10 % band +0.57 % (t 2.30), and every band from the median upward is between -0.72 % and +0.20 % with no t beyond 2 in size, so the next-day move grows with the depth of the fall.
- **F2:** Within each coin's worst 10 % of daily returns, the next-day unusual move is positive for all six coins: BTC +0.48 % (t 1.80), ETH +0.57 % (t 1.60), LTC +0.39 % (t 1.06), XMR +1.32 % (t 3.68), XRP +0.64 % (t 1.47) and ZEC +1.22 % (t 2.88), on 287 days each. It is also positive in all eight years, from +0.20 % (2025) to +1.57 % (2020).
- **F3:** Among those worst-10 % days, the ones closing in the lowest third of their range show the next-day bounce most clearly: +0.86 % (t 2.93, 1375 cases on 509 days). Closes in the middle third show +0.66 % (t 1.13, 330 cases), and only 17 cases close in the top third.
- **F4:** The bounce after the worst-10 % days is concentrated in the first days: +0.60 % over 2 days (t 1.22, 846 cases), +0.96 % over 3 days (t 1.36, 557 cases) and +0.46 % over 5 days (t 0.45, 324 cases). The 5-day horizon the tested book used does not hold it.
- **F5:** The tested situation itself carries nothing. The book's active bars returned -0.02 % on average over the next 5 days (201 bars). On the 5-day grid, wide flat days after a 5-day fall show -0.120 of a usual move (t -0.76, 42 cases), against +0.063 (t 1.50, 485) for wide days with a body. Net trade results range from -0.83 % (BTC, 59 trades) to +1.96 % (ZEC, 56 trades).
- **F6:** Measured in units of the coin's 20-day volatility, the next-day bounce is weaker and less graded than when measured by the coin's own percentile. Days below -3 units show +0.82 % (t 0.73, 171 cases), and days at -1.5 to -1 units show +0.62 % (t 2.37, 861 cases).

## Ideas
- `031-02.g1_extreme-down-day-next-day-bounce` (from F1, F2, F3, F4, F6): After a day on which a coin falls far more than it usually does in a day, it rises over the next 1 day. The deeper that day's fall ranks among the coin's own past daily returns, and the nearer its close sits to the day's low, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
