---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways
line: 7.b inconclusive
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Monday-and-Tuesday return runs against its weekend (Sunday close-to-close) move: after a weekend rise it falls over the next 2 days, and after a weekend fall it rises over the next 2 days. The larger the weekend move relative to the coin's usual daily move, the larger the move back.
Consequence: The book could take a position after every weekend, short after a rise as well as long after a fall. That would roughly double how often it is exposed, which is what the failing mean return and Calmar need.
Why:
- F1: The reversal belongs to Sunday alone: the signed 2-day move against the day's own move is 0.0082 (t 5.08, n 2051) after Sunday, while every other weekday lies between −0.0036 and +0.0008. Sunday minus the other days is 0.0079, 0.0151 and 0.0084 (Welch t 2.44, 4.78, 2.60) in the three lower |move| quartiles.
- F2: The effect is not graded at the top, which is why the supporting check failed. By |forecast| quartile, the signed 2-day reversal is 0.0037, 0.0152, 0.0125 and 0.0016 (616 cases each). In the largest |move| quartile, Sunday minus the other days is only 0.0011 (t 0.26). The median-split difference of −0.00084 is small next to these swings.
- F4: The main measure is positive in every coin, but alone none of them clears the bar except XMR (t 2.61). BTC sits at t 0.19 and the others between 0.50 and 1.34. It is positive in 7 of 8 years, with 2023 at −0.0014, so the pooled t of 2.75 comes from a small effect spread widely, not from one pocket.
