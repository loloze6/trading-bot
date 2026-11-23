---
line: 7.g patterns
backtest: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d3_much-heavier-weekend-continuation_1h
idea tested: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d3_much-heavier-weekend-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.6923 USD
---
## Findings
- **F1:** A coin's 24-hour move is followed by a reversal over the next 24 hours, and the reversal grows steeply with the size of the move. On the non-overlapping 24-hour grid, the move against the past 24 hours, in units of the coin's usual daily move, is:
- **F2:** The reversal after the 10 % largest 24-hour moves is spread rather than carried by one coin or period.
- **F3:** Among these large moves, the reversal is about twice as large when the past day's hourly volatility is high against its 30-day level. In the highest tercile of that ratio (mean 2.15) it is +0.329 usual moves. In the lower two terciles it is +0.163 and +0.168. Each tercile has about 522 cases.
- **F4:** Every coin tends to rise over the two hours 21:00–23:00 UTC.
- **F5:** The 21:00–23:00 rise is concentrated where the past day's volatility is high against its 30-day level.
- **F6:** The tested signal's Monday-morning continuation comes from the weekend's volume and not from the size of the weekend's move.
- **F7:** The book's gain rests on a few days.

## Ideas
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d3_much-heavier-weekend-continuation.g1_extreme-daily-moves-reverse` (from F1, F2): A coin's move over the past 24 hours is partly reversed over the next 24 hours. The reversal grows steeply with the size of that move against the coin's usual daily move, and is largest after the rarest moves.
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d3_much-heavier-weekend-continuation.g2_volatile-burst-moves-reverse-more` (from F1, F3): A coin's large move over the past 24 hours is reversed more over the next 24 hours the higher the past day's hourly volatility is against its own last 30 days.
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d3_much-heavier-weekend-continuation.g3_volatile-day-late-evening-rise` (from F4, F5): A coin rises over the two hours from 21:00 to 23:00 UTC. The rise grows with how high the coin's past-day hourly volatility is against its last 30 days.
- `026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins.d2_heavy-weekend-monday-morning-continuation.d3_much-heavier-weekend-continuation.g4_weekend-volume-drives-continuation` (from F6, F7): A coin's Saturday–Sunday move continues over the first 12 hours of Monday more strongly the heavier the weekend's hourly volume is against the five weekdays before it, whatever the size of the move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
