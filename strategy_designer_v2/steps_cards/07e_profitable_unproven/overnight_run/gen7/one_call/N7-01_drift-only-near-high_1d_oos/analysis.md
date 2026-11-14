---
line: 7.e profitable but not proven
backtest: N7-01_drift-only-near-high_1d_oos
idea tested: N7-01_drift-only-near-high
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3470 USD
---
## Findings
- **F1:** The book's gain is weak and partly the market's own rise. Its daily mean is 0.00127 with t = 1.81 over 1449 book days. Regressed on the equal-weight coin return it has beta 0.40 and alpha 0.00100/day with t = 1.80. Its in-market position averages 1.33× allocation (median 1.42), which adds to the market exposure.
- **F2:** The gain rests on a few days. The top 10 of 1449 book days sum to 1.32 of the book's total 1.84 in summed daily returns. The remaining 1439 days average only 0.00036. Trades show the same pattern: 2024 trades, median −1.6 %, 41 % winners, and the 10 best of 2024 make 2175 of the 9784 summed trade percent.
- **F3:** The gain is earned in a few strong-market windows, not spread evenly. In-market coin excess over the coin's all-window mean is +0.0083 in w6 (t = 4.66, n = 699 coin-days) and +0.0089 in w9 (t = 3.06, n = 593), when the market averaged +0.0086 and +0.0073 a day. It is −0.0118 in w10 (t = −2.92, n = 146), −0.0081 in w3 (t = −2.32, n = 276) and −0.0074 in w12 (t = −2.22, n = 139).
- **F4:** No single coin carries the book. Leaving any one coin out keeps the mean daily book return between 0.00108 (SOL out) and 0.00141 (UNI out).
- **F5:** Inside the gate, next-day excess grows with closeness to the 20-day high. In-market coin-days in the top quartile of the raw near-high value have next-day excess +0.0047 (t = 2.41, n = 1132). The bottom quartile has −0.0011 (t = −0.82, n = 1132). These are 1-day returns; same-day coins are correlated, so the t is optimistic.
- **F6:** Next-day excess also depends on how recent the high is. With the high 0–5 bars old (raw recency 15–20), excess is +0.0027 (t = 2.76, n = 3200). With the high 5–10 bars old (raw 10–15), excess is −0.0024 (t = −1.39, n = 851).
- **F7:** Being above SMA20 without a recent 20-day high earns nothing. Those coin-days have next-day excess −0.0016 (t = −1.02, n = 1005). By contrast, all coin-days below SMA20 have −0.0014 (t = −2.25, n = 5780), and all coin-days above it have +0.0010 (t = 1.31, n = 5009).
- **F8:** The strongest-run quartile contributes most within the gate. In-market coin-days in the top quartile of trailing 20-day return (mean +59 %) have next-day excess +0.0038 (t = 1.80, n = 995). The lower quartiles range from −0.0001 to +0.0018.

## Ideas
- `N7-01_drift-only-near-high.e1_pinned-fresh-high-continuation` (from F5, F6, F7, F2): In one coin, when the daily close sits at or very near the top of its last 20 closes and a new 20-day closing high was made within the last few bars, the next day's return is above the coin's average. The edge fades once the high is more than about five bars old or the close has slipped down its range.
- `N7-01_drift-only-near-high.e2_below-average-drag-under-sma20` (from F7, F3): In one coin, the day after a close below its 20-day simple average, the return is below the coin's average.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
