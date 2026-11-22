---
line: 7.g patterns
backtest: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction_1h
idea tested: 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4617 USD
---
## Findings
- **F1:** Sunday's own 24-hour return, read at Monday 00:00 UTC, is reversed over the next 48 hours (slope −0.135 per usual 24-hour move, t −4.70, 2,028 cases); on the other weekdays the same last-24-hour return predicts almost nothing over 48 hours (slopes −0.035 to +0.023, t −1.74 to +1.11).
- **F2:** The Sunday reversal is graded and widespread: by quintile of Sunday's return, the next 48 hours go from +0.165 to −0.179 usual 48-hour moves; the slope is negative for all six coins (XMR −0.258 t −3.57, XRP −0.171 t −2.24, LTC −0.143 t −2.20, BTC −0.063 t −0.93) and in 7 of 8 years (2023 the exception, +0.107 t 1.32).
- **F3:** Saturday's 24-hour return continues over the 48 hours from Monday 00:00 (slope +0.208, t 4.60, 1,789 cases), while the whole weekend's 48-hour return predicts nothing (−0.023, t −0.70). The two halves cancel, so the tested idea's whole-weekend signal is weak.
- **F4:** The Saturday continuation is less steady than the Sunday reversal: it shows in 4 of 6 coins (t 2.27 to 2.75; LTC and ZEC near 0) and in 5 of 8 years (t 2.7 to 5.0), but 2018, 2021 and 2025 are negative (t −0.36 to −1.45).
- **F5:** When a coin's 168-hour realised volatility is in its top quintile, its 24-hour return is reversed over the next 24 hours (slope −0.175, t −11.3, 3,248 cases); in the four lower quintiles the slope is −0.015 to +0.034 (t ≤ 1.7).
- **F6:** The high-volatility 24-hour reversal holds in all six coins (slopes −0.103 to −0.216, t −2.7 to −5.6) and in 7 of 8 years (strongest 2021: −0.262, t −8.3). It is weak in 2023 (44 cases) and 2024 (t −0.58).
- **F7:** The tested idea's gradation shows only at the top: weekends in the top tercile of volatility ratio continue by +0.109 usual 48-hour moves (t 2.23, 596 cases), against −0.037 (t −0.91) in the bottom tercile. This matches the inconclusive verdict (t 1.95).
- **F8:** The book's gains and risks sit on Monday and Tuesday: mean daily return 0.00135 and 0.00075, against −0.00015 to +0.00011 on the other days. 170 of its 176 top-1 % days and 170 of its 174 bottom-1 % days fall on those two days, and the top-1 % days sum to 12.49 against a total of 4.91.
- **F9:** Hours 21:00 and 22:00 UTC rise more than usual (mean +0.048 and +0.039 hourly standard deviations, t 6.18 and 5.31). This holds in all six coins (t 2.6 to 4.0), every weekday and 7 of 8 years. At about 0.04 of an hour's move per hour it is far below the 0.19 % cost of a trade, and it is not graded, so no idea is drawn from it.

## Ideas
- `026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction.g1_sunday-moves-reverse-early-week` (from F1, F2, F8): A coin's return over Sunday (Sunday 00:00 to Monday 00:00 UTC) is partly reversed over the next 2 days. The larger Sunday's move in either direction, the larger the opposite move over Monday and Tuesday.
- `026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction.g2_turbulent-daily-moves-reverse` (from F5, F6): When a coin's hourly volatility over the past 7 days is high, its 24-hour return is partly reversed over the next 24 hours. The reversal is larger the larger that return and the higher that volatility.
- `026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b2_turbulent-weekends-keep-their-direction.g3_saturday-moves-carry-into-week` (from F3, F4, F7): A coin's return over Saturday (Saturday 00:00 to Sunday 00:00 UTC) continues in the same direction over the 2 days after Monday 00:00 UTC. The continuation is larger the larger Saturday's move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
