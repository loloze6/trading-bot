---
line: 7.g patterns
backtest: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound_1h
idea tested: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3798 USD
---
## Findings
- **F1:** Over 24 hours, a coin's 24-hour return scaled by its 30-day hourly volatility predicts its next 24 hours in the opposite direction, on non-overlapping 24-hour cells. The slope is −16.3 bp per unit for BTC (t −2.47, 2656 cases) and −29.0 bp for ETH (t −3.41, 2656 cases). Its top quintile of 24-hour return is followed by −30.6 bp (BTC, t −2.01) and −43.4 bp (ETH, t −2.23), and its bottom quintile by +30.0 bp and +48.5 bp.
- **F2:** This 24-hour reversal sits in heavy-volume days. The slope is −27.4 bp (t −3.86, 1771 cases) in the top tercile of 24-hour volume against its 30-day mean, −23.4 bp (t −1.83) in the middle tercile and +29.8 bp (t 1.68) in the bottom tercile.
- **F3:** The reversal is not one period's artefact. Its yearly slope is negative in 6 of 8 years, with t below −2 in 2018 (−2.41), 2020 (−2.91), 2021 (−2.76) and 2025 (−2.20). It is flat in 2022 to 2024 (t +0.29, −0.73, +0.50).
- **F4:** The reversal is specific to a 24-hour look-back and a 24-hour horizon. With a 12-hour look-back over 12 hours, the slope is positive (BTC +7.1 bp, t 2.13). Look-backs of 48 and 72 hours show no reversal at any horizon (all |t| < 1.5).
- **F5:** The tested heavy-volume fall rebound is not graded. Over 2 hours, falls of 1.5 to 3 standard deviations on volume above 2.5 times its mean are followed by +20.7 bp (t 2.81, 812 cases), and falls beyond 3 standard deviations by about the same, +20.3 bp (t 1.93, 507 cases). Over 6 hours, the deepest falls give −5.8 bp (t −0.15), consistent with the step 5 slope of −4.9e-6.
- **F6:** The book gives back its 2-hour edge by holding past it. Trades lasting 1 hour or less gross +0.44 % (6724 trades) and those of 1 to 2 hours +0.27 % (10501). Trades of 2 to 5 hours gross −0.81 % (3912). The book's mean daily return is negative in 6 of 8 years (for example −30.5 bp in 2022 and −20.5 bp in 2025).
- **F7:** Hour-of-day effects stand out across both coins, but each move is far below the 0.11 % cost of a trade. Hours 20–21 UTC are followed by about +4 bp per hour (BTC t 3.81, ETH t 3.92). Hours 0–3 UTC are followed by about −2 bp (BTC t −3.24, ETH t −3.02). They are ungraded calendar effects, so no idea is written from them.

## Ideas
- `028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound.g1_heavy-volume-daily-move-reverses` (from F1, F2, F3, F4): After a coin's 24-hour return is large relative to its typical hourly move over the past 30 days, it moves back the opposite way over the next 24 hours. The larger that 24-hour move in units of its usual daily move, and the heavier the 24 hours' volume against its 30-day average, the larger the reversal.
- `028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound.g2_volume-sized-short-crash-bounce` (from F5, F6): After an hour in which the coin falls more than its typical hourly move over the past 30 days on volume well above its 30-day hourly average, it rises over the next one to two hours. The rebound grows with that hour's volume against its 30-day average rather than with the depth of the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
