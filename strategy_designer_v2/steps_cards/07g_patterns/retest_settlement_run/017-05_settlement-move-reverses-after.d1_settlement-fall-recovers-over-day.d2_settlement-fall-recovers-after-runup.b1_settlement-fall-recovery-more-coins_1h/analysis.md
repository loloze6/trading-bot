---
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins_1h
idea tested: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5415 USD
---
## Findings
- **F1:** On a non-overlapping daily grid over all coins and windows, a coin's 24-hour return, counted in its usual 24-hour moves, correlates −0.067 with its excess return over the next 24 hours (t −12.7, 35 122 cases). The reversal sits in the coin's most volatile third of its 7-day hourly volatility: corr −0.125 (t −13.6), and among falls alone corr −0.161 (t −12.4), with a mean next-day excess of +0.115 usual moves. In the calmest third, falls have −0.042 usual moves and corr +0.027.
- **F2:** This day-long reversal is broad and has weakened over time. Ten coins show it with t below −3.5: XMR −6.8, ETH −5.5, TRX −5.0, BTC −4.6, LTC −4.5, ADA −3.9, ZEC −3.8, UNI −3.7, LINK −3.5, XRP −3.5. Among falls in the volatile third, corr is −0.227 (t −12.6, 2 931 cases) in 2018–2021 and −0.043 (t −2.3, 2 881 cases) in 2022–2025. It is near zero on AVAX, INJ, NEAR, SOL, DOGE and TAO.
- **F3:** A fall is reversed more when it came on heavy volume. When the 24-hour volume is in the top third against its 7-day daily pace, the fall's size correlates −0.180 with the next-day excess return (t −13.6, 5 560 cases, mean +0.075 usual moves). In the lowest third, the correlation is −0.063 (t −4.8, mean −0.026).
- **F4:** The tested signal is not tied to the funding clock. At closes of 00:00 and 16:00 UTC its next-day excess has t 0.57 and 2.67. At non-settlement closes it is as strong or stronger: 01:00 at t 5.0, 02:00 at t 4.9, 15:00 at t 3.7, 12:00 at t 3.3. This is the brief's own third falsifier, and the tested gain looks like the general reversal in F1.
- **F5:** In calm coins, the move continues instead of reversing. In the least volatile third, the 3-day return in usual 24-hour moves correlates +0.069 with the next-day excess (t 7.5, 11 713 cases), and the 24-hour return +0.048 (t 5.2). In the most volatile third, the same correlations are −0.068 and −0.125.
- **F6:** The book's best days depend on strong run-ups. On its top 5 % of active days, the coin's prior 7-day return averaged +25.0 %, against +6.4 % on all active days. On its worst 5 % of days, the prior 7-day return averaged +5.1 % and the coin fell 7.2 % that day.
- **F7:** Size against cost. A fall in the volatile third earns +0.115 of a usual 24-hour move (about 5.5 %), which is about 0.6 % per case, near 2.9 times the 0.22 % cost of a trade. The tested idea's strength was 0.024 (an unusual move of 0.6 times the cost).
- **F8:** One hour of the day stands out across all 24 hours tested. The 1-hour return of the bar starting 22:00 UTC is +0.054 of a usual hourly move (t 10.7), and the bar starting 21:00 is +0.037 (t 7.0). At a fraction of a usual hourly move, this is far below the cost of a trade.

## Ideas
- `017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins.g1_volatile-day-fall-reverses` (from F1, F2, F4, F7): Over the next 24 hours, a coin rises after falling over the past 24 hours, by more the larger that fall is against its usual 24-hour move. The rise is larger the higher the coin's hourly volatility over the past 7 days.
- `017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins.g2_heavy-volume-fall-reverses` (from F3, F1, F7): Over the next 24 hours, a coin rises after falling over the past 24 hours, by more the larger that fall is against its usual 24-hour move. The rise is larger the more that day's volume exceeds its daily average over the past 7 days.
- `017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day.d2_settlement-fall-recovers-after-runup.b1_settlement-fall-recovery-more-coins.g3_calm-coin-trend-continues` (from F5): In a coin whose hourly volatility over the past 7 days is low against its own history, its 3-day return continues over the next 24 hours. The continuation is larger the larger that 3-day move is against the coin's usual 24-hour move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
