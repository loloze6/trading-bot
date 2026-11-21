---
line: 7.g patterns
backtest: 021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud_1d
idea tested: 021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3734 USD
---
## Findings
- **F1:** Across the 6 coins, Saturday (UTC) is the only weekday whose average return clearly stands apart from the others. The day's mean return averaged over the coins is +45 bps (t 3.04 on 414 days). The next best day, Friday, has t 1.70, and Monday to Thursday sit between −0.78 and +1.20. Saturday is positive in 17 of 24 windows (71 %) and above the other days in 7 of 8 years. Each coin taken alone shows it, with Saturday t from 1.40 (BTC) to 2.92 (LTC) and means of +16 to +58 bps. Seven weekdays were compared, so a t of 3 is only just past what chance would give.
- **F2:** Saturday's return is graded by the coin's return over the previous 7 days, ranked within each coin. The top third of past 7-day returns is followed by +90 bps on Saturday, the middle third by +26 bps and the bottom third by −9 bps. The top-minus-bottom gap has Welch t 4.15 on 2178 coin-Saturdays, with rank correlation 0.044. Coins move together, so these cases are not all independent and the true t is lower.
- **F3:** Saturday's return is not graded by the coin's 30-day volatility (top third +40 bps, bottom third +56 bps, t −0.71). Scaled by volatility, the Friday-plus-Saturday return stays positive in every volatility third (t 4.0, 2.7, 2.2). The effect is a level and does not scale with how wild the coin has been.
- **F4:** The tested short book fights the coins' normal rise. Over 26 days the coins drift −4.06 % in the short's direction, against an unusual move of +2.33 % in its favour, so the total move per case is −1.73 %. The book ends at Sharpe −0.38, below holding by 0.94, while 28 % of bars are in the "trending" short regime. In XMR and XRP the active cases rose by +4.4 % and +4.3 % above drift.
- **F5:** Past momentum over other horizons shows only weak links to what follows, none clear given the many angles I looked at:

## Ideas
- `021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud.g1_strong-week-lifts-saturday` (from F1, F2, F3): The higher a coin's return over the past 7 days at Friday's close, the higher its return over the following Saturday (the next 1 day).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
