---
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less_1h
idea tested: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3769 USD
---
## Findings
- **F1:** Among 3-day rises (72-hour return above 0, non-overlapping 72-bar grid, per-coin quintiles), the path efficiency of the rise, meaning the net log move over the sum of absolute hourly log moves, orders the next 3 days' coin-demeaned return monotonically. The least efficient quintile shows −0.0044 (t −1.29, n 575) and the most efficient shows +0.0113 (t 2.78, n 574). That is a top-minus-bottom gap of about +0.0157 (Welch t ≈ 2.96, worked out from the reported means and standard deviations).
- **F2:** The tested measure, read by quintile instead of the plan's median split, shows the same monotonic ordering. The next 3-day demeaned return goes from +0.0107 (t 2.75, n 575) when the 3 biggest hours carry the smallest share of the rise to −0.0061 (t −1.79, n 574) when they carry the largest. The gap is about +0.0168 (Welch t ≈ 3.2). The median split dilutes this to +0.0047 (t 0.83), so the effect sits in the tails.
- **F3:** Over all bars, signed path efficiency (efficiency × sign of the 3-day return) has its top quintile followed by +0.0074 demeaned 72-hour return (t 2.74, n 1108), against −0.0054 (t −2.17) in the middle quintile. Efficient rises are the bars that drift on.
- **F4:** Among 3-day falls, the least efficient (choppiest) quintile is followed by −0.0089 demeaned return (t −2.47, n 536). The most efficient falls are followed by +0.0010 (t 0.25). The top-minus-bottom gap is only about t ≈ −1.9, so this does not stand out given the number of angles tried.
- **F5:** The size of the 3-day move gives a U-shape, not a gradient. The middle quintile is followed by −0.0077 (t −3.55, n 1107), the top quintile by +0.0067 (t 2.27) and the bottom by +0.0029 (t 1.05).
- **F6:** Pooled across coins, the next-hour demeaned return is high after the 20:00 and 21:00 UTC bars (+0.00048, t 5.98; +0.00037, t 4.85, about 17,400 bars each). It is low after the 13:00 and 02:00 bars (−0.00042, t −4.46; −0.00034, t −4.65). By weekday, Friday is +0.00020 (t 4.46) and Thursday is −0.00021 (t −4.60). These are not graded situations.
- **F7:** The book's mean daily return is below holding for every coin (for example BTC 0.00076 vs 0.00118). LTC's book is negative (−0.00009 vs +0.00067). Its edge comes from being flat about 57–66% of the grid bars, not from adding return.

## Ideas
- `016-03_up-jump-price-reversal.d2_jump-rises-continue-less.g1_efficient-rises-keep-drifting` (from F1, F3, F2): When a coin has risen over the past 3 days, the more efficiently it got there, meaning the closer its net 3-day move is to the sum of its absolute hourly moves, the larger its rise over the next 3 days.
- `016-03_up-jump-price-reversal.d2_jump-rises-continue-less.g2_jump-built-rises-underperform` (from F2, F1): When a coin has risen over the past 3 days, the larger the share of that rise carried by its 3 biggest hourly gains, the smaller its return over the next 3 days, falling below the coin's usual 3-day return when that share is largest.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
