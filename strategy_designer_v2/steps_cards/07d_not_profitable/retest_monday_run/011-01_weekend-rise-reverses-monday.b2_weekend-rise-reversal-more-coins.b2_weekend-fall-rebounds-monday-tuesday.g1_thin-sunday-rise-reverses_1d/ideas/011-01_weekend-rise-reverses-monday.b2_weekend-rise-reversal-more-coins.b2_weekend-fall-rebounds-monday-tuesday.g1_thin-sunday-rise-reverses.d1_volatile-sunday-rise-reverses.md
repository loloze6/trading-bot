---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_thin-sunday-rise-reverses
line: 7.d confirmed, not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_thin-sunday-rise-reverses_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin whose Sunday close is above its Saturday close falls over the next 2 days, and the higher the coin's volatility over the past 20 days, the larger that fall measured against the coin's normal drift.
Consequence: A Sunday rise on a turbulent coin is a reason to short it at Sunday's close with conviction, while a Sunday rise on a calm coin is a reason to keep the short small.
Why:
- F1: The book keeps little of the real effect, and its sizing works against it: per case the unusual move in the short's direction is +1.08 % (t 6.95, 2541 cases), but the position's gain over the same 2 days is only +0.33 %, the mean allocation is -0.51, and the size of the short has almost no link to the move that follows (correlation of short size with unusual move -0.02).
- F2: The vol-target sizing puts the largest shorts on the calmest coins, where the effect is weakest. In the lowest fifth of 20-day volatility the mean allocation is -0.86, the unusual move is +0.40 % (t 1.45, 435 cases) and the position gain is -0.00 %. In the highest fifth the allocation is -0.30 and the unusual move is +1.75 % (t 3.98, 435). The condition alone does not carry the effect: on bars with no signal, on a 2-bar grid, high-volatility bars give the short -0.62 % (2834 bars), against +0.14 % in the calmest fifth (2324).
- F3: The book's deepest fall, which drives Calmar to 0.30, is -18.7 % over 376 days in w3–w6, while the coins rose +0.16 % a day. The Sunday rises in that stretch reversed half as much (+0.59 % against +1.21 % elsewhere, 541 against 2000 cases), on calmer coins (20-day volatility 0.035 against 0.050) that had risen more over the prior week (7-day return +4.1 % against +2.8 %).
