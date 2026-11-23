---
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d3_settlement-recovery-lasts-one-day_1h
idea tested: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d3_settlement-recovery-lasts-one-day
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3989 USD
---
## Findings
- **F1:** When a coin's past-week hourly volatility is in its top third, its 24-hour return, scaled by that volatility, is followed by a 24-hour move the opposite way: slope −57 bp per unit, t −6.41 over 5633 non-overlapping daily cases at 00:00 UTC. In the lower two thirds the slope is +8 bp (t 1.75) and +5 bp (t 0.88), so the reversal belongs to the high-volatility regime only.
- **F2:** Inside the high-volatility regime the reversal is graded and large. The unusual move in the reversal's direction grows from 0.30 % (strength 0.061) in the smallest quintile of the scaled 24-hour move to 0.73–0.78 % (strength 0.15–0.16) in the top three quintiles, which is up to four times the 0.19 % cost of a trade. It holds after both rises (0.62 %) and falls (0.52 %).
- **F3:** The high-volatility daily reversal does not rest on one year or one coin. Its t is positive in 7 of 8 years (1.9 to 4.6; 2025 −0.26) and is 2.6 to 5.2 in four of six coins (BTC 2.62, ETH 3.30, LTC 2.69, XMR 5.16; XRP 1.56, ZEC 1.02).
- **F4:** The 2-hour move into a 12:00 or 13:00 UTC close reverses over the next 4 hours, with slope t 10.4 and 8.5 (about 16 500 daily cases each), and t above 4 in 6 of 8 years. The effect sits in the largest moves: the top quintile of the scaled 2-hour move gives an unusual 4-hour move of 0.28 % (strength 0.137), while the other quintiles give 0.00–0.08 %.
- **F5:** The 2-hour-move reversal is not tied to funding settlements, against the brief's third test.
- **F6:** After the 00:00–02:00 UTC closes, the second day gives part of the recovery back, with second-day slope t −3.4, −3.1 and −3.2. The tested idea's first-day gain of 0.09 % unusual per case (0.5 times the cost of a trade) is partly undone on the second day.
- **F7:** Hourly returns into the 22:00 and 23:00 UTC closes are positive on average:

## Ideas
- `017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d3_settlement-recovery-lasts-one-day.g1_high-volatility-daily-move-reverses` (from F1, F2, F3): When a coin's hourly volatility over the past week is high against its own history, its 24-hour move is followed by a move the opposite way over the next 24 hours, larger the larger that 24-hour move is against the coin's usual 24-hour move.
- `017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d3_settlement-recovery-lasts-one-day.g2_midday-two-hour-move-reverses` (from F4, F5): A coin's 2-hour move into the 12:00 or 13:00 UTC close is followed over the next 4 hours by a move the opposite way, larger the larger that 2-hour move is against the coin's usual 2-hour move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
