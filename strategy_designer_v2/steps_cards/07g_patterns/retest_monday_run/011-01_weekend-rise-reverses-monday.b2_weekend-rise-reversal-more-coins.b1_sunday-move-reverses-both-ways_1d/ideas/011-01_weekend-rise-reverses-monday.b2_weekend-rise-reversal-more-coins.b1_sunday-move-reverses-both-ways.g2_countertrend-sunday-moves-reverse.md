---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A Sunday move that runs against the coin's previous 4-day move reverses over the next 2 days more than one that extends it, and the more strongly Sunday's move opposes the prior 4-day move, the larger the reversal.
Consequence: A trader would size the Monday-Tuesday fade of Sunday's move by how much that move broke against the week's direction.
Why:
- F3: Sunday moves that go against the coin's previous 4-day move reverse more. Over the next 2 days they reverse by 1.17 % (t 7.62, 2316 cases), against 0.53 % (t 2.98, 2013 cases) for Sunday moves that go with it. That is a gap of about 0.64 % (t about 2.7 from the two standard errors).
- F4: The reversal is spread over both days of the hold and grows with the move. Monday alone gives 0.48 % (t 5.51) and Tuesday alone 0.43 % (t 5.55). The size-weighted measure rises from 0.09 % in the smallest fifth of |Sunday z| to 1.55 % in the largest fifth. The 2-day Saturday+Sunday move carries no reversal (product t 1.22), so the effect belongs to Sunday's own bar.
