---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_sunday-reversal-in-turbulence
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways.g1_sunday-reversal-in-turbulence_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Sunday move is undone over the next 2 days (Monday and Tuesday), and the lower Sunday's volume stands relative to the coin's 20-day average volume, the larger the part that is undone.
Consequence: A trader would fade Sunday moves made on thin volume harder than Sunday moves made on normal or heavy volume.
Why:
- F6: Sunday's own move reverses over the next 2 days more strongly the lower Sunday's volume is against its 20-day average. By volume quartile, low to high, the scaled slope is −0.43 (t −3.11), −0.24 (t −1.91), −0.19 (t −2.10) and +0.07 (t 1.01), about 651 cases each. This is the brief's thin-liquidity prediction, which the tested idea did not use. Ranked by the 20-day/60-day volatility ratio instead, only the top quartile reverses (−0.26, t −3.24).
- F7: The book's profit is almost entirely Monday. Its mean daily return on Monday days is +0.221 % (std 1.79 %, 414 days), against +0.00 % to +0.01 % on Tuesday to Saturday and −0.03 % on Sunday. Long trades average +1.86 % net (3278 trades) and short trades −0.86 % (2963 trades), so the short side costs the book money.
