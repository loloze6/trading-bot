---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile
line: 7.d confirmed, not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 3 days (Monday to Wednesday), the larger the weekend fall the larger the rise, only while the coin's 20-day return is negative, and the rise is larger the more its 20-day volatility of daily returns exceeds its 60-day volatility.
Consequence: Among weekend falls of coins already falling, give the largest position to those whose recent volatility has risen above its longer level, and the smallest to quiet ones.
Why:
- F3: Over all windows the rebound is carried entirely by coins already down over 20 days: excess 3-day return +1.99 % (t 5.4, 659 cases) in the bottom third of the 20-day return (below −10.6 %), +0.45 % (t 1.5) in the middle third, and 0.00 % (t 0.0) in the top third (above +5.3 %); the price against its 50-day mean shows the same pattern (bottom third +1.37 %, t 3.5; others +0.2 %).
- F4: The 20-day-fall condition is not an effect of its own: Sundays without the signal in the bottom third of the 20-day return had an excess 3-day return of −1.60 % (t −5.7, 688 cases), against +1.99 % when the weekend fall is present. The rebound belongs to the weekend fall itself and fits the theory: a thin weekend book is pushed furthest when one-sided selling is already under way.
- F6: The idea's volatility weighting does not repair the falls: trading only when 20-day volatility is above its 60-day level gave Calmar 0.37 and a deepest fall of −12.4 %, but kept only a 4.6 % yearly return.
- F7: Volatility does help inside the falling coins: with a 20-day return in the bottom third, cases with 20-day volatility above its 60-day level had +3.14 % excess (t 5.85, 196 cases) against +0.36 % (t 0.57, 202 cases) below it. Volatility alone on no-signal Sundays earns −0.92 % (t −2.05) in its top third, so it is not an effect of its own.
- F8: The weakest cases lose: the smallest third of Sunday falls (above −1.3 %) had an excess of −0.56 % (t −2.1, 804 cases) and the lowest-forecast third −0.34 % (t −1.1). The largest third of falls (below −3.1 %) had +1.57 % (t 3.9) and the top forecast third +1.42 % (t 3.8).
