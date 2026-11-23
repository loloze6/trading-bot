---
line: 7.g patterns
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation_1h
idea tested: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5501 USD
---
## Findings
- **F1:** On Sundays with the thinnest weekend volume against the five weekdays before (lowest quartile of the 48h over prior-120h volume ratio), the Saturday-Sunday move reverses over the next 48 hours: mean signed return −0.80 % (t −2.91, 473 non-overlapping cases). The reversal is negative in 5 of 6 coins (ETH −1.13 %, LTC −1.18 %, XMR −1.35 %, XRP −1.02 %, BTC −0.43 %) and in 6 of 8 years. Its size is about four times the 0.19 % cost of a trade.
- **F2:** The reversal is graded by thinness and by move size. Over all 1,890 Sundays, the volume ratio's rank correlates with the signed 48-hour return at rho +0.078 (p 0.0007): heavy weekends continue, thin ones reverse. Among the 1,563 light weekends, a larger move is followed by a lower signed 48-hour return (rho −0.10, p 0.00006). Even inside light weekends, the thinnest quartile reverses (−0.79 %, t −2.54) while the least-thin quartile does not (+0.54 %, t 1.48).
- **F3:** The tested continuation is confined to the heaviest weekends and to the first 12 hours.
- **F4:** Two hours of the day stand out from the 24 hours examined, across 6 coins and about 17,400 hourly returns each. The hours starting 20:00 and 21:00 UTC have the largest mean returns: +0.055 % (t 6.75) and +0.044 % (t 5.66).
- **F5:** That 20:00–22:00 UTC rise is graded by the preceding 20 hours. After the coin's largest 20-hour falls (lowest quintile) it averages +0.18 % (t 4.78, 3,201 cases). It is +0.05 % in the next quintile (t 2.30) and about 0 after rises. At its strongest, the move per case is about the 0.19 % cost of one trade.
- **F6:** The book's losses are concentrated in its exposure on Monday, where it holds its positions. 77 of its 116 worst 5 % days are Mondays. Its mean return on days in a position is negative in 2018 (−0.041 %, t −1.49, 594 days) and in 2023 (−0.116 %, t −1.23), which explains the weak Calmar.

## Ideas
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.g1_thin-weekend-moves-reverse` (from F1, F2, F6): A coin's Saturday-Sunday move is reversed over Monday and Tuesday. The reversal over the next 2 days is larger the lighter the weekend's hourly volume is against its mean over the preceding five weekdays, and the larger the weekend move.
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.g2_evening-rebound-after-daily-falls` (from F4, F5): A coin's fall over its preceding 20 hours is followed by a rise over the next 2 hours from 20:00 UTC. The rise is larger the deeper the 20-hour fall, measured in the coin's usual moves.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
