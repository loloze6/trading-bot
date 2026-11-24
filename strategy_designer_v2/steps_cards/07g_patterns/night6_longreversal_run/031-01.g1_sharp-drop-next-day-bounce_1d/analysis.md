---
line: 7.g patterns
backtest: 031-01.g1_sharp-drop-next-day-bounce_1d
idea tested: 031-01.g1_sharp-drop-next-day-bounce
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3998 USD
---
## Findings
- **F1:** Wide-range days that close near their low are followed by a rise the next day, and the effect grows with the range. In a day-clustered regression of next-day excess return on close position (close minus the day's midpoint, as a share of the range), close position × range (range in 30-day usual moves) and today's move in usual moves, the interaction is −0.0131 (t −3.13) and close position alone is +0.0134 (t 2.20). The sample is 14,500 bars on 2,418 days. Today's move is +0.0010 (t 0.79), so this is not the tested fall-size effect. At a range of about two usual moves, a close at the low rather than the midpoint means roughly +0.6 % more the next day; at a range of one usual move the effect is about zero.
- **F2:** Without the range, close position barely counts. The lowest fifth of close positions is followed by +0.35 % next-day excess (t 2.26, n 3,454) and the highest fifth by −0.22 % (t −1.69, n 3,487). But the linear close-position slope, controlling today's move, is −0.0013 (t −0.36), and per coin it is no clearer: every coin's t lies between −1.33 and +0.70. The effect sits in wide-range days only (F1).
- **F3:** The tested reversal lives on down days and has no mirror on up days. Falls of 0.75 to 1.5 usual moves are followed by +0.45 % next-day excess (t 2.30, n 1,772), while the slope of next-day excess on up-day size is +0.063 % per usual move (t 0.82, n 7,335). The tested fall-size slope, controlling close position, is +0.39 % per usual move (t 1.55, 7,151 bars on 1,835 days).
- **F4:** The brief's own horizon shows no lean against the earlier move. On a 20-day grid, next-20-day excess rises with the 60-day move in usual moves, from −3.43 % (t −1.32, n 77) in the lowest fifth to +2.56 % (t 0.69, n 76) in the highest. That ordering is the trending side, but no fifth reaches |t| 1.4.
- **F5:** Continuation of the 5-day move does not stand out after the many angles looked at. Controlling today's move, the pooled slope of next-day excess on the 5-day move in usual moves is +0.0019 (t 2.05), while today's move reverses at −0.0028 (t −3.06). Per coin the 5-day slope ranges from −0.11 % to +0.24 %, all with |t| ≤ 1.45.
- **F6:** The book's gain is uneven across years, and its extreme days follow large coin moves. Mean daily book return was 0.17 % in 2020, 0.14 % in 2021 and 0.11 % in 2023, against about 0.00 % in 2018, 2019, 2022 and 2025. On the book's worst 2 % of days the coins averaged −8.84 %, and on its best 2 % they averaged +8.09 %. Weekday, volatility level and per-volatility fall-size slopes showed nothing beyond chance: every |t| ≤ 2.09 among 7, 4 and 4 groups.

## Ideas
- `031-01.g1.g1_wide-range-low-close-bounce` (from F1, F2, F3): The wider a coin's daily high-to-low range compared with its 30-day usual daily move, and the nearer to that day's low it closes, the more it rises over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
