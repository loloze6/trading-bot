---
line: 7.g patterns
backtest: 028-03_low-volume-up-fade.d1_high-volume-drop-rebounds_1h
idea tested: 028-03_low-volume-up-fade.d1_high-volume-drop-rebounds
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4250 USD
---
## Findings
- **F1:** The 24-hour move reverses over the next 24 hours, graded. On a non-overlapping 24-hour grid, the coin's next-24-hour unusual move falls with its past 24-hour return (scaled by its 30-day hourly volatility × √24). The bottom quintile is followed by +31.6 bp for BTC (t 1.77, 516 cases) and +45.9 bp for ETH (t 1.89, 551 cases). The top quintile is followed by −20.7 bp for BTC (t −1.39) and −16.4 bp for ETH (t −0.91). The correlation is negative in 6 of 8 years (−0.03 to −0.11) and near zero in 2022 (+0.01) and 2024 (+0.02). This is about 0.06 on about 5,300 cases, an estimated t of about −4 that I did not compute directly. The move per case is several times the 0.11 % cost of a trade.
- **F2:** The hour after the 20:00 and 21:00 UTC closes rises more than the coin's normal hourly drift. It does so for BTC (+3.7 bp, t 3.81, 5837 cases) and for ETH (+4.8 bp, t 3.92, 5837 cases). It is positive in 7 of 8 years (2022: −3.1 bp, t −1.45) and on all 7 weekdays (+3.4 to +5.3 bp). These are the two highest of the 24 hours tested (t 4.0 and 3.7). Even so, 4 to 5 bp an hour is well below the 0.11 % cost of a trade.
- **F3:** The hours after 00:00 to 02:00 UTC fall more than the drift. The 02:00 hour is at −3.2 bp (t −3.35), and the three hours together are negative in 2018 (t −3.35), 2021 (t −2.74) and 2022 (t −2.53). They are flat or positive in 2024 and 2025 (+0.07 and +1.3 bp), so this pattern is fading.
- **F4:** The tested rebound is graded across falls of at least 1.5 usual moves. Ranked by fall × volume ratio, the 2-hour unusual moves by quintile are −1.2, +7.8, +4.8, +17.0 (t 2.01) and +27.0 bp (t 2.72), each on about 594 cases. But the extreme cases (fall beyond 2.5 usual moves on more than 4× volume) earn their gain in 2020 (+95.6 bp, t 2.59) and 2021 (+122.5 bp, t 1.83). They are negative in 2023 to 2025 (−1.1, −3.1, −13.8 bp).
- **F5:** The book's largest positions earn the least per trade. The trades entered at the highest forecasts (14.8 to 20, 15485 trades) gain +0.027 % before fees and lose −0.073 % after. Those entered at 1.6 to 5.4 (5162 trades) gain +0.248 % before fees and +0.148 % after. The top-forecast trades are negative before fees in 2019 and in every year from 2022 to 2025. The cubed forecast thus spends most of its turnover on the cases that pay least.

## Ideas
- `028-03_low-volume-up-fade.d1_high-volume-drop-rebounds.g1_daily-move-reverses-next-day` (from F1, F4): The further a coin's 24-hour return lies below its usual 24-hour move (its 30-day hourly volatility scaled to 24 hours), the more it rises over the next 24 hours. The further above, the more it falls.
- `028-03_low-volume-up-fade.d1_high-volume-drop-rebounds.g2_heavy-volume-day-fall-rebounds` (from F1, F4): The coin's return over the next two hours rises with how far its 24-hour volume-weighted fall reaches beyond its usual 24-hour move. Here the fall is each hour's return over the past 24 hours in 30-day standard deviations, weighted by that hour's volume against its 30-day average and summed.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
