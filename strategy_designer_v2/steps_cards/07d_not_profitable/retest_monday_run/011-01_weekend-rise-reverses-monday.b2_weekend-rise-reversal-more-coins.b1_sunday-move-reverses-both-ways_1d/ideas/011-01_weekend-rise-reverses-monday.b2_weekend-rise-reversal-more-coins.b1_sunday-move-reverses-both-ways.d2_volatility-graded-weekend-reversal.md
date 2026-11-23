---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways
line: 7.d confirmed, not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that moved over the weekend (its Saturday-to-Sunday close-to-close return) moves the other way over the next 2 days (Monday and Tuesday), and the move back is larger the more the coin's 20-day daily volatility exceeds its 60-day daily volatility.
Consequence: A trader would size the Sunday-close bet against the weekend move by how far recent volatility has risen above its longer norm, rather than by the weekend move alone, whose largest cases reverse no more than moderate ones.
Why:
- F2: The effect lives almost entirely in Sundays where the coin's 20-day volatility is high against its 60-day volatility. In the top tercile of that ratio the reversal in the forecast's direction is +1.51 % over 2 days (t 5.07, 879 cases). In the middle and low terciles it is only +0.27 % (t 1.00) and +0.35 % (t 1.53). The book's summed position gain is +6.92 in the top tercile against −0.22 and −0.24 in the other two.
- F3: The high-volatility condition is not an effect of its own. On non-Sunday bars in the same top tercile, a 1-day move reverses by only +0.04 % over 2 days (t 0.25, 2750 cases). The Sunday reversal exceeds it by 1.47 % (Welch t 4.42). This fits the brief's theory: a weekend imbalance in an already stressed, thin book is paid more for liquidity.
- F5: Sizing linearly by the weekend move concentrates the falls without buying more reversal. The top |move| quintile holds a mean |allocation| of 0.88 against 0.49 for the fourth quintile, yet reverses less: +0.90 % (t 3.09) against +1.12 % (t 4.41). The worst 2 % of cases carry a mean |allocation| of 0.91. The worst 5 % of cases make up 53 % of all losses.
- F6: Capping the position also improves the falls in the proxy. With the position capped at 0.3 the proxy Calmar is 1.36 (deepest fall −7.9 %); with equal sizing it is 1.28 (−11.2 %); with the tested sizing it is 0.98.
