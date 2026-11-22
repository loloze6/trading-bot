---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound
line: 7.g patterns
backtest: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After a coin's 24-hour return is large relative to its typical hourly move over the past 30 days, it moves back the opposite way over the next 24 hours. The larger that 24-hour move in units of its usual daily move, and the heavier the 24 hours' volume against its 30-day average, the larger the reversal.
Consequence: A trader would fade a coin's heavy-volume 24-hour run for the next day rather than chase it, sizing the fade by how stretched the run is.
Why:
- F1: Over 24 hours, a coin's 24-hour return scaled by its 30-day hourly volatility predicts its next 24 hours in the opposite direction, on non-overlapping 24-hour cells. The slope is −16.3 bp per unit for BTC (t −2.47, 2656 cases) and −29.0 bp for ETH (t −3.41, 2656 cases). Its top quintile of 24-hour return is followed by −30.6 bp (BTC, t −2.01) and −43.4 bp (ETH, t −2.23), and its bottom quintile by +30.0 bp and +48.5 bp.
- F2: This 24-hour reversal sits in heavy-volume days. The slope is −27.4 bp (t −3.86, 1771 cases) in the top tercile of 24-hour volume against its 30-day mean, −23.4 bp (t −1.83) in the middle tercile and +29.8 bp (t 1.68) in the bottom tercile.
- F3: The reversal is not one period's artefact. Its yearly slope is negative in 6 of 8 years, with t below −2 in 2018 (−2.41), 2020 (−2.91), 2021 (−2.76) and 2025 (−2.20). It is flat in 2022 to 2024 (t +0.29, −0.73, +0.50).
- F4: The reversal is specific to a 24-hour look-back and a 24-hour horizon. With a 12-hour look-back over 12 hours, the slope is positive (BTC +7.1 bp, t 2.13). Look-backs of 48 and 72 hours show no reversal at any horizon (all |t| < 1.5).
