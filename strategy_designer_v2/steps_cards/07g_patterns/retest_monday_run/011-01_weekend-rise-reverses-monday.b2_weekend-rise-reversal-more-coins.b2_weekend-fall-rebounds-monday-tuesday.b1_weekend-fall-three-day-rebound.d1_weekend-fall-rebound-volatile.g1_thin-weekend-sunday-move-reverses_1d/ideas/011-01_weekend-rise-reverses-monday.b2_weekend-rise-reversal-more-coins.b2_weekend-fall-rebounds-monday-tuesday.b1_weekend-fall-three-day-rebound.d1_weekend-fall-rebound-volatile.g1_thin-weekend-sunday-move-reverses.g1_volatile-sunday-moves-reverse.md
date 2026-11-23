---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.g1_thin-weekend-sunday-move-reverses
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.g1_thin-weekend-sunday-move-reverses_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Sunday close-to-close move is partly undone over the next 3 days. The higher the coin's 20-day volatility against its own usual level, the larger the share of the move that is undone.
Consequence: A trader would fade Sunday moves hardest when the coin is in a high-volatility stretch and lean only lightly in calm stretches.
Why:
- F1: The fade after a Sunday move grows with the coin's 20-day volatility. In the fade direction, the unusual 3-day move is 0.060 of a usual 3-day move in the low-volatility tercile (t 2.71, n 1423), 0.095 in the middle tercile (t 3.75) and 0.197 in the high tercile (t 6.35). The regression slope on volatility rank is 0.242 (t 4.67, n 4320), and in 17 of 19 coins (89 %) the high-volatility half fades more than the low-volatility half.
- F5: Sunday is the only day whose move reverses clearly over 3 days: fade 0.117, t 7.68, slope on move size t 6.42. Saturday and Friday moves continue over 3 days (−0.032, t −2.22; −0.036, t −2.69). Saturday's fade over 1 day is still positive (0.022, t 2.86).
