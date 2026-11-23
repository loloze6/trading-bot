---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_thin-sunday-rise-reverses
line: 7.d confirmed, not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_thin-sunday-rise-reverses_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin whose Sunday close is above its Saturday close falls over the next 2 days, and the smaller the Sunday rise is against the coin's usual one-day move while the coin's 20-day volatility is high, the larger that fall per unit of the rise.
Consequence: Small Sunday drifts up on turbulent coins are the cleanest reason to short at Sunday's close, while outsized Sunday jumps call for a smaller short.
Why:
- F2: The vol-target sizing puts the largest shorts on the calmest coins, where the effect is weakest. In the lowest fifth of 20-day volatility the mean allocation is -0.86, the unusual move is +0.40 % (t 1.45, 435 cases) and the position gain is -0.00 %. In the highest fifth the allocation is -0.30 and the unusual move is +1.75 % (t 3.98, 435). The condition alone does not carry the effect: on bars with no signal, on a 2-bar grid, high-volatility bars give the short -0.62 % (2834 bars), against +0.14 % in the calmest fifth (2324).
- F5: The worst tenth of cases (by position gain) held larger shorts (allocation -0.83 against -0.48) after stronger 7-day rises (+4.8 % against +2.9 %) and larger Sunday rises (+4.5 % against +3.0 %). The trades that closed on Monday lost -3.79 % before fees (1071 trades), while the 2191 that closed on Tuesday gained +0.98 %.
- F6: The thinness grading of the tested idea is barely present in the sizes. The unusual move is +1.22 % in the fifth with the thinnest Sunday volume against +1.44 % in the thickest fifth. By size of the Sunday rise in usual one-day moves, it is +1.61 % for the smallest fifth against +0.93 % for the largest. The effect is still present in every year from 2018 to 2025 (+0.20 % to +2.63 %).
