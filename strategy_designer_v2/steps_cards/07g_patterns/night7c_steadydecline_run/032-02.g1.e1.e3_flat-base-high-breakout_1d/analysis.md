---
line: 7.g patterns
backtest: 032-02.g1.e1.e3_flat-base-high-breakout_1d
idea tested: 032-02.g1.e1.e3_flat-base-high-breakout
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3945 USD
---
## Findings
- **F1:** On the 5-day grid of folds B and C (1278 cases), the excess 5-day return rises with closeness to the 28-day closing high (Spearman 0.114, p 0.00004). The quintile within 3.2 % of the high gains +2.99 % (t 3.67, n 256), and closes exactly at the high gain +4.84 % (t 3.12, n 113). The quintile 17–27 % below the high loses −3.17 % (t −4.88, n 255).
- **F2:** Volatility decides whether the 28-day return continues. Splitting the cases by thirds of 28-day return and of 20-day/60-day volatility ratio, the calm third shows a graded continuation: falling third −3.63 % (t −3.48, n 107), middle third +0.67 % (t 0.83, n 166), rising third +3.76 % (t 2.46, n 105). In the wild third, all three cells are flat (−0.35 %, −0.35 %, −0.26 %, every |t| < 0.3).
- **F3:** Closes near their 28-day lowest close are followed by excess falls. The quintile within 4 % of the low loses −1.83 % over 5 days (t −2.21, n 256), and the next quintile (4–10 % above the low) loses −1.58 % (t −2.74). Quintiles 10–35 % above the low gain +1.35 % (t 2.09) and +1.54 % (t 1.98); Spearman 0.073, p 0.009.
- **F4:** Among closes within 3 % of the 28-day high, the tested idea's grading fails.
- **F5:** The volatility ratio, the relative daily range and the relative volume each predict nothing on their own (Spearman −0.038, 0.006, 0.032, all p > 0.2). Calm matters only through how it changes the 28-day move's effect (F2).

## Ideas
- `032-02.g1.e1.e3.g1_calm-regime-monthly-momentum` (from F2, F5): When a coin's daily volatility over the last 20 days is low compared with the last 60 days, the larger its 28-day return, the larger its return over the next 5 days: calm declines keep falling and calm rises keep rising, more so the larger the past move.
- `032-02.g1.e1.e3.g2_proximity-to-monthly-high` (from F1, F4): The closer a coin's close is to its highest close of the last 28 days, the larger its rise over the next 5 days.
- `032-02.g1.e1.e3.g3_monthly-low-keeps-sinking` (from F3): The closer a coin's close is to its lowest close of the last 28 days, the larger its fall over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
