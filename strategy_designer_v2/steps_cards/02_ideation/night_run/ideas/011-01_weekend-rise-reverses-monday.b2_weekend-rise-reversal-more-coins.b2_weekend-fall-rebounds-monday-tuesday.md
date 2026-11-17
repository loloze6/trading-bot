---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins
line: 7.b inconclusive
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 2 days (Monday and Tuesday), and the larger the weekend fall, the larger the rise.
Consequence: Weekend falls are a reason to buy at Sunday's close, sized by how far the coin fell.
Why:
- F1: The test fails on grading, not on direction. Among Sunday rises the next 2-day excess return is about the same at every size (bottom, middle and top thirds by |forecast|: −1.44%, −0.64%, −1.15%). The rank correlation of the rise's size with the 2-day excess is −0.008 over 2147 Sunday rises. So the top-minus-bottom check comes out at +0.0029 while the main t is 4.88 over 2574 cases.
- F3: The other side of the weekend is graded. Sunday falls are followed by a 2-day excess of +0.57% (t 3.44, n 2086). It grows with the size of the fall: +1.25% after the largest falls (mean −7.5%, t 2.81), +1.03% after −3.4% (t 2.65), +0.83% after −2.0% (t 2.35), and about −0.14% after falls of −0.3% to −1.1%.
- F6: The effect is concentrated around Sunday. Rises sized against the last 60 days are followed over 2 days by −1.00% when the day is Sunday (t −5.94), −0.30% on Monday (t −1.94), +0.44% on Thursday (t 2.72) and −0.03% on Saturday (t −0.22).
