---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-06_rebound-in-high-volatility
line: 7.e profitable but not proven
backtest: N2-06_rebound-in-high-volatility_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin in a high-volatility state, the size of the next day's rise grows with the size of the day's fall (in units of its 60-day sd), while the chance of an up day barely changes.
Consequence: The edge lies in sizing up on the largest drops rather than in winning more often, so the position should scale with the drop and the trader should expect a win rate near one half.
Why:
- F2: The gain comes from a minority of large-position bars rather than steady exposure: bars with position > 0.5 (2,269 of 17,380) sum to 28.6 of P&L, bars with position ≤ 0.1 sum to about 0, the top 1 % of bars give 123 % of the total, and the book still makes 15.7 with the 20 best bars removed.
- F4: After a drop of at least 1.5 of the 60-day sd, the next day's rebound is larger in high-volatility bars than in quiet ones, but it is not more frequent: the vol-normalised next return is +0.31 sd (t = 4.75, n = 402) in high volatility against +0.03 sd (t = 0.37, n = 397) in quiet bars, while the up share is 65 % against 60 %, which matches the verdict's z = 0.10 on frequency.
- F7: Counted per trade, the book does not profit: 3,871 one-day trades win 49 %, average −0.46 % gross and −0.56 % net, with 0.87 % commission. The profit comes from position size growing with the drop's size (cubic forecast), so a few large rebounds outweigh many small losers.
