---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin's four-hour bar closes below the lowest low of its preceding two days, the coin rises over the next three days. The rise is larger the busier its average four-hour range over the past 7 days was compared with its average over the past 60 days.
Consequence: A trader should treat a downside break after a volatile week as a buying opportunity sized by how busy that week was, and should refuse to short it.
Why:
- F1: Downward breakouts are followed by rises, not by continued falls. Over the next 18 bars (3 days), 4h closes below the lowest low of the preceding 12 bars had a mean unusual move of +1.33 % (t 2.57, 320 non-overlapping cases). Upward breakouts had +0.42 % (t 0.83, 385 cases), and bars with no breakout had −0.20 % (t −1.71, 4875 cases).
- F2: The rebound after a downward breakout grows with how busy the past week was against the past two months, and the grading is the strongest pattern found. Ranked by the 60-day/7-day mean-range ratio, from busiest week to quietest, the quarters of downward breakouts had 3-day unusual moves of +5.47 % (t 4.57, 57 cases), +1.68 % (t 1.89), +1.17 % (t 0.89) and −0.68 % (t −0.56). The Spearman correlation of busyness with the unusual move is 0.24 (p 0.0002, 227 cases).
- F3: The busy-week rebound after a downward breakout holds on every coin and in most years. In the busy half, the mean 3-day unusual move is +2.7 % to +5.7 % on all 6 coins (t 1.47 to 2.29). It is positive in 7 of the 8 years, with t 4.97 in 2022 and t 3.71 in 2025; 2018 was −0.95 % (t −0.41).
- F4: The busy-week rebound already shows over one day. Downward breakouts in the busiest quarter had +1.98 % unusual move over the next 6 bars (t 3.51, 187 cases), while the other three quarters had −0.64 % to −0.90 %.
- F5: The rebound is large against the cost of a trade. A round trip cost this backtest 0.19 %, so the busiest-quarter unusual move of +5.47 % over 3 days is about 29 times that cost. Its strength is roughly 0.6 of the coins' usual 3-day move of 6 to 10 %, far above the usual 0.05 of earlier findings.
- F9: The book's worst days are followed by a rise in the coin. In the book's lowest daily-return decile (book −2.6 %, coin −5.1 % that day), the coin returned +0.53 % the next day on average. This is consistent with F1's rebound after sharp falls.
