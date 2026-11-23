---
line: 7.d confirmed, not profitable
backtest: 017-05_settlement-move-reverses-after_1h
idea tested: 017-05_settlement-move-reverses-after
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5669 USD
---
## Findings
- **F1:** The move per case is far too small to pay for a trade, so the book loses before any choice of sizing. The idea's total move is +0.05 % per case over 2 hours, which is 0.2 times the 0.19 % cost of a trade. The book made 65 566 trades, a median of 120 minutes each, averaging −0.078 % before fees and −0.178 % after. Sharpe was −3.97, the mean daily return on days in a position −0.2 %, and the yearly return −51.9 %.
- **F2:** The short side loses before fees and the long side carries all the gross gain. SHORT trades averaged −0.303 % gross (−0.403 % net, 32 573 trades). LONG trades averaged +0.144 % gross (+0.044 % net, 32 993 trades). At the 00:00 and 16:00 settlements over 8 hours, a fall into settlement in the 50–95th percentile of |pre-move| was followed by +21.5 bp and +23.1 bp total (unusual +16.8 bp, t 4.13, n 5 007; +18.5 bp, t 2.83, n 2 559). A rise in the same bands was followed by only +4.4 bp and +2.9 bp, and by −0.5 bp to +3.7 bp over 16 hours.
- **F3:** The effect on the long side grows with the horizon past the 2 hours the book holds, and with the size of the fall, until the extreme 1 %. For falls into settlement on the long side, the total move was:
- **F4:** The 08:00 UTC settlement carries none of the effect.
- **F5:** The move reverses when it runs against the coin's 24-hour trend, the crowded-side reading the brief gives, and it grows with the strength of that trend.
- **F6:** The settlement clock adds most in the middle band of falls. Falls in the 50–80th percentile at hours away from settlement gave +7.2 bp total and +2.6 bp unusual over 8 hours. At the 00:00 and 16:00 settlements the same band gave +21.5 bp and +16.8 bp. In the 80–95 band other hours gave +19.9 bp, close to settlement's +23.1 bp.
- **F7:** The long-side gain at 00:00 and 16:00 over 8 hours, 50–99th percentile of falls, is positive in 7 of 8 years. It ranges from +4.9 bp in 2025 to +44.5 bp in 2018; 2022 was the exception at −15.9 bp (n about 1 000–1 200 per year). So it does not rest on one period.
- **F8:** The book's gross gain sits entirely in the first 2 hours after settlement, at +0.38 and +0.75 bp per bar with a mean |allocation| of 0.43. The other six hours hold about 0.014 and earn about 0. The book pays the full cost every 8 hours for a 2-hour move, and that move is below the cost.

## Ideas
- `017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day` (from F1, F2, F3, F4, F7, F8): The return over the 24 hours after the 00:00 and 16:00 UTC funding settlement times runs opposite to a fall over the 2 hours before it: the coin rises after falling into settlement, and the larger the fall against the coin's usual 2-hour move, the larger the rise.
- `017-05_settlement-move-reverses-after.d2_counter-trend-settlement-move-reverses` (from F1, F4, F5, F8): The return over the 8 hours after each funding settlement time runs opposite to the return over the 2 hours before it when that pre-move runs against the coin's 24-hour trend, and the stronger the 24-hour trend, the larger the move back.
- `017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours` (from F2, F3, F4, F6, F8): The return over the 8 hours after the 00:00 and 16:00 UTC funding settlement times runs opposite to a fall over the 2 hours before it, and the larger the fall against the coin's usual 2-hour move, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
