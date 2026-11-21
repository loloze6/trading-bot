---
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week_4h
idea tested: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4223 USD
---
## Findings
- **F1:** Downward breakouts are followed by rises, not by continued falls. Over the next 18 bars (3 days), 4h closes below the lowest low of the preceding 12 bars had a mean unusual move of +1.33 % (t 2.57, 320 non-overlapping cases). Upward breakouts had +0.42 % (t 0.83, 385 cases), and bars with no breakout had −0.20 % (t −1.71, 4875 cases).
- **F2:** The rebound after a downward breakout grows with how busy the past week was against the past two months, and the grading is the strongest pattern found. Ranked by the 60-day/7-day mean-range ratio, from busiest week to quietest, the quarters of downward breakouts had 3-day unusual moves of +5.47 % (t 4.57, 57 cases), +1.68 % (t 1.89), +1.17 % (t 0.89) and −0.68 % (t −0.56). The Spearman correlation of busyness with the unusual move is 0.24 (p 0.0002, 227 cases).
- **F3:** The busy-week rebound after a downward breakout holds on every coin and in most years. In the busy half, the mean 3-day unusual move is +2.7 % to +5.7 % on all 6 coins (t 1.47 to 2.29). It is positive in 7 of the 8 years, with t 4.97 in 2022 and t 3.71 in 2025; 2018 was −0.95 % (t −0.41).
- **F4:** The busy-week rebound already shows over one day. Downward breakouts in the busiest quarter had +1.98 % unusual move over the next 6 bars (t 3.51, 187 cases), while the other three quarters had −0.64 % to −0.90 %.
- **F5:** The rebound is large against the cost of a trade. A round trip cost this backtest 0.19 %, so the busiest-quarter unusual move of +5.47 % over 3 days is about 29 times that cost. Its strength is roughly 0.6 of the coins' usual 3-day move of 6 to 10 %, far above the usual 0.05 of earlier findings.
- **F6:** On all bars, a busy past week is followed by a rise and a quiet past week by a fall, but this is not stable across years. The busiest quintile of the range ratio had +0.85 % 3-day unusual move (t 2.47, 858 cases) and the quietest −0.71 % (t −2.51). The per-coin Spearman correlations are only 0.02 to 0.08, and the busiest quintile was negative in 2018 (t −2.34) and 2019 (t −2.77).
- **F7:** The tested idea's grading by a quiet week is weak for upward breakouts. Upward breakouts in the quietest quarter had +1.95 % (t 2.01, 73 cases), but the quarters below did not rise in order (+0.25 %, −0.75 %, +1.18 %).
- **F8:** Time-of-day and weekday patterns are strong in t but too small to pay. The 16:00 UTC bar's next-bar unusual move is +7.7 bps (t 5.15) and the 20:00 bar's is −7.1 bps (t −4.62); Fridays average +7.9 bps per 4h bar (t 4.83). All are below the 19 bps round trip, so they are not ideas a book could pay on.
- **F9:** The book's worst days are followed by a rise in the coin. In the book's lowest daily-return decile (book −2.6 %, coin −5.1 % that day), the coin returned +0.53 % the next day on average. This is consistent with F1's rebound after sharp falls.

## Ideas
- `019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week.g1_busy-week-downside-break-rebound` (from F1, F2, F3, F4, F5, F9): When a coin's four-hour bar closes below the lowest low of its preceding two days, the coin rises over the next three days. The rise is larger the busier its average four-hour range over the past 7 days was compared with its average over the past 60 days.
- `019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week.g2_busy-week-then-rise` (from F6, F2): A coin rises over the next three days by more the busier its average four-hour range over the past 7 days was compared with its average over the past 60 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
