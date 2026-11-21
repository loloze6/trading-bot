---
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal_1h
idea tested: 017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4608 USD
---
## Findings
- **F1:** The vol-scaled 2-hour return closing at 01:00 UTC reverses over the next 24 hours more strongly than the tested 00:00 one. The slope is -27.7 bps per usual move (t -7.4, 17096 daily cases) against -15.3 bps (t -4.1) at 00:00 and -18.5 bps (t -5.1) at 02:00. The largest third of cases reverses by 46 bps (t 6.8), and over 3 hours (22:00 to 01:00 closes) by 51 bps (t 7.4), about 2.4 to 2.7 times the 0.19 % cost. No other hour of the 24 scanned comes close: the next strongest are 18:00 to 21:00 closes at t -2.0 to -2.4. The pooled t's are overstated because the 6 coins move together.
- **F2:** The 01:00 reversal does not last beyond a day. Over 72 hours the slope's t is 0.0 and the top-third reversal is 7 bps (t 0.4, 5604 cases). By year its top third is positive in 6 of 8 years (52 to 84 bps, t 2.4 to 4.1) and flat in 2022 (-8 bps) and 2024 (0 bps).
- **F3:** The daily (00:00 to 00:00) 1-day vol-scaled return reverses over the next day (slope t -4.0, top third -22 bps, 14310 cases). This comes entirely from high-volatility periods: in the top tercile of 20-day volatility against its past 120 days, the largest moves reverse by 54 bps (t 2.7, 938 cases), against -6 bps (t -0.4) in the lowest tercile.
- **F4:** Hourly bars closing at 22:00 and 23:00 UTC rise by +5.5 and +4.4 bps (t 6.9 and 5.8). This holds in each coin (t 3.0 to 4.6) and in 7 of 8 years. At about 10 bps over the two hours, the rise is below a round trip's cost (F2 of the runs).
- **F5:** Five-day and 20-day returns continue weakly over 3 to 10 days (t 2.0 to 2.9). The top third's sign swings by year: for 10 days after a 5-day move it is -299 to +826 bps. I count this as not distinguishable from chance.
- **F6:** The book earned in 2018 to 2020 (+7 to +23 bps a day) and lost in 2021, 2022, 2023 and 2025 (-1.7 to -13 bps a day). It beat holding the coin only in 2018, 2019 and 2022, the years when the coin fell or barely rose.
- **F7:** By weekday, the close-to-close day ending Saturday 00:00 is +24 bps (t 2.6), and the days ending Tuesday and Thursday 00:00 are -24 and -28 bps (t -2.4, -2.3). With 7 groups and coins pooled, I do not count this as a finding to build on.

## Ideas
- `017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal.g1_night-move-reverses-next-day` (from F1, F2): The 3-hour return from 22:00 to 01:00 UTC, relative to the coin's usual 3-hour move, is followed by a move the opposite way over the next 24 hours. The larger the night move in usual moves, the larger the move back.
- `017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal.g2_turbulent-days-reverse-next-day` (from F3): When a coin's 20-day volatility is high relative to its past 120 days, its 1-day return relative to its usual daily move is followed by a move the opposite way over the next day. The larger the day's move, the larger the move back.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
