---
brief: 003_volume-separates-reversal-from-continuation
source-idea: 003-03_heavy-volume-rise-continues
line: 7.g patterns
backtest: 003-03_heavy-volume-rise-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day rise measured against its typical daily move over the past 20 days, the larger its gain over the next 5 days, whatever the day's volume.
Consequence: A trader would size continuation longs by how unusual the day's rise is, not by its volume, and would refuse to pay up for heavy volume alone.
Why:
- F2: On the non-overlapping 5-day grid, the size of a one-day rise predicts the 5-day excess return more than its volume does: among up days with z > 0.3 (n=950), Spearman(z, excess) is 0.086 (p=0.008) and is positive in all 6 coins (0.013 to 0.149); in a joint fit, z has t=1.76 while log relative volume has t=0.71.
- F3: The excess return rises step by step with the day's move in usual units: z in (0.3, 1] gives −0.0001 (n=570), z in (1, 2] gives +0.0155 (t=2.38, n=286) and z > 2 gives +0.0258 (t=1.76, n=94); down and flat days show nothing comparable.
- F1: The book earns almost nothing because it is mostly out of the market: mean daily return 0.000053 against 0.00119 for holding the coins, mean position 0.116 and a position on only 23.5 % of days; of the position's 0.000242 daily gain before costs, 0.000137 comes from the market's own rise and only 0.000104 from timing.
