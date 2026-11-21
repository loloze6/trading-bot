---
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day_1h
idea tested: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3825 USD
---
## Findings
- **F1:** Measured on the 30-day-volatility-scaled 24-hour return at every bar (non-overlapping grid, 15,950 cases), the 24-hour reversal is three times stronger in the top tercile of volatility relative to its own 90-day median (−60.6 bp of next-24h excess return per unit z, t −8.2) than in the middle tercile (−22.7 bp, t −3.1), and absent in the bottom tercile (−2.0 bp, t −0.3); the top-tercile slope is negative in all 8 years, with t at or below −2.1 in 6 of them.
- **F2:** The reversal depends on when the 24-hour move is read: per-hour slopes of next-24h excess return on the fall are largest at the 00:00–05:00 UTC closes (25–35 bp per z, t 6.1–8.9) and vanish at 13:00–15:00 UTC (t −1.5 to −0.2), while the tested 19:00-stamped bar sits in between (12.4 bp, t 3.2); at the 01:00 bar the slope is significant on every coin (t −2.3 for XRP to −6.4 for XMR) and in 6 of 8 years.
- **F3:** Against the brief, moves made with volume spread evenly across the 24 hours reverse more than moves made in a volume burst: the grid slope is −49.0 bp per z (t −6.0) in the lowest tercile of max-hour volume share versus −14.2 bp (t −2.3) in the highest, and the z × volume-concentration interaction is positive on all 6 coins (t 0.5 to 2.7, 4 of 6 above 1.8).
- **F4:** The hours after the 20:00 and 21:00 UTC closes carry a steady drift of +4.2 to +5.5 bp per hour on every coin (t 3.0 to 4.4), positive in 7 of 8 years, against a typical hour near zero.
- **F5:** The book fails mainly because it holds too little of the market's rise rather than because the signal is wrong: Sharpe 0.50 sits 0.057 below holding, and its mean daily return of 0.000368 is under the 0.0005 bar, while the reversal it trades is only a mid-strength slice (F2) of a broader effect that is strongest in high-volatility stretches (F1).

## Ideas
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day.g1_volatility-scaled-daily-move-reversal` (from F1, F5): The higher a coin's 30-day hourly volatility stands above its own 90-day norm, the more of its last 24 hours' move, scaled by that volatility, it gives back over the next 24 hours.
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day.g2_post-midnight-daily-fall-rebound` (from F2, F5): The more a coin has fallen over the 24 hours up to the 01:00 UTC close, the more it rises over the next 24 hours.
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day.g3_evenly-traded-moves-revert` (from F3, F1): The more evenly a coin's volume was spread across the hours of its last 24 hours, the larger the share of that 24-hour move it gives back over the next 24 hours.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
