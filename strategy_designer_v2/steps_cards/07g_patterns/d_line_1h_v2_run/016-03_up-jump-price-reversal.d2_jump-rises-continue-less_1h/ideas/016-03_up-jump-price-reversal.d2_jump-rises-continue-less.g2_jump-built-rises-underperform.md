---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.d2_jump-rises-continue-less_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 3 days, the larger the share of that rise carried by its 3 biggest hourly gains, the smaller its return over the next 3 days, falling below the coin's usual 3-day return when that share is largest.
Consequence: A trader would cut or drop long exposure after rises built on a few violent hours, treating them as below-average holds rather than still-good longs.
Why:
- F2: The tested measure, read by quintile instead of the plan's median split, shows the same monotonic ordering. The next 3-day demeaned return goes from +0.0107 (t 2.75, n 575) when the 3 biggest hours carry the smallest share of the rise to −0.0061 (t −1.79, n 574) when they carry the largest. The gap is about +0.0168 (Welch t ≈ 3.2). The median split dilutes this to +0.0047 (t 0.83), so the effect sits in the tails.
- F1: Among 3-day rises (72-hour return above 0, non-overlapping 72-bar grid, per-coin quintiles), the path efficiency of the rise, meaning the net log move over the sum of absolute hourly log moves, orders the next 3 days' coin-demeaned return monotonically. The least efficient quintile shows −0.0044 (t −1.29, n 575) and the most efficient shows +0.0113 (t 2.78, n 574). That is a top-minus-bottom gap of about +0.0157 (Welch t ≈ 2.96, worked out from the reported means and standard deviations).
