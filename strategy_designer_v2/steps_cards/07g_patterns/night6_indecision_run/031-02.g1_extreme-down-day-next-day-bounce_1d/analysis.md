---
line: 7.g patterns
backtest: 031-02.g1_extreme-down-day-next-day-bounce_1d
idea tested: 031-02.g1_extreme-down-day-next-day-bounce
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3971 USD
---
## Findings
- **F1:** After a down day of at least one usual move (z ≤ −1), the next-day excess return rises with the coin's own 20-day volatility quintile: −0.41 % (t −1.53, 243 days), +0.14 %, +0.62 %, +0.61 %, then +2.29 % in the top quintile (t 2.85, 170 days). The top quintile is +2.59 % (t 2.89) in w1–12 and +2.17 % (t 2.00) in w13–24, positive on all 6 coins (+1.45 % to +3.42 %), and is 12 times the 0.19 % cost of a trade.
- **F2:** Among down days of at least one usual move, the raw percentage size of the fall grades the next-day excess better than the fall in usual moves does: the deepest tercile is +1.19 % (t 2.22, 248 days), the middle +0.60 % (t 2.18, 355 days), the shallowest −0.07 % (t −0.32, 387 days). By contrast, falls of 2 usual moves or more, the tested gate, gave only +0.72 % (t 2.26, undone by day clustering, step 5 t 1.30).
- **F3:** Measured against the coin's own 120-day volatility, the same down days bounce only when the 20-day volatility stands high: the top tercile is +1.64 % next day (t 2.71, 153 days), the middle +0.09 % (t 0.26), the bottom −0.19 % (t −0.53).
- **F4:** The bounce belongs to down days only: up days of at least one usual move are followed by −0.29 % to +0.33 % across the same volatility quintiles, none with |t| > 1.6. Down days of under one usual move reach only +0.39 % (t 1.39) in the top volatility quintile.
- **F5:** A close near the day's low is followed by a modest rise: lowest close-location quintile +0.35 % next day (t 2.27, 1278 days), +0.37 % (t 2.27) on down days. It is weaker in w1–12 (+0.19 %, t 0.93) than in w13–24 (+0.51 %, t 2.23), so it adds little beside F1–F3.
- **F6:** The brief's own setup runs the other way at the day level. After a 5-day run, wide-range flat-body days are followed by a −0.67 % next-day move against the run, which means continuation (t −2.56, 636 cases, not day-clustered). The book earned +0.009 % a day (t 0.72), and trades in its lowest entry-forecast quartile lost −0.76 % (t −1.88).

## Ideas
- `031-02.g1.g1_volatile-coin-down-day-bounce` (from F1, F2, F4): After a day on which a coin falls, it rises over the next 1 day, and the larger the day's fall measured in percent and the higher the coin's 20-day volatility of daily returns, the larger that rise.
- `031-02.g1.g2_expanded-volatility-down-day-bounce` (from F3, F1, F4): After a day on which a coin falls, it rises over the next 1 day, and the higher the coin's 20-day volatility of daily returns stands against its own 120-day volatility, the larger that rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
