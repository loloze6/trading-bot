---
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound_1h
idea tested: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4194 USD
---
## Findings
- **F1:** Around the midnight UTC settlement (bars closing at 00:00–02:00 UTC), the 2-hour move reverses over the next 8 hours on both sides and in proportion to its size. The lowest decile of the scaled 2-hour return (z −2.74) is followed by +22.7 bp drift-removed (strength +0.078). The highest decile (z +2.85) is followed by −33.9 bp (strength −0.121), monotone across deciles, about 4,740 cases per decile. At the 01:00 close, the product of the reversal and the move is positive in all 6 coins (t 2.0 to 2.8, about 2,650 cases each). It is positive in 2018–2021 and 2023 (t 2.3 to 5.5) and faded in 2022, 2024 and 2025 (t 0.1, −0.3, 0.9).
- **F2:** The rise side of the midnight reversal is the strongest single reading in the hour scan. After a 2-hour rise, the 8-hour product t is −6.81 at the 01:00 close, −5.14 at 02:00 and −3.89 at 00:00 (about 7,500–8,000 cases each). This short side is not in the tested long-only idea, and its top-decile move (−33.9 bp) is about 1.8 times the 0.19 % trade cost.
- **F3:** At the 16:00 close the 24-hour move continues over the next 8 hours, and mostly at the extreme. The top quintile of the scaled 24-hour return (z24 +1.90) is followed by +33.8 bp (strength +0.119); the middle quintiles give −1.9 to −0.2 bp; the bottom quintile gives +8.4 bp (about 3,170 cases each). The 24-hour continuation product is positive at closes 15–18 (t 1.6, 3.25, 2.14, 2.36). It is positive in all 6 coins (t 0.7 to 1.9) and in 7 of 8 years.
- **F4:** During the Asian and European night the 24-hour move reverses instead. The 24-hour continuation product over 8 hours is negative at every close from 00:00 to 09:00 UTC, with t −2.1 to −5.0 (about 15,700 cases each hour). This is the opposite sign to the 15–18 UTC afternoon in F3.
- **F5:** The late evening UTC carries a strong upward drift, graded by the coin's 24-hour fall. The 1-hour return after the 21:00 close is +5.45 bp (t 6.75) and after the 22:00 close +4.36 bp (t 5.66). The 3 hours after the 20:00 close are positive in all 6 coins (+5.7 to +8.8 bp). They are largest after the deepest 24-hour falls: bottom quintile (z24 −1.83) +20.0 bp, falling to +0.9 to +3.3 bp in the upper quintiles (about 3,165 cases each). The drift is strong in 2020, 2021 and 2024 (t 5.5, 2.7, 4.4) and flat in 2018 and 2023.
- **F6:** The tested afternoon trade's edge is about the size of its cost. Gross trade returns per coin are +0.12 % to +0.67 %, and net of fees +0.02 % to +0.57 % (XMR +0.02 %, BTC +0.06 %). Yet the book's daily Sharpe is −0.02. It lost most in 2022 (−13.6 bp a day against the coins' −18.6), which matches an unusual move per case (+0.19 %) only 1.0 times the 0.19 % cost.
- **F7:** Volume concentrates around the afternoon UTC hours, as the brief expects. The median volume against its 720-bar median is 1.49–1.53 at closes 15–17 and 1.14 at 01:00, against 0.67–0.83 at closes 04–12.

## Ideas
- `017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound.g1_midnight-two-hour-move-reversal` (from F1, F2): In the hours around midnight UTC, a coin's 2-hour move reverses over the next 8 hours on both sides. The larger the 2-hour move against the coin's usual 2-hour move, the larger the opposite move, and the largest after a rise.
- `017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound.g2_afternoon-day-trend-continuation` (from F3, F4, F7): At the 16:00 UTC settlement, a coin's 24-hour return continues over the next 8 hours. The larger the 24-hour rise against the coin's usual 24-hour move, the larger the further rise.
- `017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound.g3_night-session-day-trend-reversal` (from F4): Between midnight and 09:00 UTC, a coin's 24-hour return reverses over the next 8 hours. The larger the 24-hour move against the coin's usual 24-hour move, the larger the move back.
- `017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d2_afternoon-settlement-fall-rebound.g4_evening-rebound-after-daily-fall` (from F5): After the 20:00 UTC close, a coin rises over the next 3 hours. The deeper its 24-hour fall against its usual 24-hour move, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
