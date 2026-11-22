---
line: 7.g patterns
backtest: 028-02_volume-surge-down-continuation.d1_heavy-volume-plunge-rebounds_1h
idea tested: 028-02_volume-surge-down-continuation.d1_heavy-volume-plunge-rebounds
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5744 USD
---
## Findings
- **F1:** The coin's hour starting 20:00 UTC rises more than usual, by +4.5 bps (t 4.0, n 5834), and so does the hour starting 21:00, by +4.0 bps (t 3.7, n 5840). This is the largest of 24 hours tested and holds in both coins (BTC +3.7 bps, t 3.8; ETH +4.8 bps, t 3.9), on every weekday (+3.4 to +5.3 bps), in 7 of 8 years (2022 is the exception at −3.1 bps), and in 81 % of the 48 coin-windows. Those two hours are where the book makes its own best bar returns (+3.1 and +2.7 bps), against mostly negative bars in the other hours.
- **F2:** The evening rise is graded by how the coin's past 20 hours went. The two hours after the 19:00 bar's close rise +3.5 bps above drift overall (t 2.1, n 5356), +11.4 bps (t 2.2) after the weakest fifth of 20-hour returns scaled by the 30-day hourly volatility, and −0.9 bps (t −0.3) after the strongest fifth, falling almost steadily in between (3.4, 3.3, 0.2). In the most volatile fifth of hours the evening rise is +18.0 bps (t 3.2). Only these conditioned cases reach the 11 bps cost of a trade.
- **F3:** The coin's 24-hour return, scaled by its 30-day hourly volatility, reverses over the next 24 hours. After the lowest quintile the next 24 hours run +38.7 bps above drift (t 2.5, n 1063); after the fourth quintile they run −24.1 bps (t −2.1). The slope is −22.5 bps per unit of the scaled past return. The two lowest deciles give +36 and +46 bps, in both coins (BTC +31.5 bps, t 1.8; ETH +50.6 bps, t 2.1) and in 7 of 8 years (2022: −17 bps). The reversal is absent over 6 hours (slope −1.5 bps) and over 72 hours (slope +17 bps). At 24 hours its move per case is about 3 to 4 times the 11 bps cost of a trade.
- **F4:** The coin falls more than usual in the hours starting 00:00, 01:00 and 02:00 UTC, by −2.2 bps (t −2.0), −2.3 bps (t −2.2) and −3.2 bps (t −3.3). This held in 2018 through 2023 (2018 −7.4 bps, t −3.3; 2021 −5.9 bps, t −2.7; 2022 −4.2 bps, t −2.5), but not in 2024 and 2025 (+0.1 and +1.3 bps). The book holds about 0.34 of its value long through these hours and loses 0.6 to 2.2 bps per bar there.
- **F5:** The tested signal's edge is concentrated in its extreme cases and does not survive the book.

## Ideas
- `028-02_volume-surge-down-continuation.d1_heavy-volume-plunge-rebounds.g1_weak-day-evening-rebound` (from F1, F2): The more a coin has fallen over its past 20 hours, measured against its typical hourly move over the past 30 days, the more it rises over the two hours from 20:00 to 22:00 UTC.
- `028-02_volume-surge-down-continuation.d1_heavy-volume-plunge-rebounds.g2_one-day-fall-reverses` (from F3, F5): The larger a coin's fall over its past 24 hours, measured against its typical move over 24 hours from its last 30 days of hourly returns, the larger its rise over the next 24 hours.
- `028-02_volume-surge-down-continuation.d1_heavy-volume-plunge-rebounds.g3_evening-rally-fades-overnight` (from F1, F4): The larger a coin's rise over the evening hours 20:00–24:00 UTC, measured against its typical hourly move over the past 30 days, the more it falls over the following three hours from 00:00 to 03:00 UTC.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
